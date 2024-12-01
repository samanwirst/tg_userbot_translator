import requests
import json

class GoogleTranslator:
    def translate(text, source_language, target_language):
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q="{text}"' # Готовая ссылка на API
        response = requests.get(url)
        translation = json.loads(response.text)[0][0][0]
        return translation