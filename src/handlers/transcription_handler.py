import os
from abc import abstractmethod
from typing import Optional
import whisper

from handlers.handler import Handler

class ITranscriptionHandler(Handler):
    @abstractmethod
    def transcribe(self) -> Optional[str]:
        """Generate a transcript from a video file."""
        pass

    @abstractmethod
    def save_to_txt(self, output_path: str) -> None:
        """Save the transcript to a text file."""
        pass

class TranscriptionHandler(ITranscriptionHandler):
    def __init__(self, video_file_path: str, output_path: str):
        super().__init__()
        self.video_file_path = video_file_path
        self.output_path = output_path or f"{os.path.splitext(video_file_path)[0]}.txt"
        self.transcript: Optional[str] = None

    def transcribe(self) -> Optional[str]:
        try:
            self.logger.log.info(f"Starting transcription for: {self.video_file_path}")
            model = whisper.load_model("base")
            result = model.transcribe(self.video_file_path)
            self.transcript = result['text']
            self.logger.log.info("Transcription completed.")
        except Exception as e:
            self.logger.log.error(f"Error during transcription: {e}")
        return self.transcript

    def save_to_txt(self, output_path: str) -> None:
        if self.transcript:
            try:
                self.logger.log.info(f"Saving transcript to: {output_path}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(self.transcript)
                self.logger.log.info(f"Transcript saved successfully to {output_path}")
            except Exception as e:
                self.logger.log.error(f"Error saving transcript to {output_path}: {e}")
        else:
            self.logger.log.warning("Transcript is empty. Nothing to save.")

    def process(self) -> None:
        self.transcribe()
        self.save_to_txt(self.output_path)

if __name__ == "__main__":
    video_file_path = "Semana_1_Webinar_Bienvenida.webm"
    output_path = "Semana_1_Webinar_Bienvenida.txt"

    transcription_handler = TranscriptionHandler(video_file_path)
    transcription_handler.process()
