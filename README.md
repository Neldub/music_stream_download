This application is a Python-based tool designed to download audio from YouTube, SoundCloud, and Spotify. It uses the pytube library for YouTube, yt-dlp for SoundCloud, and savify for Spotify. The application features a graphical user interface (GUI) created with tkinter that allows users to input the URL, select the download directory, and, for Spotify, select a credentials file for API access. The application automatically identifies the service based on the URL and downloads the audio in MP3 format with the highest possible bitrate (320kbps).

Requirements
General Requirements
Python 3.x
pip (Python package installer)
Python Libraries
pytube
moviepy
yt-dlp
savify
tkinter
Installation and Setup
Windows
Install Python:
Download and install Python 3.x from python.org.

Install ffmpeg:

Download ffmpeg from ffmpeg.org.
Extract the downloaded file and add the bin directory to your system's PATH environment variable.
Install Python Libraries:
Open a Command Prompt and run the following command:

bash
pip install pytube moviepy yt-dlp savify tkinter
macOS
Install Python:
Download and install Python 3.x from python.org.

Install ffmpeg:

Use Homebrew to install ffmpeg by opening a Terminal and running:
bash 
brew install ffmpeg

Install Python Libraries:
Open a Terminal and run the following command:

bash
pip install pytube moviepy yt-dlp savify tkinter
Usage
Run the Application:
Save the provided Python script to a file (e.g., audio_downloader.py) and run it:

bash
python py_download.py
Input and Select:

Enter the URL of the YouTube, SoundCloud, or Spotify track you wish to download.
Select the download directory.
For Spotify, select the credentials file (a JSON file containing your Spotify API client ID and client secret).
Download:
Click the "Download" button to start the process. The application will download the audio and save it as an MP3 file with a bitrate of 320kbps in the selected directory.

By following these steps, you can successfully run the application on both Windows and macOS, enabling you to download audio from YouTube, SoundCloud, and Spotify easily.
