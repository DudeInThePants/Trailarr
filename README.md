# Trailarr: Movie and TV Show Trailer Downloader

Trailarr is a Python script that enables you to discover upcoming American movie and TV show titles from The Movie Database (TMDB) API and effortlessly download their trailers from YouTube. The script utilizes the `youtubesearchpython` library to search for trailer URLs and the `yt_dlp` library to download and save the trailer videos.

## Prerequisites

- Python 3.x
- Required Python libraries: `requests`, `youtubesearchpython`, `yt_dlp`
- TMDB API key and YouTube API key

## Setup

1. Clone or download this repository to your local machine.

2. Install the required Python libraries:
3. pip install requests youtubesearchpython yt-dl  
4. Obtain API keys:
- **TMDB API Key**: You need to acquire an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api) and replace `API_KEY` in the script with your key.

## Configuration

1. When executing the script, you will be prompted to input configuration parameters:

- Maximum number of movie trailers to download.
- Maximum number of TV show trailers to download.
- Number of days in the past to search for upcoming content.
- Number of days in the future to search for upcoming content.

2. The script will generate a log file (`script_log.txt`) to track the script's execution, downloaded trailers, and any errors.

## Features

- Retrieves upcoming American movie and TV show titles from TMDB API.
- Searches for trailers of these titles on YouTube using the `youtubesearchpython` library.
- Downloads and saves trailers using the `yt_dlp` library.
- Generates a log file (`script_log.txt`) containing execution details, downloaded trailers, and errors.

## Notes

- This script assumes that you have installed the required libraries and obtained the necessary API keys.
- The script may need adjustments based on your environment and use case.

## Disclaimer

Trailarr is provided as-is without any warranty. Use it responsibly and adhere to the terms of service of the APIs you are accessing.

---


