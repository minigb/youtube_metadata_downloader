from omegaconf import OmegaConf

from downloader import *


def test_top_k_metadata():
    api_config = OmegaConf.load('google_api.yaml')
    api_key = api_config.api_key

    downloader = get_downloader("google-api", api_key = api_key)
    metadata_dict = downloader.get_top_results_metadata("cat", top_k = 10)

    assert len(metadata_dict) == 10
    for metadata in metadata_dict.values():
        for item_key in downloader.metadata_items:
            assert item_key in metadata.keys()