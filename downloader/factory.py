from .google_api_downloader import GoogleAPIDownloader
from .yt_dlp_downloader import YTDLPDownloader


def get_downloader(method_name):
    if method_name == "yt-dlp":
        return YTDLPDownloader()
    elif method_name == "google-api":
        return GoogleAPIDownloader()
    else:
        raise ValueError("Unknown method")