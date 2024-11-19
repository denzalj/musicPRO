import telebot
import yt_dlp
import os
import time
import glob
bot = telebot.TeleBot("956283069:AAGaXF-cnJBr-yJ8TLMGoH_6av8ugpDOrF8")
historyOfSearch = ["started"]
import os
import yt_dlp

def search_videos(name):
    """Search for videos by name and return a list of video URLs."""
    output_path = "C:\\MusicPRO\\"
    ydl_opts = {
        'default_search': 'ytsearch',
        'max_downloads': 1,
        'format': 'bestaudio/best',
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    results = ydl.extract_info(name, download=False)

    video_urls = []
    
    if 'entries' in results:
        # Process search results
        for entry in results['entries']:
            video_urls.append(entry['webpage_url'])
    else:
        # Process single result
        video_urls.append(results['webpage_url'])

    return video_urls

def download_video(video_url):
    """Download the video from the provided URL."""
    output_path = "C:\\MusicPRO\\"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.webm'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Specify mp3 format
            'preferredquality': '128',  # Specify medium quality (128 kbps)
        }],
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    try:
        ydl.download([video_url])
        filename = ydl.prepare_filename({'webpage_url': video_url})  # Get the filename after download
        return filename  # Return the filename as a string
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


# Инициализация бота
bot = telebot.TeleBot('956283069:AAHZokLFUJ3LBxlEO0Jo11WGkp2IG7VcbVk')

# Список для хранения истории поиска
historyOfSearch = ["started"]

@bot.message_handler(commands=["find"])
def handle_find(message):
    try:
        # Разделение текста команды по первому пробелу
        command_text = " ".join(message.text.split()[1:])
        historyOfSearch.append(command_text)  # Добавление запроса в историю
        bot.send_message(message.chat.id, search_videos(command_text))
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для поиска.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
@bot.message_handler(commands=["download"])
def handle_download(message):
    # Проверяем, есть ли аргументы после команды
    if len(message.text.split()) > 1:
        # Извлекаем аргументы (все слова после команды)
        video_url = " ".join(message.text.split()[1:])  # Объединяем все части сообщения после команды
        try:
            download_video(video_url)  # Вызов функции загрузки видео с переданным URL
            bot.send_message(message.chat.id, "Загрузка видео начата.")  # Сообщение об успешном начале загрузки
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при загрузке видео: {e}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите URL видео для загрузки.")
@bot.message_handler(command=['historyOfSearch'])
def handle_history(message):
    # Формирование текста для отправки
    history_message = "\n".join(historyOfSearch)  # Объединяем историю в одну строку с переносами

    # Отправка истории поиска пользователю
    bot.send_message(message.chat.id, f"История поиска:\n{history_message}")

# Запуск бота
bot.polling()