# CrazyGames

## Билд · лимит общего размера и файлов
Требование: Базовый запуск: общий размер игры ≤ 250 МБ, не больше 1500 файлов (много файлов замедляет загрузку).
Цитата: A maximum total file size of 250MB is allowed. There's a file count limit on 1500 files
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Билд · относительные пути к файлам
Требование: Ссылайся на другие файлы сборки только относительными путями; абсолютные пути не загрузятся.
Цитата: Use only relative paths when referring to other files in the game bundle. Never use absolute paths, as they will fail to load
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Загрузка · начальный размер 50 и 20 МБ
Требование: Начальная загрузка ≤ 50 МБ; чтобы попасть на мобильную главную — ≤ 20 МБ.
Цитата: The game must have an initial download size ≤ 50MB. In order to be eligible for the mobile homepage, the initial download size needs to be ≤ 20MB.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Загрузка · как измеряют размер с SDK
Требование: Если SDK подключён, начальную загрузку считают от старта загрузки до первого события Gameplay start из модуля Game; оно должно сработать, когда игрок уже в играбельном состоянии (без меню и дополнительных экранов загрузки).
Цитата: the initial download size is measured between the start of loading and the occurence of the first Gameplay start event triggered through the Game module.
Цитата: This event should be triggered when the user enters in a playable state, so excludes menus and additional loading steps.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Загрузка · размер без SDK
Требование: Без SDK считается общий размер файлов: ≤ 50 МБ (≤ 20 МБ для мобильной главной).
Цитата: In case the SDK is not integrated, total file size is used and thus should be ≤ 50MB (20MB to be eligible for the mobile home page).
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Загрузка · файлы с внешнего хостинга
Требование: Если файлы грузятся с внешнего хоста, QA оценивает время до начала геймплея: ≤ 20 секунд.
Цитата: For externally hosted/loaded files our QA team will evaluate based on the time it takes to reach gameplay (≤ 20 seconds).
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · поддерживаемые браузеры
Требование: Игра должна работать в Chrome и Edge; если плохо работает в Safari, её отключат в этом браузере.
Цитата: We expect games to work on Chrome and Edge. Games that don't work well on Safari will be disabled on that browser.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · Chromebook и 4 ГБ ОЗУ
Требование: Игра должна плавно работать на устройстве с 4 ГБ ОЗУ, иначе её отключат на Chromium OS (Chromebook).
Цитата: Games will be disabled on Chromium OS if they do not work smoothly on a 4GB RAM device.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · мышь, клавиатура, касание
Требование: Если игра поддерживает мобильные, она должна управляться мышью, клавиатурой и касанием.
Цитата: Game supports mouse, keyboard, and touch if mobile is supported.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · ориентация на десктопе
Требование: На десктопе игра должна быть играбельна в альбомной ориентации; вертикальные игры допустимы (по бокам чёрные полосы или фоновые картинки).
Цитата: Game should be playable in landscape mode on desktop. We allow vertical/portrait games to be published
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · ориентация задаётся в заявке
Требование: Поддерживаемые ориентации указываются при отправке игры; сайт сам попросит повернуть устройство, поэтому свою блокировку ориентации писать не нужно.
Цитата: You can configure supported orientation in your submission. The website will make sure your game can be played only in those orientations
Цитата: Thus, you don't need to implement any orientation lock logic.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · user-select на планшетах
Требование: Добавь в CSS body игры user-select: none (с префиксами -webkit-, -moz-, -ms-), чтобы двойное касание и долгое нажатие на планшетах не вызывали лупу или контекстное меню.
Цитата: To prevent frustration, this CSS should be added to the body of your game:
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · Unity на iOS
Требование: Unity-игры по умолчанию отключены на iOS из-за частых падений от нехватки памяти; включение рассматривают после набора достаточного числа запусков игры.
Цитата: Unity games will be disabled on iOS by default due to frequent crashes (caused by memory shortage).
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · определение типа устройства
Требование: Для разного поведения на десктопе, мобильном и планшете опирайся на system info из SDK CrazyGames.
Цитата: We strongly recommend to rely on our system info to implement a device-specific experience.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Устройства · читаемость в размерах iframe
Требование: Текст и картинки должны читаться при devicePixelRatio 1 в адаптивных iframe 16:9 (от 800x450 на мобильном до 1920x1080 в полноэкранном десктопе) и на мобильных экранах.
Цитата: Text and images must be legible on devices with a devicePixelRatio:1, on responsive iframe sizes (16x9 ratio) and mobile screens (if applicable).
Цитата: 907 x 510 px (desktop - non-fullscreen)
Цитата: 1920 x 1080 px (desktop - fullscreen)
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Производительность · физика на разной частоте
Требование: Физика должна вести себя одинаково на мониторах с разной частотой обновления (в т. ч. 144 и 165 Гц).
Цитата: The game's physics must perform consistently across different monitor refresh rates (e.g. 144 Hz, 165 Hz)
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Звук · возобновление после прерывания iOS
Требование: На iOS AudioContext после сворачивания или звонка не оживает сам: вызови audioContext.resume() внутри жеста пользователя (touchend или click); одного события visibilitychange недостаточно.
Цитата: To revive the audio, developers must call the resume() method within a valid user-initiated gesture, such as a touchend or click event.
Цитата: Simply listening for a visibility change is insufficient
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## SDK · минимум для базового запуска
Требование: Если SDK подключён в базовом запуске, нужно слать событие Gameplay start из модуля Game, когда игрок дошёл до игрового состояния (по нему меряют размер загрузки).
Цитата: A Gameplay start event is triggered from the Game module when the player reaches game state. This is used to measure initial download size.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## SDK · полная интеграция
Требование: Для полного запуска нужны события Gameplay start и stop; модуль Data (если игра сохраняет прогресс) и модуль User (если есть аккаунты, имя и аватар) — по необходимости.
Цитата: Gameplay start/stop events: allow us to measure and report on gameplay experience
Цитата: (if applicable) Data module for saving user game progression
Цитата: (if applicable) User module for account integration and using username/avatar
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## SDK · два этапа запуска
Требование: Базовый запуск (Basic Launch) — выход без доработок под CrazyGames, SDK необязателен, монетизации нет; после отбора в полный запуск (Full Launch) обязательны все интеграционные требования, включая SDK.
Цитата: A game in Basic Launch allows you to go live without needing to customize your game for CrazyGames. The CrazyGames SDK is optional and monetization is not available.
Цитата: Once your game has been selected for Full Launch, you are required to comply to all integration requirements listed below, including the CrazyGames SDK.
Источник: https://docs.crazygames.com/requirements/intro/
Сверено: 2026-10-15

## Ссылки · sitelock и домены CrazyGames
Требование: Если ставишь sitelock, добавь в белый список все домены crazygames.com и отдельные origin приложений CrazyGames для iOS и Android.
Цитата: you need to take into account that CrazyGames operates on multiple crazygames.com origins. If applicable, make sure to whitelist each of our domains
Цитата: Our iOS and Android apps have their own origins, which need to be whitelisted as well.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Прочее · уведомление о персональных данных
Требование: Если игра собирает данные сверх событий SDK, покажи новым игрокам уведомление об условиях и/или политике конфиденциальности; лучше простое уведомление, а не блокирующий попап.
Цитата: the game should add a Terms & Conditions and/or Privacy Policy notice to new players.
Цитата: We recommend to make this a simple notice rather than a pop-up blocking the user.
Источник: https://docs.crazygames.com/requirements/technical/
Сверено: 2026-10-15

## Реклама · только через SDK CrazyGames
Требование: Разрешена только реклама, запрошенная через SDK CrazyGames; внешняя реклама запрещена.
Цитата: Only Ads requested through the CrazyGames SDK are allowed.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · базовый запуск без рекламы
Требование: В базовом запуске реклама отключена и дохода нет; если рекламный SDK подключён, игра не должна зависать (например, между уровнями) — иначе отклонят.
Цитата: Advertisements will be disabled; no revenue will be shared.
Цитата: If you did integrate the Ads SDK, our team will check to make sure the game runs smoothly while ads are disabled. The game will be rejected if it does not.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · не показывать во время игры
Требование: Видеореклама не должна прерывать игру: показывай её в логичных паузах (смена уровня, смерть), а не на навигационных кнопках (главное меню, настройки, магазин).
Цитата: Advertisements should not be shown while a user is playing.
Цитата: Do not show a midgame ad on a navigational button
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · пауза и блокировка интерфейса
Требование: Пока реклама запрашивается или идёт, игрок не должен продвигаться в игре: заблокируй интерфейс до события adFinished или adError.
Цитата: Ensure that a user cannot progress the game while requesting or showing an ad.
Цитата: Block the UI until either an adFinished or adError event occurs.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · обработка adError
Требование: Запрос midgame-рекламы может не заполниться (adblock, тайминг, мало спроса) и вернёт adError; игра обязана продолжиться.
Цитата: In this case you receive an adError event. You should handle this case correctly and ensure that the game continues.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Звук · заглушать при показе рекламы
Требование: Выключай звук игры только когда реклама реально началась (не при запросе) и включай обратно после окончания.
Цитата: You should mute your audio whenever an advertisement starts playing, and unmute it when the ad has finished. Only mute the audio when the ad actually starts playing, and not when you request an ad.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · частота midgame решает SDK
Требование: Можно запрашивать midgame-рекламу в любой удобный момент: SDK сам ограничивает частоту (не чаще 1 раза в 3 минуты) и игнорирует слишком ранние запросы без последствий.
Цитата: the midroll frequency (max 1 every 3 minutes)
Цитата: If the next midgame ad request is too early, it just gets ignored by the SDK and there is no impact for the user.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · rewarded не обязательна для прохождения
Требование: Нельзя делать уровни, которые проходятся только через rewarded-рекламу; это должен быть редкий приятный бонус.
Цитата: Poorly designed levels that can only be completed by a rewarded ad are not acceptable.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · частота и цепочки rewarded
Требование: Не предлагай rewarded слишком часто (покажи таймер или скрой кнопку) и не требуй несколько просмотров ради одной награды.
Цитата: Do not offer a rewarded ad too often. Inform the user of this with a timer or hide the ad request button.
Цитата: Do not chain multiple ads, i.e. watch more than one rewarded ad to receive a single reward.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · кнопка rewarded не в геймплее
Требование: Кнопка запроса rewarded-рекламы не должна появляться на экране активного геймплея (например, во время гонки).
Цитата: The request button should not appear on an active gameplay screen.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Интерфейс · кнопки предложения rewarded
Требование: Кнопка «продолжить без рекламы» должна совпадать по размеру, шрифту и цвету с кнопкой просмотра; скрывать или задерживать кнопку пропуска/закрытия нельзя.
Цитата: the continue without watching a rewarded ad should be the same size, font, color, etc.
Цитата: Hiding or delaying the skip or close button on the offer is not allowed.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · ясность предложения rewarded
Требование: Игрок должен ясно понимать, что за награду нужно смотреть рекламу (например, значок видео), и должна быть альтернатива просмотру, например покупка награды внутриигровыми монетами.
Цитата: It needs to be clear for players that they will have to watch an advertisement in exchange for the reward.
Цитата: Provide an alternative to watching an ad.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · награда только после adFinished
Требование: После adFinished явно покажи, что игрок получил награду; при adError награду выдавать нельзя.
Цитата: When the ad has finished (adFinished), make it clear that the player is rewarded.
Цитата: When our rewarded ad returns with an adError callback, do NOT reward the player.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · rewarded за потерю жизни
Требование: Нельзя предлагать rewarded-видео при каждой потере жизни.
Цитата: It is not allowed to offer an Out-of-lives rewarded video each time the users lose a life.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · midgame и rewarded между уровнями
Требование: Между двумя уровнями нельзя совмещать midgame-рекламу и rewarded «смотри, чтобы продолжить текущий уровень» — только что-то одно.
Цитата: It's not allowed to combine a midgame ad between levels with a rewarded to keep playing the current level.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · где можно баннеры
Требование: Внутриигровые баннеры только на полезных экранах, которые в среднем открыты ≥ 5 секунд; не во время геймплея, не перекрывая интерфейс на любых размерах (включая мобильные).
Цитата: In-game banners are only allowed on useful screens with content that are open for at least 5 seconds on average.
Цитата: Do not show in-game banners during game-play.
Цитата: Make sure that in-game banners do not block any game UI on all game sizes (including on mobile).
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · число баннеров на экране
Требование: На одном экране допускается не больше 2 внутриигровых баннеров, они должны отличаться от игрового контента.
Цитата: A maximum of 2 in-game banners may be displayed on the same screen/view
Цитата: In-game banners must be clearly distinguishable from game content.
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Реклама · игроки с блокировщиком
Требование: Нельзя не пускать игроков с AdBlock и наказывать их; можно отключить отдельные функции с пояснением, но без попапов, и нельзя оставлять кликабельные rewarded-кнопки без эффекта.
Цитата: It is never allowed to block players with AdBlockers from playing, or penalize players with certain disadvantages
Цитата: Do not use popups as they might interfere with fullscreen behaviour and with CrazyGames adblock notices
Цитата: Do not keep the rewarded ads clickable but without effect
Источник: https://docs.crazygames.com/requirements/ads/
Сверено: 2026-10-15

## Витрина · размеры трёх обложек
Требование: Нужны три обложки: альбомная 16:9 — 1920x1080, портретная 2:3 — 800x1200, квадратная 1:1 — 800x800 пикселей; визуал на всех трёх должен быть единым.
Цитата: Landscape - 16:9 (1920x1080 pixels)
Цитата: Portrait - 2:3 (800x1200 pixels)
Цитата: Square - 1:1 (800x800 pixels)
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Витрина · запреты на обложках
Требование: На обложках нельзя: рамки, любые надписи кроме названия игры (New, Play и т. п.), иконки и логотипы магазинов, чужие защищённые картинки, размытая или пикселизованная графика.
Цитата: Don’t put borders around your game covers
Цитата: Don’t write anything else other than your game’s title
Цитата: Don’t use blurry or pixelated visuals
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Витрина · длина и размер превью-видео
Требование: Превью-видео 15–20 секунд (длиннее обрежут до 20), размер файла ≤ 50 МБ.
Цитата: Video Length: 15-20 seconds maximum, longer videos will be cut to 20 seconds
Цитата: Video Size: 50MB maximum
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Витрина · разрешения превью-видео
Требование: Обязательны два видео: полноэкранное альбомное 1080p 16:9 и полноэкранное портретное 1080p 2:3.
Цитата: Full-screen size in landscape (1080p - 16:9 ratio) (mandatory)
Цитата: Full-screen size in portrait (1080p - 2:3 ratio) (mandatory)
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Витрина · чего избегать в видео
Требование: В превью-видео избегай чёрного экрана с логотипом (переход), чёрных полос сверху и снизу и курсора мыши по умолчанию.
Цитата: Black screen and logo transition
Цитата: Black bars top & bottom
Цитата: Default mouse cursor
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Витрина · перемотка и первый кадр видео
Требование: Не ускоряй видео сам (CrazyGames слегка ускоряет при обработке) и начинай его со статичной обложки для плавного перехода от миниатюры.
Цитата: No fast-forwarding: We automatically speed up the video slightly when processing it
Цитата: Use your static cover as the opening frame
Источник: https://docs.crazygames.com/requirements/game-covers/
Сверено: 2026-10-15

## Возраст · соответствие PEGI 12
Требование: Игра должна соответствовать PEGI 12 (аудитория сайта — 13+); у детских игр отдельный сайт, где монетизация отключена.
Цитата: CrazyGames is a website for an audience aged 13 or more. Your game must be PEGI 12 compliant.
Цитата: monetization is disabled on that domain
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Язык · обязательный английский
Требование: В игре обязательна английская локализация.
Цитата: The game must have English localization
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Язык · язык берётся из SDK
Требование: При наличии переводов язык выбирай по locale из метода system info в SDK, а если он недоступен — английский.
Цитата: The game should use the user's language based on locale info provided through the system info method in our SDK, and if not available/set fallback to English.
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Интерфейс · собственная кнопка fullscreen
Требование: Своих кнопок полноэкранного режима в игре быть не должно: fullscreen даёт CrazyGames.
Цитата: Custom in-game fullscreen buttons are prohibited, as they can interfere with other features (e.g. monetization).
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Ссылки · кросс-промо запрещено
Требование: Нельзя рекламировать другие игры и платформы, внешние и внутренние; ссылки на App Store в игре запрещены (используй поля метаданных в Developer Portal).
Цитата: The game should not include cross-promotions for external or internal games/platforms.
Цитата: App Store links are never allowed in-game, and should use the configurable game metadata fields in our Developer Portal
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Ссылки · допустимые исключения
Требование: Допустимы (не как главная кнопка меню): ссылки на другие части серии игр и возврат на главную или категорию CrazyGames; ссылки на сообщество — в меню и без прямого перехода к играбельной веб-версии.
Цитата: Links to other game(s) in the same series of games
Цитата: Backlinks to CG home or category page are accepted but not promoted
Цитата: are allowed on the game menu only as long they don’t lead directly to a playable web version
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Витрина · вход в геймплей в полном запуске
Требование: В полном запуске игра должна сразу приводить новых игроков в геймплей; если нельзя — максимум один клик.
Цитата: Games should land new users in gameplay immediately.
Цитата: a maximum of 1 click is allowed.
Источник: https://docs.crazygames.com/requirements/gameplay/
Сверено: 2026-10-15

## Авторизация · базовая реализация со своим бэкендом
Требование: Если игра хранит профиль и прогресс на своём бэкенде без интеграции, пускай гостей и пользователей CrazyGames как гостей по умолчанию и отключи внешние способы входа (Facebook, Google, email).
Цитата: Allow both guests and registered CrazyGames users to play your game as guests by default
Цитата: Disable any external login options (e.g. Facebook, Google, email)
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · полная реализация, автоматический вход
Требование: Для игр со своими аккаунтами: вошедшего в CrazyGames нового игрока регистрируй и входи автоматически, вернувшегося — входи автоматически, гости играют как гости.
Цитата: New logged in CrazyGames users are automatically registered & logged in within your game.
Цитата: Returning logged in CrazyGames users are automatically logged in within your game.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · выход и внешний вход запрещены
Требование: Нельзя давать выйти из аккаунта в игре и войти через внешние способы (Facebook, Google, email).
Цитата: Logging out in the game and allowing login with external login options (e.g. Facebook, Google, email) is not allowed.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · проверка токена на сервере
Требование: При запуске получай пользователя через getUserToken() (JWT) и проверяй токен на своём сервере, чтобы узнать userId.
Цитата: Start by retrieving the current user by calling getUserToken() to get a JWT Token and verifying the token on your server.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · связка аккаунта по userId
Требование: Аккаунт игры привязывай к CrazyGames userId, а не к имени, которое может измениться.
Цитата: Make sure to make the link based on the userId unique field, as other fields like username might change.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · гость как основной сценарий
Требование: Всегда давай начать игру гостем; кнопка «Login with CrazyGames» допустима, но не как главный CTA, а окно входа нельзя открывать автоматически.
Цитата: You should always allow the user to start playing as Guest, as main scenario.
Цитата: Don't trigger the Auth prompt automatically as this might confuse the user
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · кнопка входа для гостей
Требование: Кнопка входа не должна блокировать игрока; она вызывает Auth prompt из SDK, гостям нельзя предлагать иные способы входа, кроме «Login with CrazyGames».
Цитата: Do not make this the main CTA blocking the user
Цитата: Don't allow Guests to use different login methods than 'Login with CrazyGames'
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Авторизация · вход и выход во время игры
Требование: Гость, вошедший в CrazyGames во время игры, определяется Auth Listener — тогда выполняй сценарий вошедшего пользователя; при выходе страница перезагружается сама.
Цитата: Guest users logging into their CrazyGames account while playing should be detected using an Auth Listener
Цитата: When a user logs out during gameplay, the entire web page is refreshed
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Сохранения · обязательный способ сохранения
Требование: Если в игре есть прогресс, нужно реализовать облачное сохранение; предпочтителен модуль Data из SDK.
Цитата: Unless progress is not applicable for your game, we require you to implement one of these methods.
Цитата: Preferably you use the CrazyGames Data module which saves the user's progress on their CrazyGames account.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Сохранения · прогресс гостя
Требование: Прогресс гостя сохраняется локально автоматически, а при входе синхронизируется в облако, если там ещё не было прогресса.
Цитата: Progress for guest users is automatically saved locally
Цитата: When a guest logs in the progress is synced to their cloud (as long as no cloud progress was present).
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Сохранения · автосохранение и покупки
Требование: Автоматическую систему сохранения прогресса (APS) нельзя использовать в играх с внутриигровыми покупками, так как она опирается на локальные данные.
Цитата: This is not allowed for games with in-game purchases as it relies on local data.
Источник: https://docs.crazygames.com/requirements/account-integration/
Сверено: 2026-10-15

## Покупки · только по приглашению через Xsolla
Требование: Внутриигровые покупки доступны избранным играм: нужна полная реализация с Xsolla в роли платёжного провайдера, заявка через команду CrazyGames.
Цитата: Selected games are eligible for In-game Purchases. A Full Implementation is required, using Xsolla as payments provider.
Источник: https://docs.crazygames.com/requirements/intro/
Сверено: 2026-10-15

## Реклама · монетизация только через SDK
Требование: Основная монетизация — доля от рекламы; разрешена только реклама, поданная через SDK CrazyGames.
Цитата: Only ads served through our SDK are allowed
Источник: https://docs.crazygames.com/requirements/intro/
Сверено: 2026-10-15

## Мультиплеер · передача комнаты в SDK
Требование: Для кнопок Join/Invite передавай через SDK данные о комнате игрока (уникальная комната, isJoinable, inviteParams); экранов онбординга для приходящих друзей избегай или делай пропускаемыми.
Цитата: Pass information on the user's room in your game through the CrazyGames SDK so we can activate our Join/Invite functionality.
Цитата: Avoid onboarding scenes for players joining like this, or make them skippable.
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Мультиплеер · мгновенный вход в комнату
Требование: Первого игрока группы сразу помещай в новую приватную комнату с настройками по умолчанию (при IsInstantMultiplayer = true запускай прямо в мультиплеер); для игр на 20+ игроков можно сразу в публичный геймплей.
Цитата: The first player in a party should be placed directly into a new private room with default settings.
Цитата: When the IsInstantMultiplayer flag is set to true in the SDK, the game should launch directly into multiplayer mode when triggered from the CrazyGames UI.
Цитата: For games that support 20+ players, you may instead place the player directly into public gameplay.
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Мультиплеер · продолжение в раундовых играх
Требование: В конце матча игроки должны продолжать той же группой без возврата через интерфейс CrazyGames: следующий матч в той же комнате или переход всех в новую общую комнату.
Цитата: At the end of a match, players should be able to continue playing with the same group without having to navigate back through the CrazyGames UI.
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Мультиплеер · размер лобби и имена
Требование: Размеры лобби указывай при загрузке билда; имена игроков CrazyGames показывай в игре, чтобы друзья узнавали друг друга.
Цитата: Submit lobby sizes when uploading your game build
Цитата: must be displayed in-game so players can recognize their friends.
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Мультиплеер · мультиплеер в базовом запуске
Требование: Мультиплеерные игры, которым нужна большая аудитория, могут пропустить базовый запуск и сразу идти в полный (с полными требованиями); какой путь — решает QA CrazyGames.
Цитата: Multiplayer games that require a large audience to ensure a good gaming experience may skip Basic Launch and proceed to Full Launch immediately.
Цитата: Our QA team will decide which flow applies for your multiplayer games
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Модерация · чат и пользовательский контент
Требование: Если в игре есть чат, нужна возможность его отключать в настройках и модерация (минимум фильтр мата); при жалобах CrazyGames потребует отключить чат совсем; модерация нужна и для пользовательского контента (картинки, рисунки).
Цитата: Your game should disable your chat based on the game settings. In case of complaints, we will require you to disable chat alltogether.
Цитата: We require you to add chat moderation. The simplest solution is a profanity filter.
Цитата: Moderation is also required if your game involves User Generated Content like uploading custom images or drawings.
Источник: https://docs.crazygames.com/requirements/multiplayer/
Сверено: 2026-10-15

## Интерфейс · клавиши с особым поведением
Требование: Рекомендация: избегай клавиш с особым поведением в вебе — Escape закрывает fullscreen, Ctrl/Cmd+W закрывает вкладку (в fullscreen это можно отключить); подстраивай раскладку под клавиатуру пользователя (AZERTY: ZQSD вместо WASD).
Цитата: Escape closes fullscreen
Цитата: Ctrl / Cmd + W closes the tab; you can disable this when the user is in fullscreen
Цитата: the typical WASD keys for movement are ZQSD on that layout
Источник: https://docs.crazygames.com/requirements/quality/
Сверено: 2026-10-15
