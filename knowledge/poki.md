# Poki

## Возраст · аудитория всех возрастов
Требование: Poki рассчитан на всех, включая детей: всё на площадке должно быть безопасным и комфортным для любого возраста, и подходить рекламодателям.
Цитата: our audience spans all ages, and every game on Poki must be rated for kids.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-11-20

## Контент · запрещённые темы
Требование: Не принимаются игры с небезопасными для всех возрастов темами: травля, насилие и сексизм, жёсткое насилие и раны, затяжной страх, сексуальный контент, азартные игры, алкоголь, табак и т. п.
Цитата: Graphic violence, including open or infected wounds and visible body fluids
Цитата: Sexual content or inappropriate clothing
Цитата: Cheating, gambling, alcohol, tobacco, or other offensive material
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Модерация · что исправимо, а что нет
Требование: Слегка неприемлемый контент (лёгкие романтические механики, намёки, сцены насилия) можно убрать и подать заново после существенных правок; взрослые темы и чужая интеллектуальная собственность — мгновенный отказ.
Цитата: Mildly inappropriate content, like light dating mechanics, suggestive jokes, or violent scenes, can often be removed or reframed
Цитата: Adult themes and misused IP are rejected immediately.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Модерация · проверка контента перед тестом
Требование: Каждая новая версия игры проходит модерацию контента до входа в тестирование (кроме игр, уже находящихся в QA, Soft Release или Global Release).
Цитата: Every new game version goes through a content moderation check before it can enter testing
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Мультиплеер · чат запрещён
Требование: Игровой чат между игроками недопустим; вместо него используй систему эмодзи.
Цитата: Chat systems expose players, especially younger ones, to real risks, so games can't include them.
Цитата: An emoji system works well and keeps everyone safe.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Мультиплеер · чат в политике внешних ресурсов
Требование: Чаты в игре запрещены; как замену выразительности игроков предлагают эмодзи.
Цитата: Chat systems aren't allowed. An emoji system is a great alternative for player expression.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Ссылки · внешние ассеты запрещены
Требование: Во время игры нельзя обращаться к внешним ресурсам (Google Fonts, внешние картинки и аудио, библиотеки с CDN вроде jsDelivr): всё скачай и включи в билд.
Цитата: No runtime requests to Google Fonts, externally hosted images or audio, or code libraries on external CDNs like jsDelivr. Download and bundle these assets into your build instead.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Авторизация · внешние аккаунты запрещены
Требование: Игра не должна собирать персональные данные: никаких входов по email, через Google или Facebook и других систем с идентифицируемыми данными.
Цитата: Games must not collect personal information. No email-based logins, no Google or Facebook sign-in.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Ссылки · исключения для внешних сервисов
Требование: По отдельному одобрению Poki возможны внешние игровые серверы мультиплеера, аналитика (GameAnalytics, ByteBrew, своя; продукты Google, включая Google Analytics, не одобряются) и внешние лидерборды.
Цитата: Multiplayer servers: externally hosted game servers are fine once approved by Poki.
Цитата: Google products (including Google Analytics) cannot be approved.
Цитата: Leaderboards: externally hosted leaderboard services are reviewed case by case.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Ссылки · как одобрить внешний ресурс
Требование: Запроси ресурс сам в Settings → CSP игры в Poki for Developers, указав ссылки и пояснение; после одобрения CSP обновят, а для сброса кэша нужно заново загрузить свежую версию.
Цитата: Go to Settings → CSP on your game in Poki for Developers and request the resource update yourself
Цитата: Once your requested services are reviewed, please re-uploaded your latest version.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Ссылки · политика конфиденциальности для сервисов
Требование: Для одобренных внешних сервисов нужна актуальная политика конфиденциальности на живой странице, доступной всем игрокам и со ссылкой из игры; Poki не проверяет и не даёт образцы политик.
Цитата: Provide an up-to-date privacy policy: hosted on a live webpage accessible to all players, linked inside the game
Цитата: Poki can't review or provide example privacy policies due to a conflict of interest.
Источник: https://developers.poki.com/guide/external-resources-policy
Сверено: 2026-10-15

## Контент · клоны не принимаются
Требование: Прямые копии и клоны никогда не принимаются; вдохновляться жанрами можно, но нужно добавить своё (шаблоны и asset flip без существенных изменений не считаются оригинальной работой).
Цитата: Direct copies and clones are never accepted; they violate our Terms & Conditions.
Цитата: Templates and asset flips with little modification don't qualify as original work either.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Контент · ИИ-материалы перед отправкой
Требование: Перед подачей: чистая, единая графика; без водяных знаков ИИ и текста промптов; диалоги вычитаны; всё проверено играми. По запросу покажи, какие ИИ-инструменты и как использовал.
Цитата: No AI watermarks or prompt text visible anywhere.
Цитата: Everything is playtested. No untested generated content ships.
Цитата: Be able to show how and which tools were used, and to provide an overview of your creation process, prompts, and iterations on request.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Контент · оригинальность при ИИ
Требование: К тесту player fit или web fit игра должна отражать твой авторский взгляд и существенные улучшения сверх базовых ИИ-инструментов; Poki вправе отклонить любую неоригинальную игру, даже работающую хорошо.
Цитата: before your game enters a player fit or web fit test, it should reflect your unique perspective and meaningful improvements beyond the base tooling.
Цитата: we reserve the right to decline any game that lacks originality or doesn't add to the diversity of the platform
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Витрина · миниатюра должна соответствовать игре
Требование: Миниатюра должна совпадать по стилю с игрой; лоскутные стили и вводящая в заблуждение графика, не из игры, недопустимы.
Цитата: Mismatched patchwork styles, or misleading art that isn't the game
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Контент · тренды и перенасыщение
Требование: Игра по тренду должна добавлять что-то своё, а не набор мемов и вирусных челленджей без геймплея; при перенасыщении жанра Poki может отклонять похожие заявки.
Цитата: Something unique added to the trend, not a collection of memes, viral challenges, or tropes without meaningful gameplay underneath.
Цитата: When a genre or trend gets crowded, we may decline additional similar submissions
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Прочее · частые причины отказа
Требование: Чаще всего отказывают за баги и неработающий геймплей, избыточный размер загрузки или слабую производительность, запутанный UX и непоследовательную графику.
Цитата: Buggy or broken gameplay
Цитата: Excessive load size or poor performance
Цитата: Confusing UX, or poor and inconsistent graphics
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Устройства · web-first
Требование: Игра должна быть задумана для веба как основной платформы, а не быть портом с мобильных.
Цитата: Web-first: designed for the web as a primary platform, not a mobile port.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Устройства · мобильная аудитория
Требование: Управление и интерфейс должны одинаково удобно работать и пальцем, и мышью; большая часть аудитории Poki — мобильная, десктоп-only игра в невыгодном положении.
Цитата: controls and UI that work as well with a thumb as with a mouse. Our audience is majority mobile, so a desktop-only game is at a disadvantage.
Источник: https://developers.poki.com/guide/what-we-look-for
Сверено: 2026-10-15

## Производительность · быстрая загрузка и малый размер
Требование: Poki проверяет техническую зрелость: быстрая загрузка, стабильная частота кадров и небольшой размер файлов на разных устройствах и движках (числовых лимитов на странице нет).
Цитата: it’s really important to nail fast load times, stable frame rates, and a lean file size across devices and engines!
Источник: https://developers.poki.com/guide/what-we-look-for
Сверено: 2026-10-15

## Интерфейс · альтернативное управление
Требование: Желательно поддерживать альтернативные схемы управления (только мышь, drag-управление, автоускорение, настраиваемые клавиши), а не только WASD.
Цитата: we encourage supporting alternative control methods like mouse only input, drag steering, auto acceleration, or customizable keys.
Источник: https://developers.poki.com/guide/content-player-safety
Сверено: 2026-10-15

## Витрина · первое впечатление
Требование: Игроки решают за секунды, поэтому важны понятная миниатюра и сразу играбельное начало.
Цитата: players decide in seconds, so a clear thumbnail and an immediate, playable opening matter as much as the game underneath.
Источник: https://developers.poki.com/guide/what-we-look-for
Сверено: 2026-10-15

## SDK · подключение и инициализация
Требование: Подключи скрипт Poki SDK в <head> и вызови PokiSDK.init() в начале игры; даже при ошибке инициализации игру надо загрузить.
Цитата: <script src="https://game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>
Цитата: Initialize the SDK at the start of your game with the following JavaScript:
Цитата: Initialized, something went wrong, load your game anyway
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## SDK · завершение загрузки
Требование: Вызови PokiSDK.gameLoadingFinished() по окончании загрузки — по нему считается конверсия в игру.
Цитата: To provide an accurate conversion to play metric for your game, fire the following event when your loading has finished:
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## SDK · события gameplayStart и gameplayStop
Требование: gameplayStart() вызывай, когда игрок играет (старт уровня, снятие паузы), gameplayStop() — когда не играет (конец уровня, game over, пауза, выход в меню).
Цитата: Use the gameplayStart() event to describe when players are playing your game (for example, level start and unpause).
Цитата: Use the gameplayStop() event to describe when players aren't playing your game (for example, level finish, game over, pause, or quit to menu).
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Реклама · commercialBreak на естественных паузах
Требование: Видеореклама показывается через commercialBreak(); вызывай его перед каждым gameplayStart(), когда игрок готов продолжать; не каждый вызов даёт рекламу — решает система Poki, поэтому сигналь как можно чаще.
Цитата: we recommend calling commercialBreak() before every gameplayStart(), whenever the player has shown intent to continue playing.
Цитата: Not every commercialBreak() triggers an ad. Poki's system decides when a player is ready for another ad
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Реклама · rewardedBreak и награда
Требование: Перед rewardedBreak() заранее скажи игроку, что он увидит рекламу; награду выдавай только если видео показано (success = true).
Цитата: When using rewardedBreak(), make it clear to the player beforehand that they're about to watch an ad.
Цитата: video not displayed, should not give reward
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Реклама · rewarded сбрасывает таймер
Требование: Взаимодействие игрока с rewardedBreak сбрасывает рекламный таймер, чтобы сразу после него не показалась ещё одна реклама.
Цитата: when a player interacts with a rewarded break, our system's ad timer resets so they don't immediately see another ad.
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Звук · отключать звук и ввод на рекламе
Требование: Во время commercial break отключай звук и клавиатурный ввод, чтобы игра не мешала рекламе, а после — возвращай и вызывай gameplayStart().
Цитата: Make sure that audio and keyboard input are disabled during commercial breaks, so that the game doesn't interfere with the ad
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Интерфейс · запрет прокрутки страницы
Требование: На Poki игра стоит внутри прокручиваемой страницы, поэтому отключи через preventDefault скролл от пробела, стрелок и колеса мыши.
Цитата: When a player presses space or the arrow keys, the default browser behavior is to emulate scroll.
Цитата: But on Poki, it will be inside a longer page that can scroll.
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Интерфейс · Poki Pill на мобильных
Требование: Кнопку Poki Pill на мобильных можно сдвинуть через PokiSDK.movePill(topPercent, topPx), но не ниже 50% области игры; размер 46x62 px на экранах уже 1211 px и 92x64 px на более широких.
Цитата: You can't move the pill lower than 50% of the game area
Цитата: 46px × 62px on screens narrower than 1211px.
Цитата: 92px × 64px on screens 1211px wide or wider.
Источник: https://developers.poki.com/guide/sdk-html5
Сверено: 2026-10-15

## Модерация · финальное ревью
Требование: После тестирования команда Poki оценивает соответствие качеству, оригинальность и уникальность в категориях; решение занимает 1–2 недели.
Цитата: Whether the game and its content are in line with our quality guidelines, including originality and craft
Цитата: 1-2 weeks. It takes time to make an informed decision
Источник: https://developers.poki.com/guide/final-review
Сверено: 2026-10-15

## Модерация · путь после финального ревью
Требование: После прохождения ревью до релиза идут юридический этап, QA, Soft Release и Global Release — всего примерно 2–3 месяца.
Цитата: legal, QA, Soft Release, and Global Release, roughly 2 to 3 months in total.
Источник: https://developers.poki.com/guide/final-review
Сверено: 2026-10-15

## Модерация · QA-проверка
Требование: После подписания договора открывается QA: при недочётах приходит отчёт, ты исправляешь, загружаешь новый билд и запрашиваешь повторную проверку, пока не пройдёшь.
Цитата: If it's not quite ready, you receive a QA report detailing what's needed to pass
Цитата: upload a new build, request a review, and QA continues until you're through.
Источник: https://developers.poki.com/guide/release-process
Сверено: 2026-10-15

## Модерация · Soft Release 2–3 недели
Требование: Soft Release нельзя пропустить; слот в календаре ждут обычно 1–2 недели, сам период — около 2–3 недель, и всё это время нужно быть готовым выпускать правки.
Цитата: It typically takes 1-2 weeks to schedule a soft release slot in our release calendar.
Цитата: The soft release period should take around 2-3 weeks.
Цитата: The soft release phase cannot be skipped.
Источник: https://developers.poki.com/guide/release-process
Сверено: 2026-10-15

## Реклама · цель по монетизации в Soft Release
Требование: В Soft Release ориентир по монетизации — не менее 1 рекламы на активного пользователя в день, с разумным соотношением midroll и rewarded.
Цитата: Monetization: aim for at least 1 ad per daily active user, with a healthy split between midroll and rewarded videos
Источник: https://developers.poki.com/guide/release-process
Сверено: 2026-10-15

## Модерация · переход к Global Release
Требование: От Soft Release до Global Release обычно проходит 2–3 недели, в зависимости от показателей и скорости оптимизации.
Цитата: it usually takes 2 - 3 weeks to move from soft release to global release.
Источник: https://developers.poki.com/guide/release-process
Сверено: 2026-10-15

## Модерация · обновления после выпуска
Требование: Обновление отправляется как при QA: загрузи новый билд и запроси ревью; после одобрения поддержка публикует версию.
Цитата: To submit an update, simply follow the same process as during QA: upload a new build and request a review.
Источник: https://developers.poki.com/guide/release-process
Сверено: 2026-10-15
