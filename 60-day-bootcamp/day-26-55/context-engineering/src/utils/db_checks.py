import weaviate
import psycopg2
import redis
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_weaviate():
    url = os.getenv("WEAVIATE_URL")
    print(f"Checking Weaviate at {url}...")

    try:
        client = weaviate.connect_to_local()
        is_ready = client.is_ready()
        client.close()

        if is_ready:
            print("✅ Weaviate is ready.")
            return True
        else:
            print("❌ Weaviate is not ready.")
            return False
    except Exception as e:
        print(f"❌ Weaviate error: {e}")
        return False
    
def check_postgres():
    dsn = os.getenv("POSTGRES_DSN")
    print("Checking Postgres...")

    try:
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        print("✅ Postgres is ready.")
        return True
    except Exception as e:
        print(f"❌ Postgres error: {e}")
        return False


def check_redis():
    url = os.getenv("REDIS_URL")
    print("Checking Redis...")
    try:
        r = redis.from_url(url)
        r.ping()
        print("✅ Redis is ready.")
        return True
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def check_ollama():
    url = os.getenv("OLLAMA_URL")
    print(f"Checking Ollama at {url}...")
    try:
        # Ollama root endpoint usually returns "Ollama is running"
        res = requests.get(f"{url}")
        if res.status_code == 200:
            print("✅ Ollama is ready.")
            return True
        else:
            print(f"❌ Ollama returned status {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False

if __name__ == "__main__":
    checks = [check_weaviate(), check_postgres(), check_redis(), check_ollama()]
    if all(checks):
        print("\n🚀 All systems operational!")
    else:
        print("\n⚠️  Some systems failed.")
        exit(1)