from pipeline.pipeline_manager import PipelineManager

video_file_path = "path_to_your_video/video.webm"

pipeline_manager = PipelineManager(video_file_path=video_file_path)
pipeline_manager.run()
