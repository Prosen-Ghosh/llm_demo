# Use Python 3.12 with arm64 architecture
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install PyTorch for M1/MPS (arm64 compatible)
RUN pip install --no-cache-dir \
    torch \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Copy the training script
COPY train.py .

# Create a non-root user
RUN useradd -m -u 1000 trainer
USER trainer

# Set environment variables for MPS
ENV PYTORCH_ENABLE_MPS_FALLBACK=1
ENV HF_HOME=/app/.cache/huggingface
ENV TORCH_USE_CUDA_DSA=1

# Run the training script
CMD ["python", "train.py"]