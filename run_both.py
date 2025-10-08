import subprocess
import threading

def run_fastapi():
    subprocess.run(["python", "fastapi_app.py"])

def run_gradio():
    subprocess.run(["python", "gradio_app.py"])

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()
    run_gradio()