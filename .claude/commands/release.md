---
description: Выпуск игры на площадку — собрать и проверить конвейером ассистента, выложить в кабинет через MCP Playgama
argument-hint: <игра> [площадка, по умолчанию playgama]
---

Выпусти игру `$1` из репозитория игр на площадку `$2` (не задана — `playgama`). Конвейер
ассистента (`webgame-release`) собирает и проверяет, ты выкладываешь через MCP `playgama`.
Отвечай по-русски.

## Границы

Можно: читать кабинет; создать черновик и заполнить форму; загрузить архив и обложки;
получить ссылку QA Tool. Нельзя: `publish_sandbox`, `start_sandbox_traffic`,
`replace_in_app_products`, `create_leaderboard`, `update_leaderboard`, `apply_referral_code` —
и всё, чего нет в шагах ниже (запрещённое закрыто и в `.claude/settings.json`, `deny`).
На модерацию игру отправляет человек кнопкой в консоли.
Ссылки загрузки (`uploadUrl`) подписаны — в итог их не выводи.

## Шаги

1. `get_game_checklist` без `page` — официальный чек-лист. Не прочитался — скажи и остановись:
   без чек-листа сборку проверенной не называть.
2. Игра в кабинете: `list_applications`, затем `get_application` у каждой — черновик этой игры
   тот, у кого есть архив с именем `$1-…` (конвейер называет архивы `<игра>-<дата>-<коммит>`).
   Нашёлся — из имени его последнего архива возьми коммит прошлой выкладки (`since`).
3. `prepare` сервера `webgame-release`: `game` = `$1`, `platform`, `checklist` — markdown из
   шага 1, `since`. Идёт 1–3 минуты.
4. `status: blocked` — покажи блокеры таблицей (пункт, почему, `путь:строка`), путь к патчу и к
   `fix_note`, отчёт `report`, и остановись: исправленное надо закоммитить и запустить снова.
5. Форма. Прочитай `form.fields` и `form.notes` и сверь с описанием полей
   `update_application_form`: категория — по её определениям, в текстах нет того, чего нет в
   сборке (`form.notes`, факты отчёта), нет чужих брендов. Явное противоречие поправь сам и скажи,
   что поправил; спорное (например, название) оставь и вынеси в итог.
6. Черновика нет — `create_application`: `title` из формы, `engine`, `agent`, `model` из формы,
   `modelId` — твоя модель. Есть — `update_application_form` с полями формы.
7. Архив: `start_archive_upload` (`name` = `archive.name`, `contentSize` = `archive.bytes`),
   `curl -sS -T "<archive.path>"` на `uploadUrl` ровно с выданными заголовками,
   `confirm_archive_upload`, затем `get_archive_status` раз в 10–15 с, пока `CHECKING`.
   `PROBLEM` или `NOT_CHECKED` — `state.message` дословно и остановись.
8. Обложки: для каждой из `covers` — `start_cover_upload` (`cover` = `slot`, `format`,
   `contentSize` = `bytes`), PUT через curl, `confirm_cover_upload`.
9. `get_archive_qa_tool_link` — ссылку бери из ответа, не собирай сам.
10. Сверка кабинета с конфигом Bridge (`bridge`): `list_in_app_products`, `list_leaderboards`.
    Чего нет в кабинете — в итог как дело для человека, сам не заводи.
11. `get_launch_steps` и `get_submission_state` (архив из шага 7).

## Итог

Коротко: коммит и архив (id, `state`), обложки, что в форме поправлено, ссылка QA Tool;
пункты чек-листа «проверить руками» (`manual`) номерами; «карточка отстала» (`stale`);
что осталось человеку в консоли — покупки и лидерборды, отправка на модерацию. Путь к отчёту
конвейера — `report`.
