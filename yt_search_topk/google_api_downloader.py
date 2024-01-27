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
        self.youtube_resource = build('youtube', 'v3', developerKey=self.api_key)


    def get_top_results_metadata(self, query: str, top_k: int = 10, dump_path = None) -> dict:
        """
        Note that 101 units of cost is needed per query.
        100 for the search().list and 1 for videos().list.
        """

        # Get top k search results
        search_response = self.youtube_resource.search().list(
            q=query,
            part='snippet',
            maxResults=top_k,
            type='video'
        ).execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        # Get metadata of top k search results
        video_response = self.get_videos_metadata(video_ids, refines = False)
        search_result_list = video_response['items']

        # Dump metadata
        if dump_path is not None:
            dump_path = Path(dump_path)
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dump_path, "w") as f:
                json.dump(search_result_list, f, indent=4)

        metadata_dict = self._refine_video_metadata(search_result_list)

        return metadata_dict


    def get_videos_metadata(self, ytids, refines = True):
        if isinstance(ytids, str):
            ytids = [ytids]
        
        video_response = self.youtube_resource.videos().list(
            id=ytids,
            part='contentDetails,snippet'
        ).execute()

        if refines:
            return self._refine_video_metadata(video_response['items'])
        
        return video_response


    def _refine_video_metadata(self, search_result_list):
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