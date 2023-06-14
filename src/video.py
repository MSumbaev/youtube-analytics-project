import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


class Video:
    """Класс для ютуб-видео"""

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        self.title = self.video_response()['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.view_count = self.video_response()['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response()['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self):
        return self.__video_id

    def video_response(self):
        return self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=self.__video_id).execute()


class PLVideo(Video):
    """Класс для  ютуб-видео и плейлиста где он находится"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
