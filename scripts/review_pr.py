"""Клиент ревью для GitHub Action: diff PR → сервер ассистента → комментарий в PR.

Только стандартная библиотека — раннеру не нужен pip. Ключ модели, индекс и
сама модель остаются на сервере; здесь — только git, HTTP и API GitHub.
Комментарий один на PR: новый пуш обновляет его, а не добавляет новый.

Окружение (задаёт workflow): REVIEW_URL, REVIEW_TOKEN, GITHUB_TOKEN,
GITHUB_REPOSITORY, PR, BASE, HEAD, TITLE.

    python3 scripts/review_pr.py
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

MARKER = "<!-- webgame-review -->"
BOT = "github-actions[bot]"
MAX_FILE = 200_000           # файл крупнее идёт только диффом
STATUS = {"A": "added", "D": "deleted"}


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout


def collect(base, head):
    """Diff PR от точки ветвления и полные тексты изменённых файлов на head."""
    diff = git("diff", "--no-color", "-M", f"{base}...{head}")
    files = []
    for line in git("diff", "--name-status", "-M", f"{base}...{head}").splitlines():
        status, *paths = line.split("\t")
        path, content = paths[-1], None
        if not status.startswith("D"):
            try:
                content = git("show", f"{head}:{path}")
            except (subprocess.CalledProcessError, UnicodeDecodeError):      # двоичный файл
                content = None
            if content is not None and len(content) > MAX_FILE:
                content = None
        files.append({"path": path, "status": STATUS.get(status[0], "modified"), "content": content})
    return diff, files


def call(url, method="GET", body=None, headers=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    return json.loads(raw) if raw else None


def github(method, path, body=None):
    return call(f"https://api.github.com{path}", method, body,
                {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                 "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})


def upsert(repo, pr, text):
    """Свой комментарий ищется по автору-боту и метке: метку в тексте мог оставить и человек."""
    mine, page = None, 1
    while mine is None:
        comments = github("GET", f"/repos/{repo}/issues/{pr}/comments?per_page=100&page={page}")
        if not comments:
            break
        mine = next((c for c in comments if c["user"]["login"] == BOT and MARKER in c["body"]), None)
        page += 1
    if mine:
        github("PATCH", f"/repos/{repo}/issues/comments/{mine['id']}", {"body": text})
    else:
        github("POST", f"/repos/{repo}/issues/{pr}/comments", {"body": text})


def summary(text):
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text + "\n")


def main():
    env = os.environ
    repo, pr = env["GITHUB_REPOSITORY"], int(env["PR"])
    if not env.get("REVIEW_URL") or not env.get("REVIEW_TOKEN"):
        sys.exit("нет REVIEW_URL или REVIEW_TOKEN: переменная и секрет репозитория")
    diff, files = collect(env["BASE"], env["HEAD"])
    print(f"PR #{pr}: файлов {len(files)}, diff {len(diff)} символов")
    try:
        result = call(env["REVIEW_URL"], "POST",
                      {"repo": repo, "pr": pr, "title": env.get("TITLE", ""), "head": env["HEAD"],
                       "diff": diff, "files": files},
                      {"Authorization": f"Bearer {env['REVIEW_TOKEN']}"}, timeout=300)
    except urllib.error.HTTPError as e:
        reason = e.read().decode("utf-8", "replace")[:500]
        summary(f"Ревью не получилось: HTTP {e.code} {reason}")
        sys.exit(f"сервер ревью: HTTP {e.code} {reason}")
    except (urllib.error.URLError, TimeoutError) as e:
        summary(f"Ревью не получилось: сервер не ответил ({e})")
        sys.exit(f"сервер ревью не ответил: {e}")
    upsert(repo, pr, result["markdown"])
    summary(result["markdown"])
    found = {key: len(items) for key, items in result["findings"].items()}
    print(f"готово: {found}, карточек проверено {result['cards']['checked']}, "
          f"с ошибками {len(result['cards']['problems'])}")


if __name__ == "__main__":
    main()
