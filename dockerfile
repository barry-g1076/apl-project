# Base image with both Python and Node.js
FROM python:3.12-bookworm

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Create working directory
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY package.json package-lock.json* ./
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Node.js dependencies
RUN if [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

# Copy the rest of the application
COPY . .

# Build frontend if needed (uncomment if you have a build step)
# RUN npm run build

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app:app"]