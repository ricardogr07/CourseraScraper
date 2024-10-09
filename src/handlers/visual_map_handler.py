from abc import abstractmethod
from handlers.handler import Handler
from typing import Optional

import spacy
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional

class IVisualMapHandler(Handler):
    @abstractmethod
    def generate_visual_map(self) -> None:
        """Generate a visual map based on the summary and concept map."""
        pass

    @abstractmethod
    def save_visual_map(self, output_path: str) -> None:
        """Save the generated visual map as an image."""
        pass

class VisualMapHandler(IVisualMapHandler):
    def __init__(self, summary_path: str, concept_map_path: str, output_image_path: Optional[str] = None):
        super().__init__()
        self.summary_path = summary_path
        self.concept_map_path = concept_map_path
        self.output_image_path = output_image_path or f"{os.path.splitext(summary_path)[0]}_visual_map.png"
        self.nlp = spacy.load("es_core_news_md")
        self.graph = nx.Graph()

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

    def _read_concept_map(self) -> List[str]:
        """Reads the concept map from the specified .txt file path."""
        try:
            self.logger.log.info(f"Reading concept map from: {self.concept_map_path}")
            with open(self.concept_map_path, 'r', encoding='utf-8') as f:
                concept_map = [line.strip() for line in f if line.strip()]
            self.logger.log.info("Concept map read successfully.")
            return concept_map
        except Exception as e:
            self.logger.log.error(f"Error reading concept map: {e}")
            raise

    def _extract_entities_and_relations(self, text: str):
        """Extract entities and relationships using spaCy."""
        doc = self.nlp(text)
        entities = {ent.text for ent in doc.ents}
        relations = []

        # Iterate through sentences to identify potential relationships
        for sent in doc.sents:
            sent_entities = [ent.text for ent in sent.ents]
            if len(sent_entities) > 1:
                # Create a relationship between each pair of entities in the sentence
                for i in range(len(sent_entities) - 1):
                    relations.append((sent_entities[i], sent_entities[i + 1]))
        
        return entities, relations

    def generate_visual_map(self) -> None:
        """Generate a visual map using spaCy NLP and networkx."""
        try:
            summary = self._read_summary()
            concept_map = self._read_concept_map()

            self.logger.log.info("Generating visual map based on summary and concept map.")
            
            # Extract entities and relationships from the summary
            summary_entities, summary_relations = self._extract_entities_and_relations(summary)

            # Add entities and relationships to the graph
            self.graph.add_nodes_from(summary_entities)
            self.graph.add_edges_from(summary_relations)

            # Also add entities from the concept map as nodes
            concept_entities = [point[2:].strip() for point in concept_map]  # Remove "- " from bullet points
            self.graph.add_nodes_from(concept_entities)

            self.logger.log.info("Visual map generation completed.")
        except Exception as e:
            self.logger.log.error(f"Error during visual map generation: {e}")

    def save_visual_map(self, output_path: str) -> None:
        """Save the generated visual map as an image."""
        try:
            self.logger.log.info(f"Saving visual map to: {output_path}")

            # Calculate degree centrality for adjusting node sizes
            centrality = nx.degree_centrality(self.graph)
            node_sizes = [3000 + 10000 * centrality[node] for node in self.graph.nodes()]

            # Draw the graph using a better layout and adjusted settings
            plt.figure(figsize=(12, 10))
            pos = nx.spring_layout(self.graph, k=0.3, iterations=50, seed=42)

            # Draw nodes, edges, and labels with adjusted sizes and styles
            nx.draw_networkx_nodes(
                self.graph, pos, node_size=node_sizes, node_color="skyblue", alpha=0.9
            )
            nx.draw_networkx_edges(
                self.graph, pos, edge_color="gray", alpha=0.5, width=2
            )
            nx.draw_networkx_labels(
                self.graph, pos, font_size=10, font_family="sans-serif", font_weight="bold"
            )

            plt.title("Conceptual Map Visualization")
            plt.tight_layout()
            plt.savefig(output_path, format="png", dpi=300)
            plt.close()

            self.logger.log.info(f"Visual map saved successfully to {output_path}")
        except Exception as e:
            self.logger.log.error(f"Error saving visual map to {output_path}: {e}")

    def process(self) -> None:
        """Generate and save the visual map."""
        self.generate_visual_map()
        self.save_visual_map(self.output_image_path)

if __name__ == "__main__":
    summary_path = "Summary.txt"  # The .txt file containing the summary.
    concept_map_path = "Summary_concept_map.txt"  # The .txt file containing the concept map.
    output_image_path = "visual_map.png"  # Optional: specify a different output path.

    visual_map_handler = VisualMapHandler(summary_path, concept_map_path, output_image_path)
    visual_map_handler.process()

