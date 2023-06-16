import datetime
import os
import isodate

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    """Класс для ютуб-плейлиста"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.title = self.playlist_response()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @property
    def playlist_id(self):
        return self.__playlist_id

    def playlist_response(self):
        return self.youtube.playlists().list(id=self.__playlist_id, part='snippet').execute()

    def playlist_videos_response(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        return self.youtube.videos().list(part='contentDetails,statistics',
                                          id=','.join(video_ids)
                                          ).execute()

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""

        video_response = self.playlist_videos_response()

        total_duration = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        best_video_id = None
        max_like_count = 0

        for video in self.playlist_videos_response()['items']:
            like_count = int(video['statistics']['likeCount'])

            if max_like_count < like_count:
                max_like_count = like_count
                best_video_id = video['id']

        return f'https://youtu.be/{best_video_id}'
