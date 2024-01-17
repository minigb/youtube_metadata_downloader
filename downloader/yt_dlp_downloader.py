import subprocess
import json

from .base import MetadataDownloader


class YTDLPDownloader(MetadataDownloader):
    def __init__(self):
        super().__init__()


    def get_top_results_metadata(self, search_query, top_k = 10) -> dict:
        ytdlp_command = [
            'yt-dlp',
            f'ytsearch{top_k}:' + search_query,  # Search for top 10 videos
            '--dump-single-json',
            '--no-playlist',
            '--match-filter', '!is_live',
            '--ignore-errors',
        ]

        result = subprocess.run(ytdlp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        videos_info = json.loads(result.stdout)

        metadata_dict = {}
        for video_info in videos_info['entries']:
            video_id = video_info['id']
            metadata_dict[video_id] = {
                'id': video_id,
                'title': video_info['title'],
                'channel_id': video_info['channel_id'],
                'channel_title': video_info['channel'],
                'description': video_info['description'],
                'duration': video_info['duration'],
                'youtube_url': f'https://www.youtube.com/watch?v={video_id}'
            }

        return metadata_dict
    

    def get_channel_name(youtube_id: str) -> str:
        command = ['yt-dlp', '--get-filename', '-o', '"%(channel)s"', youtube_id]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        return output