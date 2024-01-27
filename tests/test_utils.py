from yt_search_topk.utils import extract_ytid_from_url


def test_extract_ytid_from_url():
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