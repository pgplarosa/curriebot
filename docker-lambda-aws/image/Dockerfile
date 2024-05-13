FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy all files scripts and data
COPY src/* ${LAMBDA_TASK_ROOT}/
COPY raw/ ${LAMBDA_TASK_ROOT}/raw/
COPY vector_db/ ${LAMBDA_TASK_ROOT}/vector_db/

RUN ls -latr ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler.
CMD [ "main.handler" ]
