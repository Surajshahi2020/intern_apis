# Use the official Ubuntu 20.04 image as the base
FROM ubuntu:20.04

# Update package lists and install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy the Python script file from your host into the container
COPY . .

# Install dependencies using pip
RUN pip install -r requirements.txt

# Set an environment variable (not used in this example)
ENV MY_ENV_VAR=my_value

# Specify the Django server command as the default command
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
