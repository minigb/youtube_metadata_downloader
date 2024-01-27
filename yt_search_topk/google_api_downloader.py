from googleapiclient.discovery import build
from isodate import parse_duration
from pathlib import Path
import json

from .base import MetadataDownloader
from .utils import extract_ytid_from_url


class GoogleAPIDownloader(MetadataDownloader):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key


    def get_top_results_metadata(self, query: str, top_k: int = 10, dump_path = None) -> dict:
        """
        Note that 101 units of cost is needed per query.
        100 for the search().list and 1 for videos().list.
        """
        api_key = self.api_key
        youtube = build('youtube', 'v3', developerKey=api_key)

        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=top_k,
            type='video'
        ).execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        video_response = youtube.videos().list(
            id=','.join(video_ids),
            part='contentDetails,snippet'
        ).execute()
        search_result_list = video_response['items']

        if dump_path is not None:
            dump_path = Path(dump_path)
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dump_path, "w") as f:
                json.dump(search_result_list, f, indent=4)

        metadata_dict = {}
        for item in search_result_list:
            video_id = item['id']
            metadata_dict[video_id] = {
                'id': video_id,
                'title': item['snippet']['title'],
                'duration': parse_duration(item['contentDetails']['duration']).total_seconds(),
                'channel_title': item['snippet']['channelTitle'],
                'channel_id': item['snippet']['channelId'],
                'description': item['snippet']['description'],
                'youtube_url': f'https://www.youtube.com/watch?v={video_id}'
            }

        return metadata_dict


    def get_video_metadata(self, youtube_url, do_refine = True):
        api_key = self.api_key
        youtube = build('youtube', 'v3', developerKey=api_key)

        ytid = self.extract_ytid_from_url(youtube_url)
        video_response = youtube.videos().list(
            id=ytid,
            part='contentDetails,snippet'
        ).execute()

        return video_response['items'][0]


    def _refine_video_metadata(self, metadata):
        metadata['duration'] = parse_duration(metadata['contentDetails']['duration']).total_seconds()
        metadata['channel_title'] = metadata['snippet']['channelTitle']
        metadata['description'] = metadata['snippet']['description']
        metadata['youtube_url'] = f'https://www.youtube.com/watch?v={metadata["id"]}'

        return metadata