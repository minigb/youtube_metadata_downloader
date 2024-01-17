import pytest
from omegaconf import OmegaConf

from downloader import *


yt_dlp_downloader = get_downloader("yt-dlp")

api_config = OmegaConf.load('google_api.yaml')
api_key = api_config.api_key
google_api_downloader = get_downloader("google-api", api_key = api_key)


def test_get_downloader():
    assert isinstance(yt_dlp_downloader, YTDLPDownloader)
    assert isinstance(google_api_downloader, GoogleAPIDownloader)

    with pytest.raises(ValueError):
        get_downloader("unknown_method")


@pytest.mark.parametrize("downloader", [yt_dlp_downloader, google_api_downloader])
def test_get_top_results_metadata(downloader):
    top_k = 2
    metadata_dict = downloader.get_top_results_metadata("cat", top_k)

    assert len(metadata_dict) == top_k
    for metadata in metadata_dict.values():
        for item_key in downloader.metadata_items:
            assert item_key in metadata.keys()


@pytest.mark.parametrize("downloader", [yt_dlp_downloader, google_api_downloader])
def test_extract_ytid_from_url(downloader):
    assert downloader.extract_ytid_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert downloader.extract_ytid_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=60") == "dQw4w9WgXcQ"
    assert downloader.extract_ytid_from_url("https://www.youtube.com/embed/so9QrPEWG0M") == "so9QrPEWG0M"
    assert downloader.extract_ytid_from_url("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"