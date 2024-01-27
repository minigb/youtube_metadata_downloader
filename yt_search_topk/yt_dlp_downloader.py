import subprocess
import json
from pathlib import Path

from .base import MetadataDownloader
from .utils import extract_ytid_from_url


class YTDLPDownloader(MetadataDownloader):
    def __init__(self):
        super().__init__()


    def get_top_results_metadata(self, search_query, top_k = 10, dump_path = None) -> dict:
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

        if dump_path is not None:
            dump_path = Path(dump_path)
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dump_path, "w") as f:
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


    # TODO(minigb): Implement this
    def get_videos_metadata(self, ytids, refines = True):
        pass
    

    def get_channel_name_by_url(self, youtube_url) -> str:
        youtube_id = extract_ytid_from_url(youtube_url)
        command = ['yt-dlp', '--get-filename', '-o', "%(channel)s", youtube_id]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        return output
    

    def get_channel_id_by_url(self, youtube_url) -> str:
        command = ['yt-dlp', '--get-filename', '-o', "%(channel_id)s", youtube_url]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()

        return output