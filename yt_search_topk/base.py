from abc import ABC, abstractmethod

class MetadataDownloader(ABC):
    def __init__(self):
        self.metadata_items = [
            'title',
            'description',
            'duration',
            'id',
            'channel_title',
            'channel_id',
            'youtube_url'
        ]


    @abstractmethod
    def get_top_results_metadata(self, query, top_k, dump_dir):
        pass


    @abstractmethod
    def get_video_metadata(self, youtube_url):
        pass