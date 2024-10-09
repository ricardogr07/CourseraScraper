from pipeline.pipeline_manager import PipelineManager

transcript_path = "videos/Semana1/Pregunta_Investigacion_transcript.txt"

pipeline_manager = PipelineManager(transcript_path=transcript_path)
pipeline_manager.run_from_transcript()
