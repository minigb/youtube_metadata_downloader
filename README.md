# YouTube TopK Search Result Videos Metadata
Tool to get top k search result videos from YouTube.<br>

## Installation
```
git clone https://github.com/minigb/yt_search_topk_meta.git
cd yt_search_topk_meta
pip install -e .
```

## Example Usage
### Init downloader
You can choose which tool to use when collecting the metadata.
1. [yt-dlp](https://github.com/yt-dlp/yt-dlp)
```
import yt_search_topk

downloader = yt_search_topk.get_downloader("yt-dlp")
```

2. [YouTube Data API](https://developers.google.com/youtube/v3)
```
import yt_search_topk

api_key_path = "/path/to/your/google_api_key.yaml"
downloader = yt_search_topk.get_downloader("google-api", api_key_path = api_key_path)
```

### Get Video Metadata
```
query = 'cat'
metadata = downloader.get_top_results_metadata(query)
```

You can also set these two options:
* top_k: number of top results to get (default: 10)
* *dump_path: file path to save the raw result (default: None)
```
query = 'cat'
top_k = 15
dump_path = 'dump.json'

metadata = downloader.get_top_results_metadata(query, top_k, dump_path)
```