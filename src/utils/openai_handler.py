from abc import ABC, abstractmethod
from utils.logger import Logger
import os
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIHandler(ABC):
    """
    Abstract base class for OpenAI handlers.
    Defines the interface for handling chat completions.
    """
    
    def __init__(self, logger=None):
        """
        Initialize the OpenAIHandler with a logger instance and configure the OpenAI client
        by loading the API key from environment variables.
        """
        self.logger = logger if logger is not None else Logger("openai.log")
        self.logger.log.info("Initializing OpenAI Handler")
        self._configure_openai()
    
    @abstractmethod
    def create_messages(self, *args, **kwargs):
        """Create messages for processing."""
        pass
    
    @abstractmethod
    def generate_chat_completion(self, messages: list) -> str:
        """Generate chat completion using OpenAI."""
        pass

    def _configure_openai(self):
        """
        Configures the OpenAI client by loading the API key from environment variables.
        Raises EnvironmentError if the API key is missing.
        """
        self.logger.log.info("Configuring OpenAI Client")

        try:
            load_dotenv()
            OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        except Exception as e:
            self.logger.log.error(f"Error loading environment variables: {e}")
            raise EnvironmentError("API Key is missing in .env file.")        
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)

class BaseOpenAIHandler(OpenAIHandler):
    """
    A base class that provides the generic implementation for generating chat completions.
    """
    
    def generate_chat_completion(self, messages: list) -> str:
        """
        Generates chat completions using the OpenAI client and returns the markdown result.

        Parameters:
            messages (list): A list of messages for chat completion generation.

        Returns:
            str: The markdown-formatted response from the chat completion.
        """
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model="gpt-4",
            )
            result = completion.choices[0].message.content
            
            return result
        
        except Exception as e:
            self.logger.log.error(f"Unexpected error: {e}")
            raise

class MarkdownFileHandler(BaseOpenAIHandler):
    """
    Handler for converting .txt files to markdown and saving them as .md files.
    """

    def create_messages(self, text: str) -> list:
        """
        Creates a list of messages to format the input text into markdown.

        Parameters:
            text (str): The content of the .txt file to be processed.

        Returns:
            list: Messages formatted for chat completion requests.
        """
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant that formats text into markdown."
            },
            {
                "role": "user",
                "content": f"Please format the following text into markdown:\n\n{text}"
            }
        ]

    def process_file(self, file_path: str) -> str:
        """
        Reads the input .txt file, converts it to markdown, and saves it with a .md extension.

        Parameters:
            file_path (str): The path to the .txt file.

        Returns:
            str: The path to the saved .md file.
        """
        try:
            # Read the .txt file
            with open(file_path, 'r') as file:
                text = file.read()

            # Create the messages and generate markdown
            messages = self.create_messages(text)
            markdown_content = self.generate_chat_completion(messages)
            
            # Change the extension from .txt to .md
            md_file_path = file_path.replace('.txt', '.md')

            # Save the markdown content to the new file
            with open(md_file_path, 'w') as md_file:
                md_file.write(markdown_content)

            self.logger.log.info(f"Markdown file saved at {md_file_path}")
            return md_file_path
        
        except Exception as e:
            self.logger.log.error(f"Error processing file: {e}")
            raise
