# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies required for Chromium
RUN apt-get update && apt-get install -y \
    supervisor \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for Puppeteer
RUN useradd -m puppeteeruser && \
    mkdir -p /home/puppeteeruser/puppeteer && \
    chown -R puppeteeruser:puppeteeruser /home/puppeteeruser/puppeteer

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Adjust ownership for the entire app directory to the non-root user
RUN chown -R puppeteeruser:puppeteeruser /app

# Create a logs directory where the non-root user can write logs
RUN mkdir -p /app/logs && chown -R puppeteeruser:puppeteeruser /app/logs

# Ensure the permissions of the Flask app directories are correct (modify if necessary)
RUN chmod -R 755 /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Supervisor configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Adjust ownership for Supervisor configuration as well
RUN chown -R puppeteeruser:puppeteeruser /etc/supervisor

# Expose the ports the Flask apps will run on
EXPOSE 5005
# DO NOT EXPOSE 5555!

# Switch to the non-root user
USER puppeteeruser

WORKDIR /app/src

ENV FLAG=TUDCTF{FAKE_FLAG}

# Command to run Supervisor, which will manage both Flask servers
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
