# Article

## Описание
Телеграм бот, который запоминает ссылки, которые ему присылают пользователи и отдает их по запросу. 
Для начала взаимодействия с ботом необходимо ввести команду "/start".
## Функционал
```
Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете :)
- Чтобы я запомнил статью, достаточно передать мне ссылку на нее. К примеру https://example.com
- Если нужно отправить несколько ссылок сразу, необходимо разделять их пробелом.
К примеру https://example1.com https://example2.com.
- Чтобы получить случайную статью, достаточно передать мне команду /get_article.
- Но помни! Отдавая статью тебе на прочтение, она больше не хранится в моей базе.Так что тебе точно нужно её изучить
```
## Ссылка на бота 
https://t.me/storing_links_bot
## Установка ПО для запуска бота
1. Установите интерпретатор python версии 3.11.
2. Клонируйте репозиторий.
3. Создайте виртуальное окружение c помощью команды:
```
-python -m venv {venv name}
```
4.1 Активируйте его для Windows с помощью команды:
```
-venv\Scripts\activate.bat
```
4.2 Или для MacOS и Linux с помощью команды:
```
-source venv/bin/activate
```
5. Установите необходимые библиотеки из файла requirements.txt с помощью команды:
```
-pip install -r requirements.txt
```
6. Зарегестрировать своего бота в телеграм https://t.me/BotFather.
7. Вставьте свой TOKEN вместо `"your_token"` в файле main.py.
8. Запустите программу с помощью командной строки:
```
python main.py 
```
