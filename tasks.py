import requests
import json
import logging
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    user_text = input('Введите текст для картинки: ')
    yandex_token = input('Введите токен Яндекс.Диска: ')

    
    encoding_text = quote(user_text)
    image_url = f'https://cataas.com/cat/says/{encoding_text}'
    
    logger.info(f'Получение картинки с текстом: {user_text}')
    
    headers = {
        'Authorization': f'OAuth {yandex_token}',
    }
    
    create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': 'PD-138'}
    
    response = requests.put(create_folder_url, headers=headers, params=params)
    logger.info(f'Создание папки: {response.status_code}')
    
    if response.status_code in [201, 409]:
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        upload_params = {
            'path': f'PD-138/{user_text}.jpg',
            'url': image_url
        }
        
        logger.info('Загрузка картинки...')
        response = requests.post(upload_url, headers=headers, params=upload_params)
        logger.info(f'Статус загрузки: {response.status_code}')
        
        if response.status_code == 202:
            file_info = {
                'file_name': f'{user_text}.jpg',
                'upload_status': 'Успешно!'
            }
            
            with open('file_info.json', 'w', encoding='utf-8') as f:
                json.dump(file_info, f, ensure_ascii=False, indent=4)
            
            logger.info('JSON файл создан')

if __name__ == '__main__':
    main()