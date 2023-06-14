import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = self.get_info()['items'][0]['snippet']['title']
        self.description = self.get_info()['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = self.get_info()['items'][0]['statistics']['subscriberCount']
        self.video_count = self.get_info()['items'][0]['statistics']['videoCount']
        self.view_count = self.get_info()['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    @property
    def channel_id(self):
        return self.__channel_id

    def get_info(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_info()
        printj(channel)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, channel_name: str):
        """Сохраняет в data_channels/channel_name.json значения атрибутов экземпляра 'Channel'
        НЕОБХОДИМО СОЗДАТЬ директорию data_channels в корне проекта!!!"""
        with open(f'data_channels/{channel_name}', 'w', encoding='utf-8') as f:
            data_channel = {
                "channel_id": self.__channel_id,
                "title ": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(data_channel, f)

    def __add__(self, other):
        """Метод возвращает сумму подписчиков двух каналов."""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод возвращает разницу подписчиков двух каналов."""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __le__(self, other):
        """Метод возвращает True если подписчиков первого канала меньше либо равно, иначе False."""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __ge__(self, other):
        """Метод возвращает True если подписчиков первого канала больше либо равно, иначе False."""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """Метод возвращает True если подписчиков первого канала меньше, иначе False."""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other):
        """Метод возвращает True если подписчиков первого канала больше, иначе False."""
        return int(self.subscriber_count) > int(other.subscriber_count)
