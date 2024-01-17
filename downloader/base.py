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
    def get_top_results_metadata(self, query, top_k):
        pass


    def ytid_to_url(self, ytid, start_time = None):
        if start_time is not None:
            return f"https://www.youtube.com/watch?v={ytid}&t={start_time}"
        return f"https://www.youtube.com/watch?v={ytid}"