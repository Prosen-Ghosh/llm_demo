import time
import requests
import psutil
from prometheus_client import start_http_server, Gauge, Enum

# --- CONFIG ---
OLLAMA_URL = "http://host.docker.internal:11434"
POLLING_INTERVAL = 5

# --- METRICS ---
# 1. Gauge: How much RAM (RSS) is Ollama using?
OLLAMA_MEMORY = Gauge('ollama_memory_usage_bytes', 'Memory used by Ollama process')

# 2. Gauge: CPU % of the Ollama process
OLLAMA_CPU = Gauge('ollama_cpu_percent', 'CPU usage percent of Ollama process')

# 3. Enum: Which model is currently loaded? (Powerful feature!)
# Enums in Prometheus allow you to map string states to values.
ACTIVE_MODEL = Gauge('ollama_loaded_model_info', 'Info about loaded model', ['model_name'])

def find_ollama_process():
    """Finds the process ID (PID) of the Ollama runner."""
    for proc in psutil.process_iter(['pid', 'name']):
        # On Mac it might be 'ollama', on Linux 'ollama_llama_server'
        if 'ollama' in proc.info['name'].lower():
            return proc
    return None

def scrape_metrics():
    # 1. System Level Metrics (via psutil)
    proc = find_ollama_process()
    if proc:
        try:
            # RSS = Resident Set Size (Physical RAM)
            mem_info = proc.memory_info()
            OLLAMA_MEMORY.set(mem_info.rss)
            
            # CPU Percent
            OLLAMA_CPU.set(proc.cpu_percent(interval=None))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    # 2. Application Level Metrics (via Ollama API)
    try:
        # /api/ps tells us what models are loaded in memory
        response = requests.get(f"{OLLAMA_URL}/api/ps", timeout=2)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            # Reset previous labels (simple approach)
            ACTIVE_MODEL._metrics.clear() 
            
            if models:
                for m in models:
                    name = m.get('name')
                    # Set value to 1 to indicate "Present"
                    ACTIVE_MODEL.labels(model_name=name).set(1)
                    
                    # You could also extract VRAM usage from here if available
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

if __name__ == '__main__':
    # Start the Prometheus metrics server on port 9877
    print("Starting Ollama Exporter on port 9877...")
    start_http_server(9877)
    
    while True:
        scrape_metrics()
        time.sleep(POLLING_INTERVAL)