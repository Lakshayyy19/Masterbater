# import subprocess
# import threading

# def run_fastapi():
#     subprocess.run(["python", "fastapi_app.py"])

# def run_gradio():
#     subprocess.run(["python", "gradio_app.py"])

# if __name__ == "__main__":
#     fastapi_thread = threading.Thread(target=run_fastapi)
#     fastapi_thread.start()
#     run_gradio()

# run_both.py
import threading
import uvicorn
from fastapi_app import app as fastapi_app
from gradio_app import demo as gradio_demo

# Function to run FastAPI
def run_fastapi():
    # Bind to 0.0.0.0 so Docker can expose the port
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start FastAPI in a daemon thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Start Gradio in main thread, binding to 0.0.0.0 for Docker
    gradio_demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
