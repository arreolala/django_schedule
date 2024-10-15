# Use an official Python runtime as a parent image  
FROM python:3.9-slim  

# Set the working directory in the container  
WORKDIR /usr/src/app  

# Copy the requirements file into the container  
COPY requirements.txt ./  

# Install any needed packages specified in requirements.txt  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the current directory contents into the container at /usr/src/app  
COPY . .  

# Make port 8000 available for our app, for local usage  
EXPOSE 8000  

# Define environment variable to specify the Django settings module  
ENV DJANGO_SETTINGS_MODULE=schedule_project.settings  

# Run the application server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
