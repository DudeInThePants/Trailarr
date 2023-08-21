import os
import requests
from youtubesearchpython import VideosSearch
from datetime import datetime, timedelta
import re
import yt_dlp

# API Key for accessing TMDB
API_KEY = "YOUR_API_KEY_HERE"

# Maximum number of movie and TV show trailers to download
MAX_MOVIE_TRAILERS = 5
MAX_TV_TRAILERS = 5

# Number of days in the past and future to search for upcoming content
DAYS_IN_PAST = 0
DAYS_IN_FUTURE = 365

# Folder names for storing movie and TV show trailers
MOVIE_TRAILERS_FOLDER = "Movies"
TV_TRAILERS_FOLDER = "TV_Shows"

# Path to the script log file
SCRIPT_LOG_PATH = "script_log.txt"

# Function to retrieve YouTube trailer URL for a given title
def get_trailer_url(title):
    search_query = f"{title} trailer"
    video_search = VideosSearch(search_query, limit=1)
    results = video_search.result()

    if results["result"]:
        video_id = results["result"][0]["id"]
        trailer_url = f"https://www.youtube.com/watch?v={video_id}"
        return trailer_url
    else:
        return None

# Function to download a trailer using yt-dlp
def download_trailer(trailer_url, folder_path, title):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(folder_path, f'{title}.%(ext)s'),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([trailer_url])

        return True
    except Exception as e:
        print(f"Error downloading trailer for {title}: {e}")
        return False

if __name__ == "__main__":
    errors = []

    try:

# Get user input for configuration parameters
        MAX_MOVIE_TRAILERS = int(input("Enter the maximum number of movie trailers to download: "))
        MAX_TV_TRAILERS = int(input("Enter the maximum number of TV show trailers to download: "))
        DAYS_IN_PAST = int(input("Enter the number of days in the past to search for upcoming content: "))
        DAYS_IN_FUTURE = int(input("Enter the number of days in the future to search for upcoming content: "))
        formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create or overwrite the script log file
        with open(SCRIPT_LOG_PATH, "w") as log_file:
            log_file.write("Script Log\n")
            log_file.write("==========\n")

        # Write script start timestamp to the log file
        with open(SCRIPT_LOG_PATH, "a") as log_file:
            log_file.write(f"Script started: {formatted_datetime}\n")
            log_file.write("=============================\n")

        print("Searching for upcoming American movie and TV show titles...")

        today = datetime.now()
        future_date = today + timedelta(days=DAYS_IN_FUTURE)
        past_date = today - timedelta(days=DAYS_IN_PAST)

        # Fetch upcoming American movie data from TMDB API
        movie_url = "https://api.themoviedb.org/3/discover/movie"
        movie_params = {
            "api_key": API_KEY,
            "primary_release_date.gte": past_date.strftime('%Y-%m-%d'),
            "primary_release_date.lte": future_date.strftime('%Y-%m-%d'),
            "language": "en-US",  # English (US) language filter
            "region": "US",  # Region filter for US
        }
        movie_response = requests.get(movie_url, params=movie_params)
        if movie_response.status_code == 200:
            movie_data = movie_response.json()
            upcoming_movies = [movie["title"] for movie in movie_data["results"] if movie["original_language"] == "en"]
        
        # Fetch upcoming American TV show data from TMDB API
        tv_url = "https://api.themoviedb.org/3/discover/tv"
        tv_show_params = {
            "api_key": API_KEY,
            "air_date.gte": past_date.strftime('%Y-%m-%d'),
            "air_date.lte": future_date.strftime('%Y-%m-%d'),
            "language": "en-US",  # English (US) language filter
            "region": "US",  # Region filter for US
        }
        tv_show_response = requests.get(tv_url, params=tv_show_params)
        if tv_show_response.status_code == 200:
            tv_show_data = tv_show_response.json()
            upcoming_tv_shows = [tv_show["name"] for tv_show in tv_show_data["results"] if tv_show["original_language"] == "en"]
        
        # Write upcoming movie and TV show titles to the log file
        with open(SCRIPT_LOG_PATH, "a") as log_file:
            log_file.write("Upcoming Movies:\n")
            for movie in upcoming_movies:
                log_file.write(f"{movie}\n")
            log_file.write("\nUpcoming TV Shows:\n")
            for tv_show in upcoming_tv_shows:
                log_file.write(f"{tv_show}\n")

        print("Searching for trailers on YouTube and downloading...")
        downloaded_movie_count = 0
        downloaded_tv_count = 0

        # Loop through upcoming movies and download trailers
        for title in upcoming_movies:
            if downloaded_movie_count >= MAX_MOVIE_TRAILERS:
                break

            sanitized_title = re.sub(r'[\/:*?"<>|]', '', title)
            folder_name = MOVIE_TRAILERS_FOLDER
            subfolder_name = sanitized_title
            folder_path = os.path.join(os.getcwd(), folder_name, subfolder_name.title())
            os.makedirs(folder_path, exist_ok=True)

            trailer_url = get_trailer_url(title)

            if trailer_url:
                with open(SCRIPT_LOG_PATH, "a") as log_file:
                    log_file.write(f"Trailer URL for '{title}': {trailer_url}\n")

                if download_trailer(trailer_url, folder_path, sanitized_title):
                    print(f"Downloaded trailer for {title}")
                    downloaded_movie_count += 1
                    with open(SCRIPT_LOG_PATH, "a") as log_file:
                        log_file.write(f"Downloaded '{title}' trailer\n")
                else:
                    with open(SCRIPT_LOG_PATH, "a") as log_file:
                        log_file.write(f"Failed to download '{title}' trailer\n")

        # Loop through upcoming TV shows and download trailers
        for title in upcoming_tv_shows:
            if downloaded_tv_count >= MAX_TV_TRAILERS:
                break

            sanitized_title = re.sub(r'[\/:*?"<>|]', '', title)
            folder_name = TV_TRAILERS_FOLDER
            subfolder_name = sanitized_title
            folder_path = os.path.join(os.getcwd(), folder_name, subfolder_name.title())
            os.makedirs(folder_path, exist_ok=True)

            trailer_url = get_trailer_url(title)

            if trailer_url:
                with open(SCRIPT_LOG_PATH, "a") as log_file:
                    log_file.write(f"Trailer URL for '{title}': {trailer_url}\n")

                if download_trailer(trailer_url, folder_path, sanitized_title):
                    print(f"Downloaded trailer for {title}")
                    downloaded_tv_count += 1
                    with open(SCRIPT_LOG_PATH, "a") as log_file:
                        log_file.write(f"Downloaded '{title}' trailer\n")
                else:
                    with open(SCRIPT_LOG_PATH, "a") as log_file:
                        log_file.write(f"Failed to download '{title}' trailer\n")

        print("Finished downloading trailers.")
    except Exception as e:
        errors.append(f"An error occurred: {e}")

    # Write script finish timestamp and errors to the log file
    with open(SCRIPT_LOG_PATH, "a") as log_file:
        log_file.write("=============================\n")
        log_file.write(f"Script finished: {formatted_datetime}\n")
        log_file.write("=============================\n\n")
        log_file.write("Errors:\n")
        for error in errors:
            log_file.write(f"{error}\n")

    print("Log file generated:", SCRIPT_LOG_PATH)
