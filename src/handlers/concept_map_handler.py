import os
from abc import abstractmethod
from typing import List, Optional
from handlers.handler import Handler
from utils.openai_handler import BaseOpenAIHandler

class IConceptMapHandler(Handler):
    @abstractmethod
    def generate_concept_map(self) -> List[str]:
        """Generate a conceptual map based on the summary."""
        pass

    @abstractmethod
    def save_concept_map(self, output_path: str) -> None:
        """Save the conceptual map as bullet points to a text file."""
        pass


class ConceptMapHandler(IConceptMapHandler, BaseOpenAIHandler):
    def __init__(self, summary_path: str, concept_map_output_path: Optional[str] = None):
        IConceptMapHandler.__init__(self)
        BaseOpenAIHandler.__init__(self)
        self.summary_path = summary_path
        self.concept_map_output_path = concept_map_output_path or f"{os.path.splitext(summary_path)[0]}_concept_map.txt"
        self.concept_map: List[str] = []

    def _read_summary(self) -> str:
        """Reads the summary from the specified .txt file path."""
        try:
            self.logger.log.info(f"Reading summary from: {self.summary_path}")
            with open(self.summary_path, 'r', encoding='utf-8') as f:
                summary = f.read()
            self.logger.log.info("Summary read successfully.")
            return summary
        except Exception as e:
            self.logger.log.error(f"Error reading summary: {e}")
            raise

    def create_messages(self, summary: str) -> list:
        """
        Creates the messages for the OpenAI API to generate a conceptual map.
        
        Parameters:
            summary (str): The summary content from which to extract key points.
        
        Returns:
            list: A list of messages formatted for the OpenAI API.
        """
        return [
            {"role": "system", "content": "Eres un asistente que crea mapas conceptuales en español a partir de resúmenes."},
            {"role": "user", "content": f"Genera un mapa conceptual en formato de puntos clave a partir del siguiente resumen:\n\n{summary}"}
        ]

    def generate_concept_map(self) -> List[str]:
        """Generate a conceptual map using the OpenAI API."""
        try:
            summary = self._read_summary()
            self.logger.log.info("Generating conceptual map using OpenAI API.")
            
            # Prepare messages using the summary
            messages = self.create_messages(summary)
            result = self.generate_chat_completion(messages)
            
            # Parse the result into a list of bullet points
            self.concept_map = [
                f"- {line.strip()}" for line in result.split("\n") if line
            ]
            
            self.logger.log.info("Conceptual map generation completed.")
        except Exception as e:
            self.logger.log.error(f"Error during conceptual map generation: {e}")
        return self.concept_map

    def save_concept_map(self, output_path: str) -> None:
        """Save the conceptual map as bullet points to a text file."""
        if self.concept_map:
            try:
                self.logger.log.info(f"Saving conceptual map to: {output_path}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    for point in self.concept_map:
                        f.write(f"{point}\n")
                self.logger.log.info(f"Conceptual map saved successfully to {output_path}")
            except Exception as e:
                self.logger.log.error(f"Error saving conceptual map to {output_path}: {e}")
        else:
            self.logger.log.warning("Conceptual map is empty. Nothing to save.")

    def process(self) -> None:
        """Generate and save the conceptual map."""
        self.generate_concept_map()
        self.save_concept_map(self.concept_map_output_path)

if __name__ == "__main__":
    summary_path = "Summary.txt"  # The .txt file containing the summary.
    concept_map_handler = ConceptMapHandler(summary_path)
    concept_map_handler.process()
