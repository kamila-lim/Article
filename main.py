import sqlite3
import telebot
import os

# Создайте экземпляр бота
bot = telebot.TeleBot("6704047022:AAERXtFhexXR_Gu3lgxo3SR_PP2qiBEEPzo")

# Создание таблицы в базе данных, если она не существует
def create_articles_table() -> None:
    conn = sqlite3.connect("links.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            article_url TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
    """)
    conn.commit()
    c.close()
    conn.close()
create_articles_table()

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете :)\n\n"
                                      "- Чтобы я запомнил статью, достаточно передать мне ссылку на нее. К примеру https://example.com.\n\n"
                                      "- Если нужно отправить несколько ссылок сразу, необходимо разделять их пробелом.\n "
                                      "К примеру https://example1.com https://example2.com.\n\n"
                                      "- Чтобы получить случайную статью, достаточно передать мне команду /get_article.\n\n"
                                      "Но помни, отдавая статью тебе на прочтения, она больше не хранится в моей базе. Так что тебе точно нужно ее изучить!")

# Обработка команды /get_article
@bot.message_handler(commands=['get_article'])
def get_article(message: telebot.types.Message) -> None:
    user_id = message.from_user.id
    try:
        # Подключение к базе данных
        conn = sqlite3.connect("links.db")
        c = conn.cursor()
        # Выполнение запроса к базе данных для получения случайной статьи
        c.execute("SELECT article_url FROM articles WHERE user_id = ? ORDER BY RANDOM() LIMIT 1;", (user_id,))
        article = c.fetchone()
        if article:
            # Отправка сообщения с найденной статьей
            bot.send_message(message.chat.id, f"Вы хотели прочитать: {article[0]}\nСамое время это сделать!")
            # Удаление ссылки из базы данных после отправки пользователю
            c.execute("DELETE FROM articles WHERE user_id = ? AND article_url = ?;", (user_id, article[0]))
            conn.commit()
        else:
            bot.send_message(message.chat.id, "У вас пока нет сохраненных статей.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении статьи:)")
    finally:
        # Закрываем соединение с базой данных
        c.close()
        conn.close()

# Функция для сохранения статьи в базу данных
@bot.message_handler(func=lambda message: message.text.startswith('http'))
def save_article(message: telebot.types.Message) -> None:
    user_id = message.from_user.id
    article_urls = message.text.split()  # Разделить сообщение по пробелам, чтобы получить список ссылок

    try:
        # Подключение к базе данных
        conn = sqlite3.connect("links.db")
        c = conn.cursor()

        for article_url in article_urls:
            # Проверка, есть ли уже такая ссылка в базе данных
            c.execute("SELECT article_url FROM articles WHERE user_id = ? AND article_url = ?;", (user_id, article_url))
            existing_article = c.fetchone()
            if existing_article:
                bot.send_message(message.chat.id, f"Упс, ссылка {article_url} уже сохранена :)")
            else:
                # Если ссылка еще не сохранена, то сохраняем
                c.execute("INSERT INTO articles (article_url, user_id) VALUES (?, ?);", (article_url, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"Сохранил ссылку {article_url}, спасибо!")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при сохранении статьи.")
    finally:
        # Закрываем соединение с базой данных
        c.close()
        conn.close()

# Обработка неизвестных команд
@bot.message_handler(func=lambda message: True)
def unknown(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Извините, такой команды нет.\n"
                                      "- Чтобы посмотреть доступные команды, достаточно передать мне команду /start." )

# Запуск бота
def main() -> None:
    bot.polling()

if __name__ == '__main__':
    main()