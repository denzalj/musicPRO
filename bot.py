import telebot
import yt_dlp
import os
from yt_dlp import YoutubeDL
from telebot import types
import zipfile

def search_channels(name):
    """Search for videos by name and return a list of tuples (video title, channel URL)."""
    ydl_opts = {
        'extract_flat': True,  # Extract only links without downloading
        'default_search': 'ytsearch10:',  # Set search to YouTube and number of results
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    results = ydl.extract_info(f"ytsearch10:{name}", download=False)  # Use ytsearch for searching

    channel_pairs = ""

    if 'entries' in results:
        # Process search results
        for entry in results['entries']:
            channel_pairs=channel_pairs+entry['channel']+ entry['channel_url']+"\n" # Append title and channel URL
    else:
        # Process single result
        channel_pairs=channel_pairs+results['channel'] + results['channel_url']+"\n"  # Append title and channel URL

    return channel_pairs
def get_channel_videos(channel_url: str) -> str:
    options = {
        'extract_flat': True,  # Извлекаем только ссылки без загрузки
    }
    video_pairs = ""
    
    with YoutubeDL(options) as ydl:
        results = ydl.extract_info(channel_url, download=False)
        
        if 'entries' in results:
            # Обрабатываем результаты поиска
            for i in range(min(10, len(results['entries']))):  # Ограничиваем до 10 элементов
                entry = results['entries'][i]  # Получаем элемент из 'entries'
                title = entry.get('title', 'Нет названия')
                url = entry.get('url')
                video_pairs += f"{title}\n{url}\n"
        else:
            # Обрабатываем единственный результат
            title = results.get('title', 'Нет названия')
            url = results.get('webpage_url', 'Нет URL')
            video_pairs += f"{title}\n{url}\n"
    
    return video_pairs
def search_videos(name):
    """Search for videos by name and return a list of tuples (video title, video URL)."""
    ydl_opts = {
               'extract_flat': True,  # Извлекаем только ссылки без загрузки
        'default_search': 'ytsearch10:',  # Устанавливаем поиск по YouTube и количество результатов
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    results = ydl.extract_info(f"ytsearch10:{name}", download=False)  # Используем ytsearch для поиска

    video_pairs = ""
    
    if 'entries' in results:
        # Обрабатываем результаты поиска
        for entry in results['entries']:
            video_pairs =video_pairs+ entry['title']+"\n" +  (entry['url']) +"\n"
    else:
        # Обрабатываем единственный результат
        video_pairs= video_pairs + results['title']+"\n"+ ( results['url'])+"\n"


    return video_pairs
def download_video(video_url):
    """Download the video from the provided URL and return its filename with path."""
    output_path = "C:\\MusicPRO\\"
    ydl_opts = {
    'quiet': True,  # Отключить вывод сообщений
    'format': 'bestaudio/best',  # Скачивание видео среднего качества (360p)
    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Установить шаблон имени файла
}
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    try:
        # Download the video
        ydl.download([video_url])
        
        # Prepare filename after download
        info_dict = ydl.extract_info(video_url, download=False)  # Extract info without downloading again
        filename = os.path.join(output_path, f"{info_dict['title']}.{info_dict['ext']}")  # Construct full path
        file_size = os.path.getsize(filename) /1024/1024
        print(file_size)
        if (file_size>50):
            print("go")
            zip_file_name=filename[0:len(filename)-3]+"zip"
            with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(filename, os.path.basename(filename))
                filename=zip_file_name
        print(filename)
        return filename  # Return the full path of the downloaded file
    except Exception as e:
        print(f"Error downloading video: {e}")
        return filename
bot = telebot.TeleBot('956283069:AAHZokLFUJ3LBxlEO0Jo11WGkp2IG7VcbVk')
historyOfSearch = ["started"]
@bot.message_handler(commands=["fromchannel"])
def handle_find(message):
    try:
        # Разделение текста команды по первому пробелу
        command_text = " ".join(message.text.split()[1:])
        historyOfSearch.append(command_text)  # Добавление запроса в историю
        bot.send_message(message.chat.id, get_channel_videos(command_text)[0:])
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для поиска.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
@bot.message_handler(commands=["find"])
def handle_find(message):
    try:
        # Разделение текста команды по первому пробелу
        command_text = " ".join(message.text.split()[1:])
        historyOfSearch.append(command_text)  # Добавление запроса в историю
        
        # Получение результатов поиска
        search_results = search_videos(command_text)
        
        if not search_results:
            bot.send_message(message.chat.id, "Ничего не найдено.")
            return
        # Создание инлайн-кнопок
        markup = types.InlineKeyboardMarkup(row_width=3)
        x = 0
        res =search_videos(command_text)[0:]
        for result in range(1,11):
            button = types.InlineKeyboardButton(text=result, callback_data=res.split('\n')[result*2-1])
            print(res.split('\n')[result*2-1])
            x+=1
            markup.add(button)
        
        # Отправка сообщения с кнопками
        bot.send_message(message.chat.id, "Вот результаты поиска:"+res, reply_markup=markup)
        
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для поиска.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if len(call.data.split()) > 1:
        # Извлекаем аргументы (все слова после команды)
        video_url = " ".join(call.data)  # Объединяем все части сообщения после команды
        try:
            download_video(video_url)  # Вызов функции загрузки видео с переданным URL
            bot.send_message(call.message.chat.id, "Загрузка видео начата.")  # Сообщение об успешном начале загрузки
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Произошла ошибка при загрузке видео: {e}")
    else:
        bot.send_message(call.message.chat.id, "Пожалуйста, укажите URL видео для загрузки.")
@bot.message_handler(commands=["download"])
def handle_download(message):
    # Проверяем, есть ли аргументы после команды
    if len(message.text.split()) > 1:
        # Извлекаем аргументы (все слова после команды)
        video_url = " ".join(message.text.split()[1:])  # Объединяем все части сообщения после команды
        try:
            filename = download_video(video_url)  # Вызов функции загрузки видео с переданным URL
            with open(filename, 'rb') as file:
                bot.send_video(message.chat.id, file)        
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
@bot.message_handler(commands=["findchannel"])
def handle_find(message):
    try:
        # Разделение текста команды по первому пробелу
        command_text = " ".join(message.text.split()[1:])
        historyOfSearch.append(command_text)  # Добавление запроса в историю
        bot.send_message(message.chat.id, search_channels(command_text)[0:])
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для поиска.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
# Запуск бота
bot.polling()