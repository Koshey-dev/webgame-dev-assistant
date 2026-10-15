# GameDistribution

## Билд · допустимые движки и HTTPS
Требование: игра должна быть собрана на движке вроде Unity WebGL, JavaScript или Construct 2/3 и работать по HTTPS.
Цитата: Games must be built using engines such as Unity WebGL, Javascript, or Construct 2 & 3.
Цитата: Games must be HTTPS ready to allow for secure content delivery.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Билд · внешний хостинг запрещён
Требование: внешний хостинг игры не разрешён (исключение — реальный мультиплеер; по мультиплееру нужно писать в GD).
Цитата: We do not permit external hosting of games, except for
Цитата: If you have a multiplayer game, or any questions regarding a specific multiplayer mechanic, please reach out to us for guidance.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Билд · iframe и адаптивный размер
Требование: игра должна без обрезок и сбоев работать в iframe и полноэкранном режиме и подстраиваться под разные размеры экрана; рекомендуемый размер iframe — 800x600.
Цитата: the game should offer responsive resizing to adapt to different screen sizes.
Цитата: We recommend using the standard iframe dimensions of 800 (width) x 600 (length).
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Билд · логотип Unity с полноэкранным режимом
Требование: не используй логотип Unity WebGL вместе с кнопкой полноэкранного режима — это ломает масштаб и рекламу в fullscreen.
Цитата: Please avoid the use of the Unity WebGL logo accompanied by a fullscreen option.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Производительность · плавность и задержка ввода
Требование: игра должна идти плавно, с минимумом просадок кадров и без задержки ввода; на десктопе — в Chrome, Firefox и Safari.
Цитата: the game should run smoothly with limited frame-drops and without user input delays.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Устройства · десктоп обязателен
Требование: игра обязана работать на десктопе в популярных браузерах, управление — клавиатура и/или мышь.
Цитата: The game must be playable on desktop, ensuring smooth performance on popular browsers such as Google Chrome,
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Устройства · мобильная версия желательна
Требование: мобильная совместимость не обязательна, но рекомендована: такие игры получают приоритетное размещение у топовых издателей.
Цитата: While not mandatory, we strongly recommend making games playable on as many devices as possible.
Цитата: Games that are compatible on mobile devices receive priority placement with top game publishers.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Устройства · ориентация экрана
Требование: если у игры предпочтительная ориентация, нужно зафиксировать её или показать экран с просьбой повернуть устройство; управление должно быть удобным на тачскрине.
Цитата: Games with a preferred orientation should lock the user in that orientation or include a screen to instruct the user to turn the device.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## SDK · пре-ролл обязателен
Требование: пре-ролл и мид-ролл реклама через SDK GD обязательны для всех игр; дисплейная и rewarded — по желанию.
Цитата: the correct implementation of preroll and midroll ads is mandatory for all games.
Цитата: The use of display and rewarded ads is optional and recommended to further enhance revenue potential.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · пре-ролл после Play
Требование: пре-ролл показывается до начала игры, как правило после нажатия на кнопку Play.
Цитата: This ad type guarantees that users are exposed to an advertisement before the game begins.
Цитата: Preroll ads are typically displayed following a click on the ‘Play’ button.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · мид-ролл в паузах
Требование: мид-ролл показывается в естественных паузах (между уровнями или по таймеру); при желании можно поставить таймер 2 минуты.
Цитата: A midroll ad is an advertisement shown during natural breaks in the game, such as between levels or after a specific amount of time has passed.
Цитата: developers can choose to set a 2-minute timer for midroll ads.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · пауза и звук на время показа
Требование: на время рекламы игру нужно ставить на паузу и глушить звук; после рекламы показать экран паузы, снимаемый только действием игрока.
Цитата: The game must be paused and muted during advertisements so that the ad can run properly and the game progress is not affected.
Цитата: they should encounter a pause screen that resumes only upon player interaction
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · награда только за просмотр
Требование: в rewarded-рекламе награду можно выдавать только после полностью завершённого показа.
Цитата: users can only be given a reward when an impression is completed.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · баннер не закрывает игру
Требование: дисплейный (баннерный) блок не должен перекрывать игровой контент ни при каком разрешении окна.
Цитата: the display ad must not cover any in-game content, taking into account different window resolutions.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Реклама · показ вне игрового процесса
Требование: рекламу лучше показывать только вне геймплея (между уровнями, в паузах); при её запуске звук игры глушится, а сама игра ставится на паузу.
Цитата: we recommend that ads are displayed only during non-gameplay moments, such as between levels or during pauses.
Цитата: When an ad is triggered, game audio must be muted and the game itself should be paused.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Звук · обязательные звуковые элементы
Требование: в игре обязательны музыка, звуковые эффекты и звуки интерфейса; рекомендуется кнопка отключения звука и музыки.
Цитата: Your game must include sound elements such as background music (BGM), sound effects (SFX) and User Interface (UI) sounds.
Цитата: We recommend designing a toggle button for both sound and background music to improve user interface.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Интерфейс · перекрытие элементов UI
Требование: элементы интерфейса не должны перекрывать друг друга и мешать управлению (например, закрывать кнопки звука или Play).
Цитата: It is required that there are no overlapping UI elements that obstruct player interaction.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Интерфейс · кнопка Play и читаемость
Требование: кнопка Play должна быть всегда видна, кнопки понятны (универсальные иконки), текст читаем.
Цитата: The play button should always be visible to guide players toward starting the game.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Интерфейс · цель игры и обучение
Требование: цель игры должна быть интуитивной либо объяснена простым обучением; нестандартное управление описывается до начала игры.
Цитата: The game’s objective should either be intuitive to users or explained through a simple tutorial.
Цитата: Any instructions or deviations from generic controls should be clearly outlined for the player before the game begins.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Язык · английский по умолчанию
Требование: язык игры по умолчанию всегда английский.
Цитата: the default game language should always be English.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Язык · выбор языка при мультиязычности
Требование: в мультиязычной игре нужно определять язык браузера или дать выбрать язык до старта, чтобы обучение не показывалось на невыбранном языке.
Цитата: the game should either detect the browser language, or give players the opportunity to choose a preferred language before the game starts.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Язык · вариант No-Text
Требование: если в игре совсем нет текста (только универсальные иконки), при загрузке можно выбрать опцию No-Text вместо языка.
Цитата: you can select the ‘No-Text’ option instead of a specific language.
Цитата: should only be used if your game has no text at all.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · запрещённые темы
Требование: запрещены политическая ангажированность, оскорбительный религиозный контент, откровенные отсылки к алкоголю, наркотикам и сексу, расизм и дискриминация, чрезмерное насилие.
Цитата: Games are prohibited from including
Цитата: Political bias or offensive religious
Цитата: Excessive use of violence
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · пользовательский ввод
Требование: если игроки вводят текст (имена, чат), нужна защита от неприемлемой лексики и вредного контента.
Цитата: for games with user-input content, such as custom player names or chat options, mechanisms should be in place to prevent the use of inappropriate language or any other harmful content by players.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · чужие названия в заголовке
Требование: в названии игры нельзя использовать известные защищённые бренды (вроде «Super Mario»).
Цитата: Please avoid using well-known, copyrighted names like
Цитата: or any other protected intellectual property in your game titles.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · права на материалы
Требование: у тебя должно быть законное право на весь контент игры, включая разрешения владельцев брендов и персонажей; нужно уметь подтвердить это документами.
Цитата: It is crucial that you have the legal right to use all of the content featured in your game.
Цитата: It is important that you are able to show that you have permission to use any content that is not yours.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · копии чужих игр
Требование: напрямую скопированные или украденные игры не принимаются (вдохновляться существующими играми можно).
Цитата: submitting games that have been directly copied or stolen from existing titles is not permitted.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Контент · дипфейки и ИИ
Требование: если в игре есть созданный или изменённый ИИ контент, похожий на реальных людей, места или события и выглядящий настоящим, нужно явно указать его искусственное происхождение.
Цитата: you must clearly and distinguishably explain that the content has been artificially created or manipulated along with its artificial origin.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Возраст · обязательный выбор групп
Требование: при отправке игры обязательно выбрать возрастные группы; при необходимости пометить «kids friendly» или «no blood».
Цитата: It is mandatory to select the appropriate age groups for your game, as this will help to define your intended target audience.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Модерация · срок первой проверки
Требование: первичная проверка присланной игры занимает до одной недели.
Цитата: The initial assessment typically takes up to one week
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Витрина · обязательные размеры превью
Требование: обязательны три превью: 512x512, 512x384 и 200x120 px; они идут в каталог, поиск, заставку и на сайты издателей.
Цитата: Developers are required to submit the following thumbnail sizes: 512×512, 512×384 and 200×120
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Витрина · минимум превью и промо-размеры
Требование: нужно минимум три размера превью; опционально — горизонтальные промо 1280x550 и 1280x720 px.
Цитата: Minimum of three different sizes of thumbnails.
Цитата: Landscape promo sizes: 1280x550px and 1280x720px
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · качество превью
Требование: превью должно отражать игру, быть резким, без растяжения, с читаемым логотипом; логотип и текст необязательны, но не должны доминировать.
Цитата: The eye catcher must be of sharp quality (it’s the focus, so it should not be blurry).
Цитата: Make sure the logo is clearly legible.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · превью 200x120
Требование: на маленьком превью 200x120 не нужны мелкие детали — выбери крупные акценты, определяющие игру.
Цитата: Do not use small details as this will be barely visible.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · название на превью
Требование: название игры лучше ставить только на превью 1280, а не на 512 — там мало места.
Цитата: we would strongly advise only putting it on the 1280s as on the 512s sizes, the space is limited.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · кнопки и UI на превью
Требование: не добавляй на превью CTA-кнопки и элементы интерфейса — их трудно масштабировать для издателей.
Цитата: Try avoiding adding (CTA) buttons and UI elements on the design, it could be difficult to resize the thumbnails for publishers.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · мгновенный отказ по арту
Требование: арт с чужим IP, растянутыми или сжатыми элементами, только логотипом/текстом сразу отклоняется (похожие на оригинал, но заметно изменённые образы допустимы).
Цитата: we immediately decline games if the art includes elements from the list below;
Цитата: Copyright art or IP infringement
Цитата: Squeezed or stretched images/elements that are out of proportions;
Цитата: Only showing the game logo or text;
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · отказ: рамки, обрезка, клик-бейт
Требование: отклоняют арт с белыми рамками по краям, обрезанными названиями и персонажами, дубликат арта чужой игры GD, а также слишком вводящий в заблуждение или кликбейтный.
Цитата: White borders/lines on the sides of the thumbnails, unless clearly part of the design;
Цитата: Cropped off titles and characters;
Цитата: Duplicated art of an existing game on GameDistribution;
Цитата: It is too misleading or includes unnecessary clickbait elements.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · значок мультиплеера на превью
Требование: значок онлайн-игры на превью допустим только для настоящего мультиплеера.
Цитата: Only include this if the game is real multiplayer.
Источник: https://static.gamedistribution.com/developer/design-guidelines.html
Сверено: 2026-10-15

## Витрина · уникальность названия
Требование: название игры должно быть уникальным; прямое дублирование существующих названий недопустимо.
Цитата: it is crucial that game titles remain distinct.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Витрина · описание и инструкция
Требование: описание и инструкции — по 200–500 символов каждое; в описании хотя бы раз точное название игры; вместо «Mouse»/«Keyboard» нужны конкретные пояснения управления.
Цитата: The text for description and instructions should be between 200 and 500 characters each.
Цитата: In the description, use the game name (exactly as it is written in the title) at least once.
Цитата: Avoid using minimal descriptions such as
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Витрина · жанры и теги
Требование: минимум один жанр и один тег, максимум два жанра и пять тегов.
Цитата: Games should have a minimum of one genre and one tag, and a maximum of two genres and five tags.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Ссылки · исходящие ссылки запрещены
Требование: игра не должна уводить трафик на внешние сайты; запрещены ссылки на соцсети, рекламные страницы, магазины, опросы, партнёрские ссылки и «поделиться».
Цитата: Games are not meant to send traffic to external websites through the use of outgoing links.
Цитата: Links to external social media platforms such as Facebook, X,
Цитата: Links for sharing game content or achievements on external platforms.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Ссылки · брендинг и контакты в игре
Требование: логотип разработчика можно показывать на загрузке, в меню или кредитах, но без кликабельных ссылок, контактов и соцсетей.
Цитата: any branding elements within the game must not refer the player to an external site, as clickable outgoing links are not permitted.
Цитата: Please do not include any contact details or referrals to social media pages within the game.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Ссылки · ссылки на сторы
Требование: ссылки на AppStore/PlayStore внутри игры запрещены (их можно дать во вкладке Backlinks на странице игры в каталоге).
Цитата: References to your game’s AppStore or PlayStore are not permitted within the game itself.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Прочее · сбор данных и трекеры
Требование: сбор и хранение данных игры запрещены; чужие cookies и трекеры (Google Analytics, Facebook Pixel, Mixpanel и т. п.) не допускаются.
Цитата: Any collection or storing of data from a game is strictly prohibited.
Цитата: any types of cookies or trackers that are not directly from GD will not be permitted.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15

## Авторизация · вход запрещён
Требование: обязательный вход в игру не разрешён, кроме случаев отдельного соглашения с GD.
Цитата: Login requirements are not permitted unless permission is granted for this under a separate agreement.
Источник: https://static.gamedistribution.com/developer/developers-guidelines.html
Сверено: 2026-10-15
