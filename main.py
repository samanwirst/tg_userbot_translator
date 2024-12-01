from pyrogram import Client, filters
from google_translator_manager import GoogleTranslator # Класс с функцией перевода текста
from config import API_ID, API_HASH # Данные юзера, что можно получить на https://my.telegram.org/
import re
from translations import TranslationsList

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
remove_symbols = ["«", "»", '"']

@app.on_message(filters.text)
async def answer(client, message):
    async def message_editing(sl, tl): # Функция для перевода принимающая source_language и target_language
        translation = GoogleTranslator.translate(message.text.replace(f'[{tl}]', ''), sl, tl)
        
        for symbol in remove_symbols: # При переводе возвращает ковычки, удаляем их
            translation = translation.replace(symbol, '')
        
        splitted_translation = re.findall(r'\S+|\s+', translation) # Разбиваем текст со словами на массив
        new_message = ''
        for word in splitted_translation:
            try:
                new_message += f'{word}'
                await app.edit_message_text(message.chat.id, message.id, new_message)
            except:
                continue
            
    for suffix, (src, dest) in TranslationsList.translations.items(): # Из translations.py, получаем все варианты перевода текста
        if message.text.endswith(suffix):
            await message_editing(src, dest)
            break

app.run()