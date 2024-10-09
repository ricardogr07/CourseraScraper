import os
from typing import Optional
from utils.logger import Logger
from abc import abstractmethod
from handlers.handler import Handler

class IMarkdownHandler(Handler):
    @abstractmethod
    def generate_markdown(self) -> None:
        """Generate a markdown file containing links to all outputs."""
        pass

class MarkdownHandler(IMarkdownHandler):
    def __init__(
        self, 
        video_file_path: Optional[str], 
        transcript_path: str, 
        summary_path: str, 
        concept_map_path: str, 
        visual_map_path: str,
        output_markdown_path: Optional[str] = None
    ):
        IMarkdownHandler.__init__(self)
        self.video_file_path = video_file_path
        self.transcript_path = transcript_path
        self.summary_path = summary_path
        self.concept_map_path = concept_map_path
        self.visual_map_path = visual_map_path
        self.output_markdown_path = output_markdown_path or os.path.join(
            os.path.dirname(transcript_path), f"{os.path.splitext(os.path.basename(transcript_path))[0]}.md"
        )
        self.logger = Logger("markdown_handler.log")
        self.markdown_content = ""

    def generate_markdown(self) -> None:
        """Generate the markdown content that includes references to all output files."""
        try:
            self.logger.log.info("Generating markdown content.")

            video_name = os.path.splitext(os.path.basename(self.transcript_path))[0]
            self.markdown_content = f"# {video_name}\n"

            # Add video section with HTML embed
            self.markdown_content += "\n## Video\n"
            if self.video_file_path and self.video_file_path.startswith("http"):
                # Embed video directly using HTML for web-based markdown viewers
                self.markdown_content += f'<video controls src="{self.video_file_path}" width="600"></video>\n'
            elif self.video_file_path:
                # Adjust the path for local videos
                video_relative_path = os.path.relpath(self.video_file_path, start=os.path.dirname(self.output_markdown_path))
                video_relative_path = video_relative_path.replace("\\", "/")  # Replace backslashes with forward slashes
                self.markdown_content += f'<video controls src="{video_relative_path}" width="600"></video>\n'

            # Add summary section
            self.markdown_content += "\n## Resumen\n"
            self.markdown_content += self._read_file_content(self.summary_path, "summary")

            # Add concept map section
            self.markdown_content += "\n## Mapa Conceptual\n"
            self.markdown_content += self._read_file_content(self.concept_map_path, "concept map")

            # Add visual map section
            self.markdown_content += "\n## Mapa Visual\n"
            self.markdown_content += f"![Mapa Visual]({os.path.basename(self.visual_map_path)})\n"

            self.logger.log.info("Markdown content generated successfully.")
        except Exception as e:
            self.logger.log.error(f"Error generating markdown content: {e}")
            raise

    def _read_file_content(self, file_path: str, section_name: str) -> str:
        """Reads the content of a text file and formats it for markdown."""
        try:
            self.logger.log.info(f"Reading content from {file_path} for {section_name}.")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.log.info(f"Content read successfully from {file_path}.")
            return f"```\n{content}\n```\n"
        except Exception as e:
            self.logger.log.error(f"Error reading {section_name} file: {e}")
            return f"Error reading {section_name} file.\n"

    def save_markdown(self) -> None:
        """Save the generated markdown content to a file."""
        try:
            self.logger.log.info(f"Saving markdown file to: {self.output_markdown_path}")

            with open(self.output_markdown_path, 'w', encoding='utf-8') as md_file:
                md_file.write(self.markdown_content)

            self.logger.log.info(f"Markdown file saved successfully at: {self.output_markdown_path}")
        except Exception as e:
            self.logger.log.error(f"Error saving markdown file: {e}")
            raise

    def process(self) -> None:
        """Execute the markdown generation and save process."""
        self.generate_markdown()
        self.save_markdown()


if __name__ == "__main__":
    # Define the base directory where all the files are located
    base_dir = "videos/Semana1"

    # Define the paths for each component
    video_file_path = os.path.join(base_dir, "Metodo_Cientifico.webm")
    transcript_path = os.path.join(base_dir, "Metodo_Cientifico_transcript.txt")
    summary_path = os.path.join(base_dir, "Metodo_Cientifico_summary.txt")
    concept_map_path = os.path.join(base_dir, "Metodo_Cientifico_concept_map.txt")
    visual_map_path = os.path.join(base_dir, "Metodo_Cientifico_visual_map.png")
    output_markdown_path = os.path.join(base_dir, "Metodo_Cientifico.md")

    # Create an instance of the MarkdownHandler with the provided paths
    markdown_handler = MarkdownHandler(
        video_file_path=video_file_path,
        transcript_path=transcript_path,
        summary_path=summary_path,
        concept_map_path=concept_map_path,
        visual_map_path=visual_map_path,
        output_markdown_path=output_markdown_path
    )

    # Run the process to generate and save the markdown file
    markdown_handler.process()