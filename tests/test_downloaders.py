import pytest
import tempfile
import os
import json

from yt_search_topk import *


downloader_by_yt_dlp = get_downloader("yt-dlp")
downloader_by_google_api = get_downloader("google-api", api_key_path = 'google_api.yaml')


def test_get_downloader():
    assert isinstance(downloader_by_yt_dlp, YTDLPDownloader)
    assert isinstance(downloader_by_google_api, GoogleAPIDownloader)

    with pytest.raises(ValueError):
        get_downloader("unknown_method")


@pytest.mark.parametrize("downloader", [downloader_by_yt_dlp, downloader_by_google_api])
def test_get_top_results_metadata(downloader):
    top_k = 2
    metadata_dict = downloader.get_top_results_metadata("cat", top_k)

    assert len(metadata_dict) == top_k
    for metadata in metadata_dict.values():
        for item_key in downloader.metadata_items:
            assert item_key in metadata.keys()


@pytest.mark.parametrize("downloader", [downloader_by_yt_dlp, downloader_by_google_api])
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
        assert extract_ytid_from_url(url) == ytid


# TODO(minigb): Add test for GoogleAPIDownloader
@pytest.mark.parametrize("downloader", [downloader_by_yt_dlp])
def test_get_channel_name(downloader):
    url = "https://www.youtube.com/watch?v=zSQ48zyWZrY"
    assert downloader.get_channel_name_by_url(url) == "HYBE LABELS"


# TODO(minigb): Add test for GoogleAPIDownloader
@pytest.mark.parametrize("downloader", [downloader_by_yt_dlp])
def test_get_channel_id(downloader):
    url = "https://www.youtube.com/watch?v=zSQ48zyWZrY"
    assert downloader.get_channel_id_by_url(url) == "UC3IZKseVpdzPSBaWxBxundA"


@pytest.mark.parametrize("downloader", [downloader_by_google_api, downloader_by_yt_dlp])
def test_dump_dir(downloader):
    query = 'cat'
    top_k = 2
    dump_dir = tempfile.mkdtemp()
    dump_path = f"{dump_dir}/{query}.json"
    _ = downloader.get_top_results_metadata(query, top_k, dump_path)

    assert os.path.exists(dump_path)
    
    with open(dump_path, "r") as f:
        metadata_dump = json.load(f)
    assert len(metadata_dump) == top_k

    os.remove(dump_path)
    os.rmdir(dump_dir)