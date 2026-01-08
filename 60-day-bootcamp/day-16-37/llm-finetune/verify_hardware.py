import torch

if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✅ Success: Apple MPS (Metal Performance Shaders) detected.")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("⚠️ Surprise: CUDA detected (Excellent!)")
else:
    device = torch.device("cpu")
    print("⚠️ Standard Mode: Using CPU (Slower, but functional).")