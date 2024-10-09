from pipeline.pipeline_manager import PipelineManager

video_file_path = "videos/Semana1/Webinar_Bienvenida.webm"
pipeline_manager = PipelineManager(video_file_path)
pipeline_manager.run()
