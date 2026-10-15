# Playgama

## Билд · общий размер архива
Требование: общий размер всех файлов игры в загружаемом архиве не больше 300 МБ.
Цитата: The total size of all game files does not exceed 300 MB when uploaded as an archive.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Билд · index.html и имена файлов
Требование: index.html лежит в корне архива; имена файлов и папок только латиницей.
Цитата: An index.html file is added to the root of the archive. File and folder names use only Latin characters.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Билд · Facebook размер и файлы
Требование: для партнёра Facebook билд не больше 200 МБ, в архиве не больше 500 файлов.
Цитата: The game build size should not exceed 200 MB.
Цитата: The game archive should contain no more than 500 files.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · Facebook сжатие Unity
Требование: для Unity-игр на Facebook отключить Decompression Fallback (off) и использовать сжатие Brotli или Gzip.
Цитата: For Unity games, set Decompression Fallback to off.
Цитата: For Unity games, use Brotli or Gzip compression.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · MSN размер
Требование: для партнёра MSN билд меньше 50 МБ.
Цитата: Have a build size under 50 MB.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · Xiaomi размер
Требование: для партнёра Xiaomi размер игры не больше 100 МБ.
Цитата: The game size should not exceed 100 MB.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · YouTube Playables размер
Требование: для YouTube Playables начальный билд не больше 30 МБ.
Цитата: Have an initial build no larger than 30 MB.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · YouTube Playables файлы
Требование: для YouTube Playables в именах файлов только буквы, цифры и символы . - _ (без пробелов и спецсимволов); в бандле не больше 8000 файлов; в Unity Decompression Fallback должен быть true.
Цитата: File names must not contain special characters or spaces. Allowed characters are letters, digits, ., -, and \_
Цитата: The game bundle must contain 8,000 or fewer files.
Цитата: If the game is built in Unity, Decompression Fallback must be set to true.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · TikTok размер
Требование: для TikTok игра не больше 30 МБ.
Цитата: Be no larger than 30 MB.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Билд · GameSnacks размеры файлов
Требование: для GameSnacks каждый файл меньше 10 МиБ, вся игра не больше 100 МиБ, начальная загрузка меньше 15 МиБ.
Цитата: Every file must be less than 10 MiB.
Цитата: The size of the game must not be more than 100 MiB.
Цитата: The initial download must be less than 15 MiB.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Загрузка · Facebook скорость
Требование: для Facebook очень быстрая загрузка, желательно меньше 3 секунд.
Цитата: Ensure very fast loading times, preferably under 3 seconds.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Загрузка · CrazyGames и Xiaomi
Требование: загрузка не дольше 5 секунд для CrazyGames (Playgama там сейчас не публикует) и меньше 15 секунд для Xiaomi.
Цитата: Loading time should be no more than 5 seconds.
Цитата: Load in under 15 seconds.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Загрузка · GameSnacks время запуска
Требование: для GameSnacks игра должна стать играбельной меньше чем за 15 секунд на соединении от 10 Мбит/с.
Цитата: Game must be playable in less than 15 seconds on any connection of at least 10 Mbps.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Производительность · ошибки и зависания
Требование: в игре не должно быть технических сообщений, ошибок, вылетов и зависаний при долгой работе и действиях игрока (поворот экрана, долгое нажатие, свайпы, сворачивание браузера, показ рекламы, переходы по истории).
Цитата: There are no technical messages, errors, or crashes, freezing after some time of use, or during certain user actions, such as screen rotation, long press on the game field, gestures and swipes, minimizing the browser, opening ads, browsing history transitions, and other interactions.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## SDK · Playgama Bridge обязателен
Требование: в игру нужно встроить Playgama Bridge SDK; без него игру часто отклоняют.
Цитата: The Playgama Bridge is integrated into the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## SDK · событие Game Ready
Требование: игра должна отправлять событие Game Ready; его отсутствие входит в частые причины отказа при модерации.
Цитата: The Playgama Bridge SDK is not integrated, the Game Ready event is not sent, or progress is not saved through SDK methods.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## SDK · внешняя аналитика запрещена
Требование: нельзя подключать внешнюю аналитику (Google Analytics GA4 и подобную), запросы к ней могут блокироваться; для аналитики использовать модуль analytics из Bridge (с версии Bridge 2.3.0).
Цитата: The game does not include external analytics systems such as Google Analytics (GA4) or similar — requests to them may be blocked.
Цитата: (available since Bridge 2.3.0)
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## SDK · внешние вызовы на партнёрах
Требование: для партнёрских площадок YouTube Playables, TikTok и GameSnacks в игре не должно быть внешних вызовов, включая встроенную аналитику.
Цитата: Not contain any external calls, including built-in analytics.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Авторизация · не требовать вход
Требование: для запуска и использования игры нельзя требовать регистрацию или авторизацию на внешних сервисах.
Цитата: Registration or authorization on external services is not required for launching and using the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Реклама · только через Bridge
Требование: рекламу показывать только через Playgama Bridge; рекламы сторонних рекламодателей, в том числе статичных картинок и текста, быть не должно.
Цитата: No ads from third-party advertisers, including static ad images and text. Ads are displayed only through the Playgama Bridge.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · паузы и место показа
Требование: рекламу показывать в логических паузах (между уровнями, после конца игры, после паузы); блоки не должны появляться под пальцем или курсором поверх нужного элемента.
Цитата: Ads are shown during logical pauses: between levels, after the game ends, after pressing pause, etc. Ads should not interfere with gameplay.
Цитата: Ad blocks should not appear under the player's finger or cursor on top of an element the player wants to click on or get information from.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · ориентация и состояние
Требование: рекламные блоки должны соответствовать ориентации игры, а игровой процесс сохраняться после перехода по рекламе и возврата.
Цитата: The internal process is saved after transitioning through the ad and returning.
Цитата: All ad blocks have an orientation matching the game's orientation.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · пауза звука и игры
Требование: при показе полноэкранной рекламы (interstitial или rewarded video) звук и игровой процесс должны быть на паузе.
Цитата: When showing full-screen ads (interstitial or rewarded video), the game sound and gameplay must be paused.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · rewarded видео
Требование: награда за rewarded-видео — дополнительный бонус (бустеры, доп. действия, пропуск уровня и т. п.), не влияющий на возможность продолжить игру; кнопка должна ясно говорить, что будет реклама и что игрок получит.
Цитата: The reward for watching a rewarded video is an additional bonus (e.g., but not limited to: boosters, additional actions, level skip, bonus levels, and other similar mechanics) to the main game and should not affect the ability to continue the gameplay.
Цитата: the user will now watch an ad for a reward;
Цитата: the user understands what they will receive as a reward.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · запрет жизни за рекламу
Требование: нельзя предлагать rewarded-рекламу за «+1 жизнь» каждый раз, когда игрок теряет жизнь.
Цитата: It is forbidden to offer reward-based ads to “gain +1 life” every time users lose a life.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · дополнительные баннеры
Требование: дополнительные рекламные блоки допускаются только в виде sticky-баннеров; собственные RTB-баннеры запрещены.
Цитата: Additional ad blocks are exclusively sticky banners.
Цитата: The use of custom RTB banners is prohibited.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Реклама · Facebook старт игры
Требование: для Facebook не показывать рекламу в самом начале игры.
Цитата: Do not display ads at the very start of the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Покупки · только через Bridge
Требование: платежи только через Playgama Bridge.
Цитата: Payments are made only through the Playgama Bridge.
Источник: https://wiki.playgama.com/playgama/game-requirements/advertising-requirements.md
Сверено: 2026-10-15

## Покупки · без микротранзакций
Требование: микротранзакции и любые внешние покупки запрещены, разрешены только внутренние покупки через Bridge.
Цитата: There are no microtransactions or any external purchases. Only internal purchases via the Playgama Bridge are allowed.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Покупки · реальные деньги и призы
Требование: нельзя давать выигрыши или вывод реальных денег и призов (физические призы, подписки, внешний контент, денежные эквиваленты); игра не может быть интернет-магазином, азартной игрой или онлайн-лотереей.
Цитата: There are no winnings or withdrawals of real money and prizes that are not internal values, such as physical prizes, subscriptions, external content, cash equivalents of prizes, etc.
Цитата: The game is not an online store, gambling game, or online lottery.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Покупки · Facebook и Discord
Требование: для Facebook нужно минимум две из четырёх функций (покупки, таблицы лидеров, мультиплеер, шаринг с друзьями); для Discord нужны внутриигровые покупки.
Цитата: Include at least two of the following features: in-app purchases, leaderboards, multiplayer, and social sharing with friends.
Цитата: Include in-game purchases.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Сохранения · прогресс обязателен
Требование: если в игре есть сюжет или уровни, нужно сохранение прогресса; в бесконечной игре или игре на рекорд — сохранение рекорда; прогресс должен сохраняться корректно.
Цитата: The game includes a save progress option if the game mechanics involve progressing through the story or levels. If it's an endless game or a high-score game, there is a record save feature.
Цитата: The game properly saves player progress.
Источник: https://wiki.playgama.com/playgama/game-requirements/user-experience-requirements.md
Сверено: 2026-10-15

## Сохранения · через методы SDK
Требование: прогресс нужно сохранять через методы SDK; сохранение не через SDK и некорректное сохранение — частые причины отказа.
Цитата: The Playgama Bridge SDK is not integrated, the Game Ready event is not sent, or progress is not saved through SDK methods.
Цитата: The game does not properly save player progress.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Сохранения · смена ориентации
Требование: на мобильных прогресс игры не должен теряться при смене ориентации устройства.
Цитата: Game progress is saved when changing device orientation.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Язык · перевод интерфейса
Требование: интерфейс переведён на все заявленные языки, язык интерфейса совпадает с языком игры; название игры одинаково в игре и в материалах черновика на одном языке.
Цитата: The app interface is not translated into all declared languages, or the interface language does not match the game language.
Цитата: The app name does not match between the game and the draft materials in one language.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Язык · выбор языка
Требование: язык должен легко выбираться даже при включённом незнакомом языке: флаги или названия языков на их языке (English, Español); меню к выбору языка понятны без текста (шестерёнка, глобус).
Цитата: Languages are indicated by country flag icons or the language names in their own languages (e.g., English, Español).
Цитата: All menus and settings leading to language selection are understandable without text and represented by universal icons (e.g., gear for settings, globe for localization).
Источник: https://wiki.playgama.com/playgama/game-requirements/user-experience-requirements.md
Сверено: 2026-10-15

## Язык · Playhop и VK русский
Требование: для Playhop / Yandex нужна поддержка русского языка; для VK русский — язык по умолчанию, весь интерфейс и тексты переведены (Playgama на VK сейчас не публикует).
Цитата: Support the Russian language.
Цитата: Support Russian as the default language. All interface elements, texts, dialogues, descriptions, and instructions must be translated into Russian.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Устройства · мобильные требования
Требование: на мобильных игра идёт в полноэкранном режиме; клавиатура появляется автоматически при нажатии на поле ввода; управление полностью жестами (акселерометр допустим как дополнение); системный плеер не открывается в браузерах; нет уведомления о WebGL.
Цитата: The game runs in full-screen mode during gameplay or startup.
Цитата: If data entry is possible (e.g., player nickname or document name), the keyboard automatically appears when clicking on the input field.
Цитата: The game is fully controlled by gestures. Control mechanics can be supplemented by using the mobile device's accelerometer.
Цитата: There is no WebGL notification when opening the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Устройства · ориентация на мобильных
Требование: элементы не должны деформироваться при смене ориентации; если игра поддерживает одну ориентацию, это нужно указать в черновике, и в обратной ориентации будет показана заглушка с просьбой повернуть устройство.
Цитата: If the game only supports one orientation, the corresponding value must be selected when filling out the draft. In the opposite orientation, a special placeholder for rotating the device will be displayed.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Устройства · десктопное поле
Требование: на десктопе игровое поле растягивается по вертикали или горизонтали до края доступной области (без учёта sticky-баннеров), его соотношение сторон не больше 1:2; управление по умолчанию с клавиатуры или мыши.
Цитата: The active field stretches vertically or horizontally to the edge of the available area (excluding sticky banners).
Цитата: The aspect ratio of the active field does not exceed 1:2.
Цитата: The game is controlled by keyboard or mouse by default.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Устройства · браузеры и ОС
Требование: игра должна корректно работать в Chrome, Firefox, Opera, Safari, Edge; на Windows Vista/7/8/10 и Mac OS X 10.6+; на Android 5.0+ и iOS 9.0+.
Цитата: Browsers: Google Chrome, Mozilla Firefox, Opera, Safari, Edge.
Цитата: Mobile operating systems: Android 5.0 and higher, iOS 9.0 and higher.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Устройства · рекомендуемые ориентации
Требование: рекомендуется (не обязательно) иметь кнопки home и pause и поддерживать портретную и ландшафтную ориентации.
Цитата: The game has "home" and "pause" buttons.
Цитата: The game should implement both portrait and landscape orientations.
Источник: https://wiki.playgama.com/playgama/game-requirements/other-requirements.md
Сверено: 2026-10-15

## Устройства · MSN, TikTok и YouTube
Требование: MSN требует ландшафт (или ландшафт и портрет); TikTok — портрет и работу на iOS и Android; YouTube Playables — портрет и корректный ландшафт без чёрных полос по бокам.
Цитата: Support landscape orientation, or both landscape and portrait orientation.
Цитата: Support portrait orientation.
Цитата: Support both portrait and properly adapted landscape orientation, without black bars on the sides.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Устройства · GameSnacks формат
Требование: для GameSnacks игра работает на iOS и Android и поддерживает портретное соотношение 9:16.
Цитата: Run on both iOS and Android.
Цитата: The game must support a 9:16 portrait aspect ratio.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Интерфейс · отображение
Требование: поле не выходит за границы экрана, элементы не обрезаются и не перекрываются; нет системной полосы прокрутки страницы (своя прокрутка внутри игры допустима); у всех всплывающих окон есть крестик или кнопка закрытия.
Цитата: The active field scale does not exceed the screen boundaries, and elements are not cut off.
Цитата: There is no browser page scrolling (browser window system scrollbar). However, it is allowed to implement custom content scrolling within the game.
Цитата: All pop-up windows have a cross or button to close them.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Интерфейс · управление одной рукой
Требование: игра управляется одной рукой, оставаясь на главной сцене без дополнительных прокруток и свайпов (движение внутри большого поля допустимо в стратегиях, RPG и др.).
Цитата: It is possible to control the game with one hand and remain on the main scene without additional scrolling or swiping.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Интерфейс · важные элементы не обрезаны
Требование: важные элементы интерфейса не должны обрезаться границами игровой области так, чтобы часть действий стала невозможной.
Цитата: Important interface elements are cut off by the game area boundaries (making some actions in the game impossible).
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Звук · пауза при рекламе и сворачивании
Требование: при сворачивании страницы игры (на десктопе и мобильных) звук должен останавливаться.
Цитата: When the game page is minimized on desktop and mobile devices, the sound stops playing.
Источник: https://wiki.playgama.com/playgama/game-requirements/user-experience-requirements.md
Сверено: 2026-10-15

## Звук · пауза при рекламе
Требование: звук должен останавливаться при показе рекламы и при сворачивании экрана; невыполнение — частая причина отказа.
Цитата: Sound in the game does not pause when an ad is played or when the screen is minimized.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Звук · наличие и кнопка mute
Требование: игра не может быть полностью беззвучной (нужны музыка, сигналы, звуки интерфейса) и должна иметь кнопку mute.
Цитата: The game cannot be completely silent. Background music, sound signals, and UI sounds are important for enhancing the game quality.
Цитата: A mute button must be implemented in the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/user-experience-requirements.md
Сверено: 2026-10-15

## Контент · запрещённые темы
Требование: в игре не должно быть реалистичного насилия над детьми или животными, политики, религии и предсказаний о жизни, здоровье или смерти игрока.
Цитата: Realistic scenes depicting violence and/or abuse towards children or animals.
Цитата: Images or references to politics, political situations, political figures, internal or international conflicts, wars.
Цитата: Images or references to religion, religious figures, or religious attributes.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Контент · чужие бренды и персонажи
Требование: нельзя использовать чужие авторские права (названия, логотипы брендов, музыку); персонажей из других игр и фильмов (Brawl Stars, Sprunki, Squid Game и др.) не принимают.
Цитата: No one's copyrights (names, brand logos, music) are used.
Цитата: If your game uses characters from another game or movie (Brawl Stars, Sprunki, Squid Game, etc.), we don't accept those either.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Контент · копии и продолжения
Требование: игра не должна быть полной или частичной копией другой игры каталога или дублировать игру того же разработчика; продолжение принимается отдельной игрой, только если графика и механика полностью переработаны, иначе обновляйте прежнюю игру.
Цитата: The game is not a complete or partial copy of another game in the catalog and does not duplicate another game by the same developer.
Цитата: it is accepted as a separate game only if the graphics and mechanics are completely redesigned.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Контент · ИИ-генерация
Требование: ассеты, сгенерированные ИИ, допустимы, но игра не должна целиком строиться на генеративном ИИ; низкокачественные игры, целиком созданные ИИ, отклоняют.
Цитата: Games can use AI-generated assets, but they shouldn't be built entirely from them.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Контент · отказ за игры только на ИИ
Требование: низкокачественные игры, целиком созданные генеративным ИИ и ничего не добавляющие игроку, отклоняют.
Цитата: The game is a low-quality title built entirely with generative AI and does not add anything meaningful to the player experience.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Контент · видео и YouTube-плеер
Требование: видео в игре допустимо только так, чтобы через интерфейс плеера нельзя было перейти на внешние ресурсы; встраивание через YouTube-плеер не принимается — использовать свой хостинг или класть видео в архив.
Цитата: Integration of videos through YouTube player does not meet this condition, and games with such integration cannot be accepted.
Цитата: it is recommended to use your own hosting or embed the video in the archive.
Источник: https://wiki.playgama.com/playgama/game-requirements/content-requirements.md
Сверено: 2026-10-15

## Контент · данные пользователя
Требование: если игра работает с данными пользователя, для действий с ними нужно явное разрешение пользователя.
Цитата: If the game handles user data, explicit permission from the user is required for actions involving their data.
Источник: https://wiki.playgama.com/playgama/game-requirements/other-requirements.md
Сверено: 2026-10-15

## Возраст · запрещённый контент
Требование: запрещены эротика, порнография, мат и оскорбления по полу, национальности, религии, сцены суицида, разжигание ненависти, фашизм и экстремистские материалы.
Цитата: erotic, pornographic materials, depictions of objects imitating genitalia, and/or references to sexual acts
Цитата: obscene language, vulgar expressions, and phrases
Цитата: Contains descriptions of means and methods of suicide, as well as any incitement to commit it.
Цитата: Contains extremist materials and violates other rights and interests of citizens and legal entities or the laws of other countries.
Источник: https://wiki.playgama.com/playgama/game-requirements/other-requirements.md
Сверено: 2026-10-15

## Возраст · CrazyGames и Game Distribution
Требование: для CrazyGames целевая аудитория 13+; для Game Distribution — без сцен насилия и явной крови (оба требования партнёров; Playgama на CrazyGames сейчас не публикует).
Цитата: Target audience should be 13+.
Цитата: Not contain scenes of violence or explicit depictions of blood on the screen.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Модерация · границы проверки
Требование: прохождение модерации не подтверждает соответствие законам какой-либо территории и отсутствие претензий третьих лиц по правам; тестирование идёт в средах, близких к пользовательским.
Цитата: Passing moderation does not confirm that the game complies with the laws of any territory or that it is free from third-party rights claims.
Цитата: Game testing is performed in environments that closely resemble user environments.
Источник: https://wiki.playgama.com/playgama/game-requirements.md
Сверено: 2026-10-15

## Модерация · частые причины отказа
Требование: отказывают также за баги, мешающие использованию, и за технические сообщения, ошибки, вылеты и зависания; перед загрузкой стоит пройти чек-лист самопроверки.
Цитата: The app has bugs or issues that hinder usability.
Цитата: The app contains technical messages or errors, crashes, or freezes.
Источник: https://wiki.playgama.com/playgama/game-requirements/game-self-check.md
Сверено: 2026-10-15

## Модерация · ограничения по URL
Требование: в игре не должно быть технических средств, ограничивающих её работу в зависимости от URL, с которого она открыта.
Цитата: The game does not include any technical means of limiting its operation due to the URL it is opened from.
Источник: https://wiki.playgama.com/playgama/game-requirements/technical-requirements.md
Сверено: 2026-10-15

## Витрина · критерии игры
Требование: игра должна подходить хотя бы под один критерий: есть игровой прогресс, есть механики взаимодействия или есть сюжет; также нужны нарастающая сложность и понятный сюжет или сеттинг.
Цитата: It has game progress.
Цитата: It has a plot (progressive unfolding of game events, choosing certain actions and getting storyline results).
Цитата: The game has increasing difficulty and a clear storyline or setting.
Источник: https://wiki.playgama.com/playgama/game-requirements/user-experience-requirements.md
Сверено: 2026-10-15

## Витрина · объём контента для партнёров
Требование: Playhop / Yandex — контента хватает больше чем на 10 минут игры; VK — больше 10 минут; Xiaomi — средняя сессия не меньше 5 минут; TikTok — не меньше 10 минут; YouTube Playables — в идеале больше 8 минут.
Цитата: Have enough content to keep players engaged for more than 10 minutes.
Цитата: Have an average playtime of at least 5 minutes.
Цитата: Have an average playtime of at least 10 minutes.
Цитата: Have a strong average playtime, ideally over 8 minutes.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Витрина · публикация зависит от партнёров
Требование: MSN публикует только 2–4 игры от партнёра в месяц; YouTube принимает игры в ограниченном числе; Playgama на CrazyGames и VK сейчас не публикует, публикацию на TikTok приостановили из-за низкого трафика.
Цитата: MSN only publishes 2–4 games per partner each month on their platform.
Цитата: YouTube accepts games in limited numbers.
Цитата: Playgama currently doesn't publish games on Crazygames.
Цитата: At the moment, we've paused publishing games on TikTok due to low traffic.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Ссылки · внешние ссылки на партнёрах
Требование: для Game Distribution нельзя никаких исходящих ссылок (редиректы, Google Analytics, прочая аналитика, соцсети), хостинг внутренний (кроме real-time мультиплеера); для Facebook не ссылаться на другие сайты и приложения и не показывать сторонней рекламы.
Цитата: Not use any outgoing links, including redirects, Google Analytics, other analytics, or social media links.
Цитата: Be hosted internally, except for real-time multiplayer games.
Цитата: Do not reference any other websites or applications and do not display third-party ads.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Ссылки · выдавать себя за бренд
Требование: игра не должна выдавать себя за официальный продукт внешнего приложения или бренда и использовать посторонние бренды для привлечения аудитории.
Цитата: It does not pretend to be an official product of an external application or brand.
Цитата: It does not use unrelated brands to attract an audience.
Источник: https://wiki.playgama.com/playgama/game-requirements/other-requirements.md
Сверено: 2026-10-15

## Мультиплеер · Discord и Facebook
Требование: для Discord в игре должен быть мультиплеер; для Facebook мультиплеер — одна из функций на выбор (нужно минимум две из четырёх).
Цитата: Include multiplayer mode.
Цитата: Include at least two of the following features: in-app purchases, leaderboards, multiplayer, and social sharing with friends.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Прочее · требования VK к жизням и соцфункциям
Требование: для VK прогрессовые блокеры (жизни, энергия) восстанавливаются автоматически, на первом запуске игрок начинает с полным запасом; соцфункции не должны ограничивать игру, если игрок отказался от приглашений, постов и т. п.
Цитата: Progress blockers such as lives or energy must automatically regenerate over time.
Цитата: functionality cannot be restricted for users who decline optional actions such as sending invites, posting on walls, receiving notifications, or joining game groups.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15

## Прочее · TikTok кнопки Shortcut и Sidebar
Требование: для публикации в TikTok нужно реализовать в игре кнопки Home Screen Shortcut и Sidebar.
Цитата: For publishing, you need to be ready to implement a Home Screen Shortcut button in the game.
Цитата: You’ll also need to implement a Sidebar button in the game.
Источник: https://wiki.playgama.com/playgama/game-requirements/platform-specific-requirements.md
Сверено: 2026-10-15
