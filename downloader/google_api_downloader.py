from .base import MetadataDownloader

class GoogleAPIDownloader(MetadataDownloader):
    def __init__(self, api_key):
        self.api_key = api_key


    def download_video_metadata(self, ytid):
        # Implementation using Google API
        pass