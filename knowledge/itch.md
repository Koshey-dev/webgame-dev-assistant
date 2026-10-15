# itch.io

## Билд · ZIP с index.html
Требование: игра из нескольких файлов загружается ZIP-архивом, в котором обязательно есть index.html (точка входа), имена файлов чувствительны к регистру.
Цитата: If your game is more than a single file, it must be uploaded as a ZIP file.
Цитата: The ZIP file must contain a file called index.html
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · одиночный HTML-файл
Требование: игру из одного самодостаточного .html можно загружать без архива, но она не сможет ссылаться на другие загруженные файлы.
Цитата: Your page will not be able to reference any other files you've uploaded on itch.io page.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · только ZIP, без rar и 7z
Требование: другие архивы (.rar, .tar.gz, .7z) не поддерживаются, а отдельные файлы по одному загружать нельзя — только ZIP.
Цитата: We do not support any other archive types, (.rar,.tar.gz, and .7z are not supported).
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · лимит числа файлов в ZIP
Требование: в ZIP после распаковки должно быть не более 1000 файлов.
Цитата: The ZIP file should not contain more than 1,000 individual files after extraction.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · длина имени файла
Требование: длина имени файла вместе с путём — не более 240 символов.
Цитата: The maximum length of a file name including path should not be greater than 240 characters long.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · размер распакованной игры
Требование: суммарный размер распакованного содержимого — не более 500 МБ, один файл — не более 200 МБ.
Цитата: The size of all the extracted content should not be greater than 500MB.
Цитата: The size any single extracted file should not be greater than 200MB.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · кодировка и регистр имён
Требование: имена файлов чувствительны к регистру и должны быть в кодировке UTF-8.
Цитата: The filenames are case sensitive and should be encoded as UTF-8
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · относительные пути
Требование: пути к ресурсам только относительные: абсолютные (начинающиеся с /) ломаются, т. к. игра лежит в подкаталоге CDN.
Цитата: You must use relative paths to access other files you have provided in your project.
Цитата: Absolute paths are paths that start with a /.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · регистр в ссылках на файлы
Требование: ссылки на файлы должны совпадать по регистру с именами (Hello.png, а не hello.png): сервер чувствителен к регистру, локально на Windows и macOS это может работать, а после загрузки давать 403.
Цитата: The server that hosts your project’s files is case-sensitive.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · внешние ресурсы только по HTTPS
Требование: любые внешние файлы и API должны запрашиваться по HTTPS, исключений нет.
Цитата: then that domain must be requested with HTTPS.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · запросы к папкам дают 403
Требование: нельзя обращаться к папке (путь с / на конце) вместо файла — вернётся 403, а не 404.
Цитата: This includes attempting to access a folder (paths ending in /) instead of a specific file.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · сжатие .br и .gz
Требование: файлы с расширением .br сервер считает сжатыми Brotli (так делает Unity 2020 WebGL), а gzip определяется по содержимому; тип содержимого берётся по расширению без .gz/.br.
Цитата: If the filename ends with the extension .br then we'll assume that the content is Brotli compressed
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · автосжатие CDN
Требование: CDN сам применяет GZIP к несжатым файлам html, js, css, svg, wasm, wav, glb, pck.
Цитата: itch.io’s CDN will automatically apply GZIP compression to the following file types if they are provided uncompressed.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · крупные игры лучше скачиваемыми
Требование: очень большие HTML5-игры хуже по загрузке и производительности; для больших проектов лучше скачиваемая версия, лимиты можно снять по запросу.
Цитата: For larger games, it’s often better to go for a downloadable version.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Билд · адаптивный canvas
Требование: игру лучше экспортировать с шаблоном, где canvas подстраивается под размер окна.
Цитата: we recommend using a template or markup that allows for your game’s canvas to adjust to the size of the window is is placed in.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Витрина · режимы встраивания
Требование: игра показывается либо встроенной на странице (нужно задать размеры окна), либо по клику на весь экран (размеры не нужны, код должен подстраиваться под размер).
Цитата: Embed in page — You provide the dimensions of the viewport, and the game will run directly on the page
Цитата: The code you provide should be able to adapt to various sizes.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Загрузка · Click to Play по умолчанию
Требование: по умолчанию игра стартует по клику; автозапуск при загрузке страницы стоит включать только для лёгких проектов.
Цитата: By default your project will require a click to start.
Цитата: If you have a lightweight project, you can disable Click to play and your project will start when the page loads.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Звук · автозапуск и звук
Требование: при автозапуске звук в некоторых браузерах может быть заглушён.
Цитата: Keep in mind audio may be muted on some browsers when using auto-start.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Устройства · флажок Mobile Friendly
Требование: если игра работает в мобильном браузере, включи Mobile Friendly; иначе зрителю покажут предупреждение, что игра может не работать.
Цитата: If you know your project functions in a mobile browser then you can select the Mobile Friendly option in the embed settings for your project.
Цитата: If you haven’t enabled Mobile Friendly then a warning will be displayed to the viewer that the game may not work
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Устройства · мобильный запуск на весь экран
Требование: на телефоне страница всегда использует режим «на весь экран по клику», независимо от настроек для десктопа.
Цитата: it will use Click to launch in fullscreen mode regardless of how you've configured your embed for desktop computers.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Покупки · HTML5-игры только за донаты
Требование: в HTML5-играх на itch.io платежи возможны только как донаты; чтобы продавать доступ, нужно поставить тип «Downloadable».
Цитата: Currently all HTML5 games on itch.io are set up to only take payments as donations.
Цитата: it’s possible to sell access to your game by setting its “Kind of Game” to “Downloadable”.
Источник: https://itch.io/docs/creators/html5
Сверено: 2026-10-15

## Загрузка · лимиты страниц и файлов
Требование: у новых аккаунтов мягкий лимит 20 страниц проектов и не более 10 файлов на страницу; размер файла ограничен, лимиты снимаются по запросу.
Цитата: There is a soft limit of 20 project pages.
Цитата: Individual file size is limited, and you should have 10 files max per page.
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Контент · сексуальный контент
Требование: нельзя размещать сексуализированные фото и видео реальных людей, в том числе ИИ-изображения, похожие на фото реальных людей; вымышленный и нарисованный контент в целом допустим, если он законен.
Цитата: We don’t allow hosting content that includes sexualized images or videos of real-life humans.
Цитата: AI-generated imagery that is designed to resemble photographic content of real people is not allowed.
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Контент · запрещённые темы платёжных систем
Требование: при приёме денег действуют правила платёжных систем (PayPal, Stripe, Payoneer); нельзя продавать контент с темами вроде принуждения, несовершеннолетних, инцеста и т. п.
Цитата: If you plan to collect money for your content, then you must adhere to the acceptable use policy of all respective payment processors that your account utilizes:
Цитата: Underage or “barely legal” themes
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Модерация · нарушения 18+ без апелляции
Требование: нарушения политики, повлёкшие административные меры, необратимы, деньги на аккаунте не выплачиваются.
Цитата: Violations that result in administrative action are permanent with no chance of appeal.
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Прочее · данные покупателей
Требование: личные данные покупателей (email, имя, IP, страна, ID транзакций) нельзя публиковать и передавать третьим лицам; подписывать на рассылку можно только с явного согласия.
Цитата: Sharing private, identifiable information that itch.io collects about buyers is a violation of our privacy policy.
Цитата: Do not automatically sign people up for mailing lists.
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Витрина · кастомный CSS
Требование: свой CSS на страницах отключён по умолчанию и выдаётся по заявке после ручного одобрения; сначала используй встроенный редактор тем.
Цитата: but it’s disabled by default.
Цитата: We manually approve accounts for CSS
Источник: https://itch.io/docs/creators/faq
Сверено: 2026-10-15

## Модерация · последствия нарушений правил качества
Требование: за нарушение гайдлайнов качества страницу могут убрать из индекса поиска и рекомендаций (по прямой ссылке она останется доступной).
Цитата: our systems or a site moderator may choose to remove your page from itch.io’s discovery index.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · публикуй страницу готовой
Требование: делай страницу публичной, когда готовы все изображения, файлы и классификации: в список «Most Recent» страница попадает один раз.
Цитата: When you decide to make your page public it should be ready for everyone to see.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · платформы только реальные
Требование: платформу (Windows, Linux, Mac, Android) отмечай только если есть исполняемая программа под неё; для html-игр не отмечай все платформы.
Цитата: Do not select a platform (Windows, Linux, MacOS, Android, etc.) unless you have a program that runs directly on the respective operating system or device.
Цитата: If you're uploading a rom, project file, save state, mod, html file, or other non-executable software, don’t select all platforms
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · метаданные без лишних категорий
Требование: не добавляй нерелевантные классификации, теги, движки; если выбраны все подряд, страницу могут счесть спамом и ограничить.
Цитата: If you intentionally add every classification, we may identify your page as spam and restrict access to your project pages.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · правила для тегов
Требование: выбирай подсказанные теги, не дублируй классификации из метаданных (например multiplayer), не используй синонимы и название проекта как тег.
Цитата: Prefer using a suggested tag over creating a new one.
Цитата: Avoid using tag synonyms.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · не пересоздавай страницу ради буста
Требование: нельзя пересоздавать страницу с тем же содержимым ради видимости: рейтинги, коллекции и библиотеки пользователей не переносятся, аккаунт могут лишить доступа к рекомендациям.
Цитата: Recreating pages with identical or nearly identical content in an attempt to increase visibility or traffic is against our guidelines.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Возраст · разметка контента 18+
Требование: страницы с сильными взрослыми темами нужно пометить в Metadata » Classification; откровенные изображения в обложке не используй.
Цитата: If you have a project page that has strong adult themes, then it must be marked.
Цитата: avoid using explicit images as your cover image.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · обложка
Требование: у проекта должна быть обложка (можно GIF); анимированная обложка не должна вызывать приступов по стандартам WCAG.
Цитата: The cover image is typically the first element someone sees when they discover your game on our browse pages.
Цитата: please ensure it doesn’t have seizure-inducing effects as per the Web Content Accessibility Guidelines.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · скриншоты
Требование: скриншоты рекомендованы даже для встроенной браузерной игры; для чисто текстовых проектов необязательны.
Цитата: Even if your project is an embedded browser game, it’s recommended to provide screenshots.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Язык · не отмечай все языки
Требование: если в проекте нет текста и речи, не выбирай все языки, а используй классификацию доступности «No text»; ложный выбор языков может привести к удалению из выдачи.
Цитата: Instead, please utilize the relevant Accessibility classifications, such as No text.
Цитата: Misusing the language options may result in your page being delisted.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Витрина · не вводи в заблуждение
Требование: описание и изображения должны точно отражать проект; фейковые картинки, несуществующие функции и чужие ассеты вместо своих запрещены.
Цитата: Fake or misleading imagery regarding your project and the functionality it provides
Цитата: Using assets from other products or services to represent your own
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Контент · имитация чужих брендов
Требование: нельзя выдавать себя за других авторов и компании: похожие названия, логотипы, внешний вид и функционал без разрешения запрещены.
Цитата: Impersonating other creators or companies by uploading content that is confusingly similar to theirs is strictly prohibited.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Покупки · азартные игры на деньги
Требование: нельзя предлагать заработок за «вход» зрителя: токены и цифровые товары за денежные призы, инвестиции, конкурсы с денежным призом для покупателей.
Цитата: Buying tokens or other kinds of digital goods to redeem monetary or equivalent prizes
Цитата: Contests that include a cash prize for buyers of your page
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Контент · рескины
Требование: не создавай несколько страниц для практически одинаковых проектов с мелкими правками; существенные изменения и версии вроде jam и final допустимы.
Цитата: Do not create multiple project pages for projects that are essentially the same but have only minor adjustments.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Контент · массовый ИИ-контент
Требование: нельзя массово плодить страницы автоматически или ИИ-сгенерированным контентом; такое сочтут спамом и уберут из поиска.
Цитата: do not use automated systems to mass produce product pages.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Контент · пометка генеративного ИИ
Требование: если в проекте есть материалы генеративного ИИ, отметь их в разделе AI Disclosure; обычный игровой ИИ (поиск пути, процедурная генерация и т. п.) помечать не нужно.
Цитата: We ask that you accurately tag your project if it contains materials produced by generative AI by utilizing the AI Disclosure section on your project’s edit page.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Загрузка · файлы прямо на itch.io
Требование: загружай файлы прямо на itch.io, не через сторонние сервисы и внешние ссылки; одни ключи Steam или ссылка на другой магазин без файлов нежелательны.
Цитата: Avoid using third-party download services or links to other platforms that the end-user must go through to access your project’s files.
Цитата: Please try not to upload just Steam keys, or put a link to your Steam store page without uploading any files.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Реклама · навязчивая реклама
Требование: лучше без рекламы; если она есть, она не должна быть навязчивой или обманной и не должна мешать играть без лишних действий.
Цитата: Avoid sponsored installers, or ads that prevent someone from playing the game without performing some action.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Авторизация · сторонний вход
Требование: не ставь вход через сторонний сервис перед игрой без необходимости и не используй его ради сбора личных данных или перенаправления трафика.
Цитата: Please avoid putting third-party login walls in front of your game unless necessary.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Модерация · вредоносное ПО
Требование: проекты с malware, spyware и adware запрещены и банятся; это включает установщики, ставящие рекламу в ОС или браузер.
Цитата: Any projects that contain malware, spyware or adware are prohibited and will be banned from our platform.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Контент · шок и мигание
Требование: проекты, построенные на шоковых образах, мигающих цветах и раздражающих звуках, могут быть исключены из каталога и поиска.
Цитата: or other material that is designed to be obnoxious then we may delist from our browse and search pages.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Покупки · постоянная распродажа
Требование: проект не должен быть на распродаже постоянно, а цену нельзя искусственно менять перед скидкой; исключение — скидка на бандл.
Цитата: If your game is perpetually on sale, then it isn’t genuinely on sale.
Цитата: Do not alter the base price of your product, then apply a sale to bring your product back to its original price
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15

## Прочее · реклама игры в сообществе
Требование: свои проекты анонсируй только на доске Release announcements; реклама в чужих комментариях и сообществах считается спамом.
Цитата: Unless your project is relevant to the other one, do not post advertisements on other communities.
Источник: https://itch.io/docs/creators/quality-guidelines
Сверено: 2026-10-15
