from pyrogram import Client, filters
from google_translator_manager import GoogleTranslator # Класс с функцией перевода текста
from config import API_ID, API_HASH # Данные юзера, что можно получить на https://my.telegram.org/
import re

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.text)
async def answer(client, message):
    async def message_editing(sl, tl): # Функция для перевода принимающая source_language и target_language
        translation = GoogleTranslator.translate(message.text.replace(f'[{tl}]', ''), sl, tl)
        translation = translation.replace('"', '')
        
        splitted_translation = re.findall(r'\S+|\s+', translation)
        new_message = ''
        for word in splitted_translation:
            try:
                new_message += f'{word}'
                await app.edit_message_text(message.chat.id, message.id, new_message)
            except:
                continue
            
    match message.text: # Ловим что в конце сообщения
        case text if text.endswith('[en]'):
            await message_editing('ru', 'en')
        case text if text.endswith('[ru]'):
            await message_editing('en', 'ru')

app.run()