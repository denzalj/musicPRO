import telebot
import yt_dlp
import os
import time
import glob
bot = telebot.TeleBot("956283069:AAGaXF-cnJBr-yJ8TLMGoH_6av8ugpDOrF8")
def findYT(name):
    try:
        output_path="C:\\MusicPRO\\"
        ydl_opts = {
    'default_search': 'ytsearch',
    'max_downloads': 1,
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_path, '%(title)s.webm'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',  # Указываем формат mp3
        'preferredquality': '128',  # Указываем среднее качество (128 kbps)
    }],
}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        results = ydl.extract_info(name, download=False)

        if 'entries' in results:
    # Обработка результатов поиска
            for entry in results['entries']:
                video_url = entry['webpage_url']
                print(video_url)
        else:
    # Обработка результата запроса
            video_url = results['webpage_url']
            print(video_url)
        ydl.download([video_url])
        filename = ydl.prepare_filename(results)  # Получаем имя файла после загрузки
        return filename  # Возвращаем строку с названием файла    
    except:
        pass
    finally:
        pass

# Создайте экземпляр бота с вашим токеном
bot = telebot.TeleBot('956283069:AAHZokLFUJ3LBxlEO0Jo11WGkp2IG7VcbVk')

@bot.message_handler(commands=['find'])
def handle_send_file(message):
    try:
        # Разделение текста команды по первому пробелу
        command_text = message.text.split(' ', 1)[1]
        # Обработка текста команды (предполагается, что findYT - это ваша функция)
        folder_path = "C:\\MusicPRO\\"+findYT(command_text) # Укажите путь к вашей папке
            # Отправка файла пользователю
        with open(folder_path, "rb") as file:
            bot.send_document(message.chat.id, file)
            # Удаление файла после отправки
            os.remove(folder_path)

    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите текст для поиска.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Запуск бота
bot.polling()