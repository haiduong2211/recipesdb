# Use a base image
FROM python:3.9-slim

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Update system and install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && apt-get clean

# Install Apache Airflow
RUN pip install apache-airflow

# Create the Airflow home directory
RUN mkdir -p $AIRFLOW_HOME

# Set the working directory
WORKDIR $AIRFLOW_HOME

# Expose port 8080 for the webserver
EXPOSE 8080

# Entry point for the container
CMD ["airflow", "standalone"]