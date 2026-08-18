# Use a lightweight Python image
FROM python:3.11-slim

# Specify work directory within the container. In this case, it's
# /app
WORKDIR /app

# Copy your code into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copies the actual application into the container.
# The first '.' designates the current directory to be copied into
# the current directory of the container, which is also specified by
# the second '.'
# This copies everything in /backend on your machine to /app in the
# container's directory
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the application, this is otherwise called the "entry point"
# or the point in the code where you run the application
CMD ["python", "run.py"]