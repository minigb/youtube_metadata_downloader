from downloader import get_downloader


def test_top_k_metadata():
    downloader = get_downloader("yt-dlp")
    metadata_dict = downloader.get_top_results_metadata("cat", 10)

    assert len(metadata_dict) == 10
    for metadata in metadata_dict.values():
        for item_key in downloader.metadata_items:
            assert item_key in metadata.keys()