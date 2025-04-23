import os
import time
from datetime import datetime
from telethon import TelegramClient, functions
from PIL import Image, ImageDraw, ImageFont

# === Параметры авторизации ===
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('cyberclock_session', api_id, api_hash)

ASSETS_DIR = 'assets'
BACKGROUND_PATH = os.path.join(ASSETS_DIR, 'background.png')
FONT_PATH = os.path.join(ASSETS_DIR, 'orbitron.ttf')
OUTPUT_PATH = 'avatar.png'


def generate_clock_image():
    img = Image.open(BACKGROUND_PATH).convert('RGBA')
    draw = ImageDraw.Draw(img)

    font_size = 130
    font = ImageFont.truetype(FONT_PATH, font_size)

    now = datetime.now()
    time_str = now.strftime('%H:%M')

    # Получаем bounding box текста
    bbox = draw.textbbox((0, 0), time_str, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    img_w, img_h = img.size
    x = (img_w - text_w) / 2
    y = (img_h - text_h) / 2

    draw.text((x, y), time_str, font=font, fill=(0, 255, 255, 255))
    img.save(OUTPUT_PATH)



async def main():
    await client.start()
    print("[✓] Авторизация прошла успешно")

    while True:
        generate_clock_image()
        print("[⏰] Сгенерировано:", datetime.now().strftime('%H:%M'))

        try:
            await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(OUTPUT_PATH)
            ))
            print("[🖼] Аватарка обновлена")
        except Exception as e:
            print("[!] Ошибка при установке аватарки:", e)

        time.sleep(60)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
