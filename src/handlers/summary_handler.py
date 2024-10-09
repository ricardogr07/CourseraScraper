from abc import abstractmethod
from handlers.handler import Handler
from typing import Optional
import os
from typing import Optional
from utils.openai_handler import BaseOpenAIHandler

class ISummaryHandler(Handler):
    @abstractmethod
    def summarize(self) -> Optional[str]:
        """Summarize the content of a transcript."""
        pass

    @abstractmethod
    def save_summary(self, output_path: str) -> None:
        """Save the summary to a text file."""
        pass

class SummaryHandler(ISummaryHandler, BaseOpenAIHandler):
    def __init__(self, transcript_path: str, summary_output_path: Optional[str] = None):
        ISummaryHandler.__init__(self)
        BaseOpenAIHandler.__init__(self)
        self.transcript_path = transcript_path
        self.summary_output_path = summary_output_path or f"{os.path.splitext(transcript_path)[0]}_summary.txt"
        self.summary: Optional[str] = None

    def _read_transcript(self) -> str:
        """Reads the transcript from the specified path."""
        try:
            self.logger.log.info(f"Reading transcript from: {self.transcript_path}")
            with open(self.transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()
            self.logger.log.info("Transcript read successfully.")
            return transcript
        except Exception as e:
            self.logger.log.error(f"Error reading transcript: {e}")
            raise

    def create_messages(self, transcript: str) -> list:
            """
            Creates the messages for the OpenAI API to generate a summary.
            
            Parameters:
                transcript (str): The content of the transcript to be summarized.
            
            Returns:
                list: A list of messages formatted for the OpenAI API.
            """
            return [
                {"role": "system", "content": "Eres un asistente útil que resume transcripciones en español de clases."},
                {"role": "user", "content": f"Resume la siguiente transcripción en español:\n\n{transcript}"}
            ]

    def summarize(self) -> Optional[str]:
        """Generate a summary of the transcript using the OpenAI API."""
        try:
            transcript = self._read_transcript()
            self.logger.log.info("Generating summary using OpenAI API.")
            
            messages = self.create_messages(transcript)

            self.summary = self.generate_chat_completion(messages)
            self.logger.log.info("Summary generation completed.")
        except Exception as e:
            self.logger.log.error(f"Error during summary generation: {e}")
        return self.summary

    def save_summary(self, output_path: str) -> None:
        """Save the summary to a text file."""
        if self.summary:
            try:
                self.logger.log.info(f"Saving summary to: {output_path}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(self.summary)
                self.logger.log.info(f"Summary saved successfully to {output_path}")
            except Exception as e:
                self.logger.log.error(f"Error saving summary to {output_path}: {e}")
        else:
            self.logger.log.warning("Summary is empty. Nothing to save.")

    def process(self) -> None:
        """Read the transcript, generate a summary, and save it."""
        self.summarize()
        self.save_summary(self.summary_output_path)

if __name__ == "__main__":
    transcript_path = "Semana_1_Webinar_Bienvenida.txt"  # The .txt file generated from the transcription.
    summary_output_path = "Summary.txt"  # Optional: specify a different output path.

    summary_handler = SummaryHandler(transcript_path, summary_output_path)
    summary_handler.process()
