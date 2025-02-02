import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from PIL import Image, ImageDraw, ImageFont

# Импорт для дисплея
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13b_V4

# Настройка шрифтов
font17 = ImageFont.truetype("Roboto-Regular.ttf", 17, encoding='UTF-8')
font14 = ImageFont.truetype("Roboto-Regular.ttf", 14, encoding='UTF-8')

# Настройка бота
BOT_TOKEN = "ВАШ_ТОКЕН"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Глобальные переменные
max_length = 19  # Максимальная длина строки
last_message = None

# Функция для разбиения текста на строки
def split_text(text, max_length):
    words = text.split()  # Разделяем текст на слова
    lines = []
    current_line = ""

    for word in words:
        # Если добавление нового слова превысит максимальную длину строки
        if len(current_line) + len(word) + 1 > max_length:
            lines.append(current_line)  # Добавляем текущую строку в список
            current_line = word  # Начинаем новую строку с текущего слова
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word

    if current_line:  # Добавляем последнюю строку, если она не пустая
        lines.append(current_line)

    return lines  # Возвращаем список строк

# /start
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне сообщение, и я его выведу на экран.")

# Обработчик всех сообщений
@dp.message()
async def handle_message(message: Message):
    global last_message
    try:
        last_message = message.text

        # Запись в файл 
        with open("save.txt", "w", encoding="utf-8") as file:
            file.write(last_message)
            print(last_message, message.from_user.full_name)

        # Разбиваем текст на строки
        lines = split_text(last_message, max_length)
        formatted_text = "\n".join(lines)  # Объединяем строки для вывода

        # Логика для EPD-дисплея
        logging.info("epd2in13b_V4 Demo")
        epd = epd2in13b_V4.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)

        logging.info("1.Drawing on the Horizontal image...")
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
        HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)

        # Отображение имени пользователя
        drawblack.text((15, 5), f"{message.from_user.full_name}", font=font17, fill=0)

        # Отображение текста с переносами
        y_offset = 30  # Начальное смещение по вертикали
        for line in lines:
            drawblack.text((10, y_offset), line, font=font14, fill=0)
            y_offset += 20  # Увеличиваем смещение для следующей строки

        # Вывод на дисплей
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        time.sleep(2)

        # Ответ пользователю
        await message.answer(f"✅ Сообщение сохранено! Текущее значение:\n{formatted_text}", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        print(f"Error: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке сообщения")

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
