import subprocess
import json

from .base import MetadataDownloader


class YTDLPDownloader(MetadataDownloader):
    def __init__(self):
        super().__init__()


    def get_top_results_metadata(self, search_query, top_k = 10, dump_dir = None) -> dict:
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
        search_result_list = videos_info['entries']

        if dump_dir is not None:
            with open(f'{dump_dir}/{search_query}.json', 'w') as f:
                json.dump(search_result_list, f, indent=4)

        metadata_dict = {}
        for video_info in search_result_list:
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
    

    def get_channel_name_by_url(self, youtube_url) -> str:
        youtube_id = self.extract_ytid_from_url(youtube_url)
        command = ['yt-dlp', '--get-filename', '-o', "%(channel)s", youtube_id]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        return output
    

    def get_channel_id_by_url(self, youtube_url) -> str:
        command = ['yt-dlp', '--get-filename', '-o', "%(channel_id)s", youtube_url]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        return output