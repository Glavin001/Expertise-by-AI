#!/usr/bin/env bash

DATA_DIR=$(dirname $(dirname $(realpath $0)))/data/
echo $DATA_DIR

function download_playlist {
    PLAYLIST_ID=$1

    echo "Creating directory $DATA_DIR"
    mkdir -p $DATA_DIR

    echo "Downloading playlist $PLAYLIST_ID"
    (cd $DATA_DIR && python3 -m yt_dlp --split-chapters --extract-audio --audio-format best --audio-quality 0 -o "%(playlist)s/%(playlist_index)s %(id)s - %(title)s.%(ext)s" -o "chapter:%(playlist)s/%(playlist_index)s %(id)s - %(title)s/%(section_number)03d %(section_title)s.%(ext)s" $PLAYLIST_ID)

    echo "Done downloading playlist $PLAYLIST_ID"
    echo "Look in $DATA_DIR for the downloaded files"
}

download_playlist $1
