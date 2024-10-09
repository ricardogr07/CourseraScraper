import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from abc import abstractmethod
from typing import Optional

from handlers.handler import Handler

class IVideoHandler(Handler):
    @abstractmethod
    def download_video(self) -> Optional[str]:
        """Download the video and return the local file path"""
        pass

class VideoHandler(IVideoHandler):
    def __init__(self, video_url: str):
        super().__init__()
        self.logger.log.info(f'Initialized VideoHandler class with {video_url}')
        self.video_url = video_url
        self.username = os.getenv('COURSERA_EMAIL')
        self.password = os.getenv('COURSERA_PASSWORD')
        self.file_path: Optional[str] = None

    def download_video(self) -> Optional[str]:
        local_filename = self.video_url.split("/")[-1].split("?")[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        try:
            self.logger.log.info(f"Starting download")
            with requests.get(
                self.video_url, 
                auth=HTTPBasicAuth(self.username, self.password), 
                headers=headers, 
                stream=True
            ) as response:
                response.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            self.file_path = local_filename
            self.logger.log.info(f"Downloaded video to {self.file_path}")
        except requests.exceptions.RequestException as e:
            self.logger.log.error(f"Error downloading video: {e}")
        return self.file_path

    def process(self) -> None:
        self.download_video()

if __name__ == "__main__":
    video_url = "https://d3c33hcgiwev3.cloudfront.net/61235b4c-7330-4e92-9952-94f43e80a428_76cceeb3f26746e18cbfa1b6b7da8f9d_GMT20241007-210427_Recording_1920x1080_WEBM_720.webm?Expires=1728604800&Signature=QVqWE-S3w9076BAc2kqLXccdFKe0JIIkM~k~dqt-6rZFxjbApqOhyRPGKmPBfvJwXVISX9fjX~V6mGpwFdEz-eLCtwERD8K9GtVhTJCb3mY5H1WjaCSs3B5kRO0RfuTrHM~y40D3jyXzP2UHf~gWhS84qxOxKldlCS3z21al-LY_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
    load_dotenv()
    video_handler = VideoHandler(video_url)
    video_handler.process()
