import vk_api
import time
import requests
import logging
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from config import TOKEN, CHAT_IDS, GROUP_ID, access_token, GROUP_IDS, access_token_andr, GROUP_IDS_andr

# Настройка логирования
logging.basicConfig(
    filename='bot_log.log',  # Файл для логов
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(message)s',  # Формат: время и сообщение
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
)

# Авторизация для пользователя
vk_session = vk_api.VkApi(token=access_token_andr)
vk = vk_session.get_api()

# Авторизация для бота
vk_session1 = vk_api.VkApi(token=TOKEN)
vk1 = vk_session1.get_api()

# Подключение LongPoll для бота
longpoll = VkBotLongPoll(vk_session1, GROUP_ID)

# Функция для отправки сообщений с задержкой и обработкой капчи
def send_message(message, delay=5):
    for group_id in GROUP_IDS_andr:
        vk.messages.send(
            peer_id=group_id,
            message=message,
            random_id=get_random_id()
        )
        logging.info(f"Сообщение отправлено в беседу {group_id}: {message}")
        time.sleep(delay)  # Задержка между отправкой сообщений

# Основная функция работы бота
def main():
    logging.info("Бот запущен и ожидает сообщений...")
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message_info = event.object.message
                # Проверяем, что сообщение отправлено в ЛС (отправитель и получатель совпадают)
                if message_info['peer_id'] == message_info['from_id']:
                    new_message = message_info['text']
                    logging.info(f"Новое сообщение в боте: {new_message}")

                    send_message(new_message)
    except requests.exceptions.ReadTimeout:
        logging.error("Ошибка подключения (ReadTimeout), перезапуск через 5 секунд...")
        time.sleep(5)  # Задержка при ошибке подключения
        main()

# Запуск бота
if __name__ == "__main__":
    main()
