import os
from typing import Optional
from handlers.transcription_handler import TranscriptionHandler
from handlers.summary_handler import SummaryHandler
from handlers.concept_map_handler import ConceptMapHandler
from handlers.visual_map_handler import VisualMapHandler
from utils.logger import Logger

class PipelineManager:
    def __init__(self, video_file_path: str):
        self.video_file_path = video_file_path
        self.base_dir = os.path.dirname(video_file_path)
        self.video_name = os.path.splitext(os.path.basename(video_file_path))[0]

        self.transcript_path = os.path.join(self.base_dir, f"{self.video_name}_transcript.txt")
        self.summary_path = os.path.join(self.base_dir, f"{self.video_name}_summary.txt")
        self.concept_map_path = os.path.join(self.base_dir, f"{self.video_name}_concept_map.txt")
        self.visual_map_path = os.path.join(self.base_dir, f"{self.video_name}_visual_map.png")

        self.logger = Logger("pipeline_manager.log")

    def run(self):
        """Execute the entire pipeline."""
        self.logger.log.info("Starting the pipeline process.")

        self.transcribe_video()

        self.generate_summary()

        self.generate_concept_map()

        self.generate_visual_map()

        self.logger.log.info("Pipeline process completed successfully.")

    def transcribe_video(self):
        """Create a transcript from the video file."""
        self.logger.log.info(f"Starting transcription for video: {self.video_file_path}")
        transcription_handler = TranscriptionHandler(self.video_file_path, self.transcript_path)
        transcription_handler.process()
        self.logger.log.info(f"Transcript saved to: {self.transcript_path}")

    def generate_summary(self):
        """Generate a summary from the transcript."""
        self.logger.log.info(f"Generating summary for transcript: {self.transcript_path}")
        summary_handler = SummaryHandler(self.transcript_path, self.summary_path)
        summary_handler.process()
        self.logger.log.info(f"Summary saved to: {self.summary_path}")

    def generate_concept_map(self):
        """Generate a conceptual map from the summary."""
        self.logger.log.info(f"Generating concept map for summary: {self.summary_path}")
        concept_map_handler = ConceptMapHandler(self.summary_path, self.concept_map_path)
        concept_map_handler.process()
        self.logger.log.info(f"Concept map saved to: {self.concept_map_path}")

    def generate_visual_map(self):
        """Generate a visual map using the summary and concept map."""
        self.logger.log.info(f"Generating visual map using summary and concept map.")
        visual_map_handler = VisualMapHandler(self.summary_path, self.concept_map_path, self.visual_map_path)
        visual_map_handler.process()
        self.logger.log.info(f"Visual map saved to: {self.visual_map_path}")
