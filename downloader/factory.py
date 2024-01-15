from .google_api_downloader import GoogleAPIDownloader
from .yt_dlp_downloader import YTDLPDownloader


def get_downloader(method_name, **kwargs):
    if method_name == "yt-dlp":
        return YTDLPDownloader()
    elif method_name == "google-api":
        api_key = kwargs.get("api_key")
        return GoogleAPIDownloader(api_key = api_key)
    else:
        raise ValueError("Unknown method")