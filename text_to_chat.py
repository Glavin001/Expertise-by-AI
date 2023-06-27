import asyncio
import os
import json
from transcribe import file_to_json_path, get_recordings, get_all_recordings, print_json

async def main():
    data = get_recordings('data/Startup Interviews')
    # print(json.dumps(data, indent=4))
    all_recordings = get_all_recordings(data)
    # print_json(all_recordings)
    print_json(len(all_recordings))

    chat_items = []

    for i, recording in enumerate(all_recordings):
        # print(f"{i}: {recording['filePath']}")
        print(f"{i + 1} of {len(all_recordings)}: {recording['title']}")

        json_file_path = file_to_json_path(recording['filePath'])
        if not os.path.exists(json_file_path):
            print(f"\tJSON file does not exist at {json_file_path}")
            continue

        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            # print(json.dumps(json_data, indent=4))
            """
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "...",
                                "words": [
                                    {
                                        "word": "i",
                                        "start": 0.0,
                                        "end": 0.16,
                                        "confidence": 0.99353653,
                                        "speaker": 0,
                                        "speaker_confidence": 0.8430252,
                                        "punctuated_word": "I"
                                    },
                                ]
            """
            transcript = json_data['results']['channels'][0]['alternatives'][0]
            transcript_text = transcript['transcript']
            words = transcript['words']
            print(len(words), len(transcript_text.split()))
            # count unique speakers
            speakers = set()
            for word in words:
                speakers.add(word['speaker'])
            num_speakers = len(speakers)
            # print(len(speakers))
            print(num_speakers)

            if num_speakers > 5:
                # chat_item = {
                #     'title': recording['title'],
                #     'speakers': num_speakers,
                #     'text': transcript_text,
                # }
                # duplicate recording
                chat_item = recording.copy()
                # merge in an object with the transcript text
                chat_item.update({
                    'speakers': num_speakers,
                    'text': transcript_text,
                })
                chat_items.append(chat_item)

    print_json(chat_items)
    print_json(len(chat_items))


if __name__ == "__main__":
    asyncio.run(main())
