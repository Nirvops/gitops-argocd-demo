# 1. Use the lightest and safest official image for Python (https://hub.docker.com/_/python)
FROM python:3.12-slim

# 2. Add metadata to the image to indicate the source repository
LABEL org.opencontainers.image.source=https://github.com/Nirvops/gitops-argocd-demo

# 3. Define the working directory (place where the code will be copied)
WORKDIR /app

# 4. Copy and install dependencies (from requirements.txt for cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code
COPY . .
EXPOSE 5000

# 6. Setup an app user so the container doesn't run as the root user
RUN useradd --no-create-home --shell /usr/sbin/nologin app
USER app

# 7. Launch the application
CMD ["python3", "app.py"]
