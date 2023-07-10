# Data Generation

**🎯 Goal:** Generate a dataset from YouTube videos.

## Preqrequisites

- [Deepgram](https://deepgram.com/) account
- [OpenAI](https://platform.openai.com/) account
- [ffmpeg](https://ffmpeg.org/) installed (e.g. `sudo apt install ffmpeg`)
```bash
sudo apt -y update
sudo apt -y install ffmpeg
```

- Change directory into `data-gen` folder:
```bash
cd data-gen
```

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Create a YouTube Playlist

For your convenience we'll use a playlist that we've already created.

| Playlist Name | Playlist ID |
| --- | --- |
| [Startup Interviews](https://www.youtube.com/playlist?list=PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2) | `PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2` |

If you'd like to [create your own YouTube playlist](https://support.google.com/youtube/answer/57792), ensure your playlist is **public** or **unlisted**.
Then extract the playlist ID using format: `https://www.youtube.com/playlist?list={YOUR_PLAYLIST_ID}`

## 3. Download YouTube videos from the Playlist

```bash
./download.sh REPLACE_WITH_PLAYLIST_ID
```

For example, using the `Startup Interviews` playlist:

```bash
./download.sh "PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2"
```

## 4. ....

Coming soon.
