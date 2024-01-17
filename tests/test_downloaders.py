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
    url_list = [
        "https://www.youtube.com/watch?v=zSQ48zyWZrY",
        "https://www.youtube.com/watch?v=zSQ48zyWZrY&t=60",
        "https://www.youtube.com/embed/zSQ48zyWZrY",
        "https://youtu.be/zSQ48zyWZrY",
        "https://youtu.be/zSQ48zyWZrY?t=60",
        "https://m.youtube.com/watch?v=zSQ48zyWZrY"
    ]
    ytid = "zSQ48zyWZrY"

    for url in url_list:
        assert downloader.extract_ytid_from_url(url) == ytid


# TODO(minigb): Add test for GoogleAPIDownloader
@pytest.mark.parametrize("downloader", [yt_dlp_downloader])
def test_get_channel_name(downloader):
    url = "https://www.youtube.com/watch?v=zSQ48zyWZrY"
    assert downloader.get_channel_name_by_url(url) == "HYBE LABELS"


# TODO(minigb): Add test for GoogleAPIDownloader
@pytest.mark.parametrize("downloader", [yt_dlp_downloader])
def test_get_channel_id(downloader):
    url = "https://www.youtube.com/watch?v=zSQ48zyWZrY"
    assert downloader.get_channel_id_by_url(url) == "UC3IZKseVpdzPSBaWxBxundA"