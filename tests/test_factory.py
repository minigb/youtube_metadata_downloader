import pytest
from omegaconf import OmegaConf

from downloader import get_downloader, YTDLPDownloader, GoogleAPIDownloader


def test_get_downloader():
    downloader = get_downloader("yt-dlp")
    assert isinstance(downloader, YTDLPDownloader)

    downloader = get_downloader("google-api", api_key = "fake_api_key")
    assert isinstance(downloader, GoogleAPIDownloader)

    with pytest.raises(ValueError):
        get_downloader("unknown_method")


def test_get_top_results_metadata():
    yt_dlp_downloader = get_downloader("yt-dlp")
    # metadata_dict = downloader.get_top_results_metadata("cat", 10)

    api_config = OmegaConf.load('google_api.yaml')
    api_key = api_config.api_key
    google_api_downloader = get_downloader("google-api", api_key = api_key)

    for downloader in [yt_dlp_downloader, google_api_downloader]:
        metadata_dict = downloader.get_top_results_metadata("cat", top_k = 10)

        assert len(metadata_dict) == 10
        for metadata in metadata_dict.values():
            for item_key in downloader.metadata_items:
                assert item_key in metadata.keys()