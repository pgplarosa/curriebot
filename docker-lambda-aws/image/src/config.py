import os

bucket_name = "plarosa-portfolio-bot"
s3_folder_resume = "raw/resume/"
repo_name = "curriebot"
chroma_directory = "vector_db"
local_root = "/home/ubuntu/curriebot/docker-lambda-aws/image"
root_dir = os.environ.get("LAMBDA_TASK_ROOT", local_root)
temperature = 1
model_name = "gpt-4"