#Импорт для дисплея
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

font20 = ImageFont.truetype("Roboto-Regular.ttf", 15, encoding='UTF-8')
#font20 = ImageFont.truetype("arial.ttf", 20)
#Ипорт для бота
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import code

#БОТ------------------------------------------



BOT_TOKEN = "7620403422:AAHHZO5zq4qV5azEYmWWeoUtCD3sEik4rsc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_message = None  # Вынесено из обработчика для ясности


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне сообщение, я буду отображать их на экране.")


@dp.message()
async def handle_message(message: Message):
    global last_message
    try:
        last_message = message.text

        # Запись в файл (относительный путь)
        with open("save.txt", "w", encoding="utf-8") as file:
            file.write(last_message)
            print(last_message)


             # Drawing on the image
             #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
            logging.info("epd2in13b_V4 Demo")
            epd = epd2in13b_V4.EPD()
            logging.info("init and Clear")
            epd.init()
            epd.Clear()
            time.sleep(1)
    
            print(last_message)
            logging.info("1.Drawing on the Horizontal image...") 
            HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
            HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
            drawblack = ImageDraw.Draw(HBlackimage)
            drawry = ImageDraw.Draw(HRYimage)
            drawblack.text((20, 10), last_message, font = font20, fill = 0)
    #drawblack.text((10, 40), '2.13inch e-Paper b V4', font = font20, fill = 0)
    #drawblack.text((120, 0), u'HELO NIGEET', font = font20, fill = 0)    
    
    #drawblack.line((60, 50, 70, 150), fill = 0)
    #drawblack.line((70, 50, 40, 100), fill = 0)
    
    #drawblack.rectangle((60, 70, 90, 100), outline = 0 )    
    #drawblack.triangle((70, 80, 90, 100, 75, 70), outline =0)

   
            epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
            time.sleep(2)

        await message.answer(
            f"✅ Сообщение сохранено! Текущее значение: {last_message}"
        )

    except Exception as e:
        print(f"Error: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке сообщения")


async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
