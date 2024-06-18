FROM python:3.10

# Set the working directory
WORKDIR /code

# Copy the requirements.txt file into the working directory
COPY ./requirements.txt /code/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the backend code into the working directory
COPY ./Backend /code/Backend

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python3", "Backend/main.py"]
