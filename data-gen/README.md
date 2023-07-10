# Data Generation

**🎯 Goal:** Generate a text dataset from a playlist of YouTube videos.

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

## 3. Download YouTube videos as audio from the Playlist

The following command will download all videos from the playlist as audio files and split them into chapters, if available:

```bash
./download.sh REPLACE_WITH_PLAYLIST_ID
```

For example, using the `Startup Interviews` playlist:

```bash
./download.sh "PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2"
```

## 4. Transcribe Audio to Text

First, create a new Deepgram API key.

<details>
<summary>❓ How to create a new Deepgram API key?</summary>

1. Click `API Keys` in the left sidebar.

![image](https://github.com/Glavin001/Expertise-by-AI/assets/1885333/550cd7de-05c5-49da-ada1-b2e3fcd4cac7)

2. Click `Create API Key` button.

![image](https://github.com/Glavin001/Expertise-by-AI/assets/1885333/02a6f971-6f5b-4148-afe4-58f7b4820848)

3. Select `Member` and click `Create Key` button.

![image](https://github.com/Glavin001/Expertise-by-AI/assets/1885333/1d10b6c3-6c11-406b-b738-f7ea9869675c)

4. Copy the API key.

</details>

Then, set your Deepgram API key as an environment variable:

```bash
export DEEPGRAM_API_KEY=REPLACE_WITH_YOUR_API_KEY
```

Now you can run the script to convert YouTube videos to text:

```bash
python3 transcribe.py REPLACE_WITH_PLAYLIST_ID
```

For example, using the `Startup Interviews` playlist:

```bash
python3 transcribe.py "PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2"
```

You now have `.json` files containing the transcrptions of each video in the playlist!
