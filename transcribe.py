from deepgram import Deepgram
import asyncio
import os
import re
import json
import codecs

# import yt_dlp

# DEEPGRAM_API_KEY = 'YOUR_API_KEY'
# PATH_TO_FILE = 'some/file.wav'

DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')

# URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

# ydl_opts = {
#     'format': 'best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }]
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     error_code = ydl.download(URLS)

def get_recordings(path_to_directory):
    # Get the list of directories and files
    dirs_and_files = os.listdir(path_to_directory)

    # Initialize the list to store the data
    data = []

    # Pattern to match
    pattern_dir = r'^(\d+) (.+) - (.+)$'
    pattern_file = r'^(\d+) (.+) - (.+)\.opus$'
    pattern_chapter = r'^(\d{3}) (.+)\.opus$'

    for df in dirs_and_files:
        full_path = os.path.join(path_to_directory, df)

        # Check if it is a directory
        if os.path.isdir(full_path):
            # Match the pattern
            match = re.match(pattern_dir, df)
            if match:
                # If the pattern matches, get the data
                index = int(match.group(1))
                youtube_id = match.group(2)
                title = clean_title(match.group(3))
                # Initialize the chapters map
                chapters = {}
                # Find all .opus files in the directory
                for chapter_file in os.listdir(full_path):
                    # Check if the file matches the chapter pattern
                    match_chapter = re.match(pattern_chapter, chapter_file)
                    if match_chapter:
                        # If the pattern matches, add the file to the chapters map
                        # Here, the chapter_number will be an integer as per your requirements
                        chapter_number = int(match_chapter.group(1))
                        chapter_title = clean_title(match_chapter.group(2))
                        # chapters[chapter_number] = os.path.join(full_path, chapter_file)
                        chapter_id = f"{youtube_id}-{chapter_number}"
                        prev_chapter_id = f"{youtube_id}-{chapter_number-1}" if chapter_number > 1 else None
                        chapters[chapter_number] = {
                            "title": chapter_title,
                            "chapterId": chapter_id,
                            "prevChapterId": prev_chapter_id,
                            "filePath": os.path.join(full_path, chapter_file)
                        }
                # Append the data to the list
                data.append({
                    'index': index,
                    'youtubeId': youtube_id,
                    'title': title,
                    'filePath': full_path,  # Full directory path for the video
                    'chapters': chapters
                })

        # Check if it is a file and matches the pattern
        elif os.path.isfile(full_path) and re.match(pattern_file, df):
            match = re.match(pattern_file, df)
            if match:
                index = int(match.group(1))
                youtube_id = match.group(2)
                title = clean_title(match.group(3))
                # Append the data to the list
                data.append({
                    'index': index,
                    'youtubeId': youtube_id,
                    'title': title,
                    'filePath': full_path,  # Full file path for the video
                    'chapters': {}  # No chapters
                })
    
    # Merge items with the same youtubeId
    return merge_items(data)

def merge_items(data):
    """
    Merge items with the same youtubeId
    """
    # Initialize the list to store the merged data
    merged_data = []

    # Initialize the dictionary to store the data
    data_dict = {}

    # Loop for all data
    for data_element in data:
        # Get the youtubeId
        youtube_id = data_element['youtubeId']

        # Check if the youtubeId is already present in the dictionary
        if youtube_id in data_dict:
            # If the youtubeId is already present, get the data
            data_dict_element = data_dict[youtube_id]
            # Check if the data has chapters
            if data_dict_element['chapters']:
                # If the data has chapters, append the new chapters
                data_dict_element['chapters'].update(data_element['chapters'])
            else:
                # If the data does not have chapters, append the chapters
                data_dict_element['chapters'] = data_element['chapters']
        else:
            # If the youtubeId is not present, add the data to the dictionary
            data_dict[youtube_id] = data_element

    # Append the dictionary values to the list
    merged_data.extend(data_dict.values())

    return merged_data

# def get_recording_file_path(data_element):
#     # Check if there are chapters
#     if data_element['chapters']:
#         # There are chapters, return the path to the first .opus file
#         # sorted() function is used to sort the chapter numbers
#         first_chapter_number = sorted(data_element['chapters'].keys())[0]
#         return data_element['chapters'][first_chapter_number]
#     else:
#         # No chapters, return the path to the standalone .opus file
#         return data_element['filePath']

def get_recording_file_paths(data_element):
    """
    Returns a list of paths to the .opus files for the recording.
    Include the chapter titles with file path.
    If there are no chapters, return video title with standalone .opus file.
    """
    # Check if there are chapters
    if data_element['chapters']:
        return list(map(lambda x: {
            # 'title': x['title'],
            'id': x['chapterId'],
            'prevId': x['prevChapterId'],
            'title': data_element['title'] + " - " + x['title'],
            'filePath': x['filePath']
        }, data_element['chapters'].values()))
    else:
        # No chapters, return the path to the standalone .opus file
        return [{
            'id': data_element['youtubeId'],
            'title': data_element['title'],
            'filePath': data_element['filePath']
        }]
        

def get_all_recordings(data):
    # loop for all data
    count = 0
    all_recordings = []
    for i, data_element in enumerate(data):
        # Get the path to the .opus file
        # opus_file_path = get_recording_file_path(data_element)
        # print(f"{i}: {opus_file_path}")
        items = get_recording_file_paths(data_element)
        # print all items
        for j, item in enumerate(items):
            count += 1
            # print(f"{i}.{j}: {item['filePath']}")
            # print(f"{count}: {item['filePath']}")
            # print(f"{count} ({i}.{j}): {item['title']}\n\t\t\t{item['filePath']}")
            all_recordings.append(item)
    return all_recordings

def file_to_json_path(file_path):
    """
    Converts a file path to a JSON file path
    """
    return file_path.replace('.opus', '.json')

async def transcribe_recording(recording):
    # get file path
    filePath = recording['filePath']
    # check if the file exists
    if not os.path.exists(filePath):
        # if the file does not exist, return
        print(f"File does not exist for {filePath}")
        return

    # generate file path for JSON output (replace .opus with .json)
    # jsonFilePath = filePath.replace('.opus', '.json')
    jsonFilePath = file_to_json_path(filePath)
    # check if JSON file already exists
    if os.path.exists(jsonFilePath):
        # if JSON file exists, return
        print(f"\tJSON file already exists at {jsonFilePath}")
        return

    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(recording['filePath'], 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/opus'}
        response = await deepgram.transcription.prerecorded(source, {
            'smart_format': True,
            'punctuate': True,
            'numerals': True,
            'diarize': True,
            'paragraphs': True,
            'utterances': False,
            "model": "nova",
            "language": "en-US"
        })
        # print(json.dumps(response, indent=4))
        # write response to JSON file
        with open(jsonFilePath, 'w') as outfile:
            json.dump(response, outfile, indent=4)
        print(f"\tTranscribed {jsonFilePath}")
        return response

async def main():
    data = get_recordings('data/Startup Interviews')
    # print(json.dumps(data, indent=4))
    all_recordings = get_all_recordings(data)
    print_json(all_recordings)

    # await transcribe_recording(all_recordings[0])
    # Loop over all recordings and transcript them
    # show progress indication
    for i, recording in enumerate(all_recordings):
        # print(f"{i}: {recording['filePath']}")
        print(f"{i + 1} of {len(all_recordings)}: {recording['title']}")
        await transcribe_recording(recording)

    # Initializes the Deepgram SDK
    # deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    # with open(PATH_TO_FILE, 'rb') as audio:
    #     # ...or replace mimetype as appropriate
    #     # source = {'buffer': audio, 'mimetype': 'audio/wav'}
    #     # source for opus
    #     source = {'buffer': audio, 'mimetype': 'audio/opus'}
    #     response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
    #     print(json.dumps(response, indent=4))

def clean_title(title):
    try:
        return title.encode('iso-8859-1').decode('utf-8')
    except UnicodeEncodeError:
        return title.encode('utf-8').decode('utf-8')

def print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
