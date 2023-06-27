#!/usr/bin/env bash

# function which takes in 1 arg (the url) and downloads the playlist
function download_playlist {
    mkdir -p data/
    cd data/
    python3 -m yt_dlp --split-chapters --extract-audio --audio-format best --audio-quality 0 -o "%(playlist)s/%(playlist_index)s %(id)s - %(title)s.%(ext)s" -o "chapter:%(playlist)s/%(playlist_index)s %(id)s - %(title)s/%(section_number)03d %(section_title)s.%(ext)s" $1
    cd ../
}

download_playlist "https://www.youtube.com/playlist?list=PLZQTcICOilg6c4DXPE9LOGnFgUszSBGg2"
