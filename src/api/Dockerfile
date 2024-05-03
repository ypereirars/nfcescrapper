ARG PYTHON_VERSION=3.11.7

FROM python:${PYTHON_VERSION}-slim as base

# Set webdriver environment variables
ENV LOCAL_BIN_PATH=/usr/local/bin

# Update the package list and install the required dependencies and Firefox webdriver.
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget curl unzip build-essential \
    && rm -fr /var/lib/apt/lists/* \
    && apt-get autoremove -y

WORKDIR /api

# Copy the source code into the container.
COPY requirements.txt .

# Install the application's dependencies.
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

# Expose the port that the application listens on.
EXPOSE 80
