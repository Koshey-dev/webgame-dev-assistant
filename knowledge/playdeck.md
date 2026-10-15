# Playdeck (Telegram)

## Билд · вес сборки
Требование: вес сборки должен быть меньше 50 МБ.
Цитата: The build weight is less than 50 Mb
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Game-requirements
Сверено: 2026-10-15

## Загрузка · время загрузки
Требование: игра должна загружаться не дольше 10 секунд.
Цитата: Game loads within 10 seconds
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Game-requirements
Сверено: 2026-10-15

## SDK · обязательные методы и аналитика
Требование: игра обязана реализовать обязательные методы интеграции PlayDeck и иметь включённую внутриигровую аналитику.
Цитата: Game must implement the mandatory methods
Цитата: Game must have in-game analytics enabled
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Game-requirements
Сверено: 2026-10-15

## SDK · сигнал прогресса загрузки
Требование: в начале загрузки нужно передать loading (1), по завершении — loading (100); без сигнала 100% кнопка Play в обёртке не станет активной.
Цитата: At the start of the game loading process, it's essential to transmit loading (1), and similarly, at the end when the game has finished loading (100).
Цитата: If the loading progress reaching 100% is not signaled, the Play button within Wrapper won't become active.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Required-steps
Сверено: 2026-10-15

## Покупки · только Telegram Stars
Требование: внутриигровые платежи разрешены только через Telegram Stars (TG Stars).
Цитата: they must be processed exclusively through TG Stars.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Required-steps
Сверено: 2026-10-15

## Реклама · метод PlayDeck
Требование: если в игре есть реклама, её нужно подключать через метод PlayDeck, указанный в документации.
Цитата: If Game includes ads, they should be implemented using the method available via the link.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Required-steps
Сверено: 2026-10-15

## Язык · локаль пользователя
Требование: рекомендуется выводить интерфейс на языке пользователя: локаль берётся из getUserProfile() или из языка устройства.
Цитата: The game should consider to use correct user locale for rendering proper UI texts.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Highly-recommended-steps
Сверено: 2026-10-15

## Сохранения · облако через setData/getData
Требование: рекомендуется сохранять прогресс и бонусы через setData()/getData() — облачные сохранения и работа на разных устройствах.
Цитата: It can be utilized for cloud saving and cross-device experiences.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Highly-recommended-steps
Сверено: 2026-10-15

## Сохранения · лимит setData
Требование: через setData() можно хранить до 10 КБ данных, длина ключа — не более 50 символов.
Цитата: We have limit for data = 10Kb and key length <= 50 symbols
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Сохранения · ключ в ответе getData
Требование: при нескольких вызовах getData() ответ нужно сопоставлять по полю key в ответе.
Цитата: Each getData() response contains key field according to requested data key
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Авторизация · токен JWT
Требование: подлинность пользователя проверяется через getToken(): токен в формате JWT, его валидируют через API или локально по публичному ключу.
Цитата: It is JWT format of token and you can read more about it and validate over API or inplace with public key
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Прочее · аналитика для лидербордов
Требование: методы маркетинговых инструментов нужны для сбора аналитики, без неё не запустить лидерборды и специальные задания.
Цитата: This methods are necessary to collect game analytics in order to launch leaderboards and special tasks.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/Highly-recommended-steps
Сверено: 2026-10-15

## Прочее · определение запуска в PlayDeck
Требование: при запуске в iframe определить PlayDeck нельзя, но в URL игры передаются параметры telegram=true и playdeck=true — по ним можно понять, что игра стартовала в Telegram.
Цитата: we pass telegram=true and playdeck=true query parameter into every game url
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Загрузка · событие окончания загрузки
Требование: окончание загрузки обёртка сообщает событием loaded.
Цитата: Upon reaching the end of the loading, the Wrapper will fire event loaded.
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Прочее · кеширование в webview
Требование: кеширование данных внутри Telegram webview настраивается HTTP-заголовками Cache-Control.
Цитата: You can control how webview is caching data using Cache-Control http headers
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15

## Прочее · отладка в Telegram
Требование: приложение можно отлаживать через devtools webview в Telegram Desktop.
Цитата: You can debug your app using webview devtools from Telegram Desktop
Источник: https://github.com/ton-play/playdeck-integration-guide/wiki/FAQ
Сверено: 2026-10-15
