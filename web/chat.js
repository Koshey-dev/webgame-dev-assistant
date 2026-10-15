// Чат ассистента: список чатов, ход потоком NDJSON, след хода, источники.
"use strict";

const $ = (s) => document.querySelector(s);
const ui = {
  side: $("#side"), chats: $("#chats"), thread: $("#thread"), hello: $("#hello"), tries: $("#tries"),
  input: $("#input"), form: $("#composer"), send: $("#sendBtn"), model: $("#model"), title: $("#chatTitle"),
  custom: $("#customBtn"), dlg: $("#customDlg"), slash: $("#slash"), info: $("#indexInfo"),
};
const COMMANDS = [
  ["/help ", "вопрос о проекте: MCP git + документация"],
  ["/platforms", "площадки и что о них в базе"],
  ["/model", "какая модель отвечает"],
];
const TRIES = [
  "Какой лимит размера билда на CrazyGames?",
  "Когда на Яндекс Играх нужно вызвать LoadingAPI.ready?",
  "Сравни требования к рекламе у Poki и Яндекс Игр",
  "/help на какой ветке проект и где лежит сборщик страниц?",
];
const KINDS = { card: "карточка", page: "страница", note: "мой опыт", doc: "документ" };

let state = null, chatId = null, busy = false, controller = null;

// ── Хранилище браузера: только удобства, всё в try/catch ──
const store = {
  get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* приватное окно */ } },
};

// ── Мини-markdown: сначала экранировать, потом разметить ──
function esc(s) {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/\[(\d+)\]/g, '<span class="cite" data-n="$1">[$1]</span>')
    .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
}
function markdown(text) {
  const out = [];
  let list = null, table = null;
  const close = () => {
    if (list) { out.push(`</${list}>`); list = null; }
    if (table) { out.push("</table>"); table = null; }
  };
  for (const raw of text.split("\n")) {
    const line = raw.trimEnd();
    const cells = line.match(/^\|(.+)\|$/);
    if (cells) {
      if (/^\|[\s:|-]+\|$/.test(line)) continue;
      if (!table) { close(); table = true; out.push("<table>"); }
      out.push("<tr>" + cells[1].split("|").map((c) => `<td>${inline(c.trim())}</td>`).join("") + "</tr>");
      continue;
    }
    const li = line.match(/^\s*(?:[-*•]|(\d+)[.)])\s+(.*)$/);
    if (li) {
      const kind = li[1] ? "ol" : "ul";
      if (list !== kind) { close(); list = kind; out.push(`<${kind}>`); }
      out.push(`<li>${inline(li[2])}</li>`);
      continue;
    }
    close();
    const h = line.match(/^#{1,4}\s+(.*)$/);
    if (h) out.push(`<p><b>${inline(h[1])}</b></p>`);
    else if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  close();
  return out.join("");
}

// ── API ──
async function api(path, opts = {}) {
  const r = await fetch(path, { headers: { "Content-Type": "application/json" }, ...opts });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}

// ── Список чатов ──
async function loadChats() {
  const list = await api("/api/chats");
  ui.chats.innerHTML = "";
  for (const c of list) {
    const item = document.createElement("div");
    item.className = "chat-item" + (c.id === chatId ? " on" : "");
    item.innerHTML = `<span>${esc(c.title)}</span><button title="Удалить">✕</button>`;
    item.onclick = () => openChat(c.id);
    item.querySelector("button").onclick = async (e) => {
      e.stopPropagation();
      await api(`/api/chats/${c.id}`, { method: "DELETE" });
      if (c.id === chatId) startFresh();
      loadChats();
    };
    ui.chats.append(item);
  }
}

function startFresh() {
  chatId = null;
  ui.title.textContent = "Новый чат";
  ui.thread.innerHTML = "";
  ui.thread.append(ui.hello);
  ui.hello.hidden = false;
  location.hash = "";
}

async function openChat(id) {
  const chat = await api(`/api/chats/${id}`);
  chatId = chat.id;
  location.hash = chat.id;
  ui.title.textContent = chat.title;
  ui.thread.innerHTML = "";
  for (const m of chat.messages) {
    if (m.role === "user") addUser(m.text);
    else replay(m);
  }
  ui.side.classList.remove("open");
  loadChats();
  scrollDown(true);
}

// ── Отрисовка хода ──
function addUser(text) {
  const el = document.createElement("div");
  el.className = "msg user";
  el.innerHTML = `<div class="bubble">${esc(text)}</div>`;
  ui.thread.append(el);
}

function addAssistant() {
  const el = document.createElement("div");
  el.className = "msg assistant";
  el.innerHTML = `<div class="trace"></div><div class="panels"></div><div class="body caret"></div>
    <div class="sources"></div><div class="meta"></div>`;
  ui.thread.append(el);
  return {
    el, trace: el.querySelector(".trace"), panels: el.querySelector(".panels"),
    body: el.querySelector(".body"), sources: el.querySelector(".sources"), meta: el.querySelector(".meta"),
    text: "", stage: null,
  };
}

function chip(view, html, cls = "") {
  const c = document.createElement("span");
  c.className = "chip " + cls;
  c.innerHTML = html;
  view.trace.append(c);
  return c;
}

function panel(view, cls, html, toggle) {
  const p = document.createElement("div");
  p.className = cls;
  p.innerHTML = html;
  view.panels.append(p);
  toggle.classList.add("click");
  toggle.onclick = () => p.classList.toggle("open");
}

function onEvent(view, ev) {
  if (view.stage && ev.type !== "stage") { view.stage.classList.remove("run"); }
  switch (ev.type) {
    case "stage":
      if (view.stage) view.stage.classList.remove("run");
      view.stage = chip(view, esc(ev.title), "run");
      break;
    case "rewrite":
      view.stage.innerHTML = `запрос: <b>${esc(ev.query)}</b> · ${ev.ms} мс`;
      break;
    case "mcp": {
      const c = chip(view, `MCP <b>${esc(ev.tool)}</b> → ${esc(mcpShort(ev))} · ${ev.by} · ${ev.ms} мс`, "mcp");
      panel(view, "mcpres", esc(`${ev.server} · ${ev.tool}(${JSON.stringify(ev.args)})\n\n` +
        JSON.stringify(ev.result, null, 2)), c);
      break;
    }
    case "hits": {
      const passed = ev.hits.filter((h) => h.passed).length;
      const where = ev.platforms.length ? ` · площадки: ${ev.platforms.join(", ")}` : "";
      const c = chip(view, `поиск: <b>${passed}</b> из ${ev.hits.length} выше порога ${ev.threshold.toFixed(2)}, ` +
        `в ответ ${ev.chosen}${where} · ${ev.ms} мс`);
      panel(view, "hits", ev.hits.map((h) =>
        `<div class="${h.passed ? "pass" : ""}"><span class="s">${h.score.toFixed(3)}</span>` +
        `${esc(KINDS[h.kind] || h.kind)} · ${esc(h.platform || h.title)} · ${esc(h.section || h.title)}</div>`).join(""), c);
      break;
    }
    case "delta":
      view.text += ev.text;
      view.body.innerHTML = markdown(view.text);
      scrollDown();
      break;
    case "error":
      chip(view, esc(ev.text), "err");
      break;
    case "done":
      finish(view, ev);
      break;
  }
}

function mcpShort(ev) {
  const r = ev.result || {};
  if (r.error) return "ошибка";
  if (ev.tool === "git_branch") return r.branch === "HEAD" && r.tag ? `тег ${r.tag}` : r.branch;
  if (ev.tool === "git_status") return `${(r.changes || []).length} изменений`;
  if (ev.tool === "git_log") return `${(r.commits || []).length} коммитов`;
  if (ev.tool === "list_files") return `${r.total} файлов`;
  return "ok";
}

function finish(view, done) {
  view.body.classList.remove("caret");
  if (view.stage) view.stage.classList.remove("run");
  if (!done) { view.meta.textContent = "ответ прерван"; return; }
  view.body.innerHTML = markdown(done.text || view.text);
  view.sources.innerHTML = "";
  for (const s of done.sources || []) {
    const el = document.createElement("div");
    el.className = "src" + (s.cited ? "" : " dim");
    el.id = `src-${s.n}`;
    const link = /^https?:/.test(s.ref) ? `<a href="${esc(s.ref)}" target="_blank" rel="noopener">${esc(s.ref)}</a>`
      : `<code>${esc(s.ref)}</code>`;
    el.innerHTML = `<div class="head"><span class="n">[${s.n}]</span><b>${esc(s.platform || s.title)}</b>` +
      `<span>${esc(s.section || s.title)}</span><span class="badge ${s.kind}">${esc(s.kind_title)}</span>` +
      (s.checked ? `<span class="badge">${s.kind === "page" ? "собрано" : "сверено"} ${esc(s.checked)}</span>` : "") +
      (s.stale ? `<span class="badge stale">требует сверки</span>` : "") +
      `<span class="badge">cos ${s.score.toFixed(2)}</span></div>` +
      (s.quote ? `<blockquote>${esc(s.quote)}</blockquote>` : "") + link;
    view.sources.append(el);
  }
  view.body.querySelectorAll(".cite").forEach((c) => {
    c.onclick = () => document.getElementById(`src-${c.dataset.n}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  const parts = [done.model];
  if (done.first_ms) parts.push(`первое слово ${(done.first_ms / 1000).toFixed(1)} с`);
  if (done.total_ms) parts.push(`всего ${(done.total_ms / 1000).toFixed(1)} с`);
  if (done.refusal) parts.push("ответ кода: ниже порога");
  view.meta.textContent = parts.join(" · ");
}

function replay(m) {
  const view = addAssistant();
  for (const ev of m.trace || []) onEvent(view, ev);
  view.text = m.text || "";
  finish(view, m.done ? { ...m.done, text: m.text } : null);
  if (m.cut && !m.done) view.body.innerHTML = markdown(view.text);
}

function scrollDown(force) {
  const t = ui.thread;
  if (force || t.scrollHeight - t.scrollTop - t.clientHeight < 160) t.scrollTop = t.scrollHeight;
}

// ── Отправка ──
function customSettings() { return store.get("wda.custom", { base_url: "", model: "", key: "" }); }

async function send(text) {
  if (busy || !text.trim()) return;
  busy = true;
  ui.send.disabled = true;
  ui.hello.hidden = true;
  if (!chatId) {
    const chat = await api("/api/chats", { method: "POST" });
    chatId = chat.id;
    location.hash = chat.id;
  }
  addUser(text);
  const view = addAssistant();
  scrollDown(true);
  const model = ui.model.value;
  controller = new AbortController();
  let done = null;
  try {
    const r = await fetch(`/api/chats/${chatId}/send`, {
      method: "POST", headers: { "Content-Type": "application/json" }, signal: controller.signal,
      body: JSON.stringify({ text, model, custom: model === "custom" ? customSettings() : null }),
    });
    if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
    const reader = r.body.getReader();
    const dec = new TextDecoder();
    let buf = "";
    for (;;) {
      const { value, done: end } = await reader.read();
      if (end) break;
      buf += dec.decode(value, { stream: true });
      let nl;
      while ((nl = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, nl);
        buf = buf.slice(nl + 1);
        if (!line.trim()) continue;
        const ev = JSON.parse(line);
        if (ev.type === "done") done = ev;
        onEvent(view, ev);
      }
    }
  } catch (e) {
    chip(view, esc(String(e.message || e)), "err");
  } finally {
    if (!done) finish(view, null);
    busy = false;
    ui.send.disabled = false;
    loadChats();
  }
}

// ── Ввод и подсказка команд ──
function autosize() {
  ui.input.style.height = "auto";
  ui.input.style.height = Math.min(ui.input.scrollHeight, 180) + "px";
}

function showSlash() {
  const v = ui.input.value;
  const fits = v.startsWith("/") && !v.includes("\n") ? COMMANDS.filter(([c]) => c.startsWith(v.split(" ")[0])) : [];
  if (!fits.length || COMMANDS.some(([c]) => v.startsWith(c.trim() + " ") && c.trim() !== "/help")) {
    ui.slash.hidden = true;
    return;
  }
  if (v.startsWith("/help ")) { ui.slash.hidden = true; return; }
  ui.slash.innerHTML = fits.map(([c, d]) => `<div data-c="${c}"><code>${c.trim()}</code><small>${d}</small></div>`).join("");
  ui.slash.hidden = false;
  ui.slash.querySelectorAll("div").forEach((d) => {
    d.onclick = () => { ui.input.value = d.dataset.c; ui.slash.hidden = true; ui.input.focus(); };
  });
}

ui.input.addEventListener("input", () => { autosize(); showSlash(); });
ui.input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    ui.form.requestSubmit();
  }
});
ui.form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = ui.input.value;
  ui.input.value = "";
  ui.slash.hidden = true;
  autosize();
  send(text);
});
$("#newChat").onclick = () => { startFresh(); loadChats(); ui.side.classList.remove("open"); };
$("#burger").onclick = () => ui.side.classList.toggle("open");

// ── Модель и свой API ──
ui.model.onchange = () => {
  store.set("wda.model", ui.model.value);
  ui.custom.hidden = ui.model.value !== "custom";
  if (ui.model.value === "custom" && !customSettings().base_url) openCustom();
};
ui.custom.onclick = openCustom;
function openCustom() {
  const c = customSettings();
  $("#cuUrl").value = c.base_url;
  $("#cuModel").value = c.model;
  $("#cuKey").value = c.key;
  ui.dlg.showModal();
}
ui.dlg.addEventListener("close", () => {
  if (ui.dlg.returnValue !== "ok") return;
  store.set("wda.custom", { base_url: $("#cuUrl").value.trim(), model: $("#cuModel").value.trim(), key: $("#cuKey").value.trim() });
});

// ── Старт ──
async function boot() {
  state = await api("/api/state");
  for (const m of state.models) {
    const o = new Option(m.title + (m.disabled ? " (нет ключа)" : ""), m.id);
    o.disabled = !!m.disabled;
    ui.model.append(o);
  }
  const saved = store.get("wda.model", null);
  ui.model.value = state.models.some((m) => m.id === saved && !m.disabled) ? saved : state.default_model;
  ui.custom.hidden = ui.model.value !== "custom";
  const idx = state.index;
  const cards = idx["platforms/card"] || 0, pages = idx["platforms/page"] || 0;
  ui.info.innerHTML = `Площадок ${state.platforms.length} · карточек ${cards} · кусков страниц ${pages}` +
    (idx["notes/note"] ? ` · мой опыт ${idx["notes/note"]}` : "") + ` · проект ${idx["project/doc"] || 0}`;
  for (const t of TRIES) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = t;
    b.onclick = () => send(t);
    ui.tries.append(b);
  }
  await loadChats();
  if (location.hash.length > 1) openChat(location.hash.slice(1)).catch(startFresh);
}
boot();
