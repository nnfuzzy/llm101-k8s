FROM python:3.12-slim

# Set working directory in the container
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/ && \
    mv /root/.local/bin/uvx /usr/local/bin/

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies using uv
RUN uv pip install --no-cache -r requirements.txt --system

# Copy the rest of your application
COPY . .

# Expose the port Chainlit runs on
EXPOSE 8000

# Command to run the application
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000", "-h"]