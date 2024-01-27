import re


def ytid_to_url(ytid, start_time = None):
    if start_time is not None:
        return f"https://www.youtube.com/watch?v={ytid}&t={start_time}"
    return f"https://www.youtube.com/watch?v={ytid}"


def extract_ytid_from_url(url):
    # Regular expression for extracting the video ID
    yt_url_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'

    match = re.search(yt_url_regex, url)
    if match:
        return match.group(1)
    else:
        return None