import gradio as gr
import requests
from PIL import Image
import io, base64, os, json

API_URL = "http://127.0.0.1:8000/"

# --- Gradio UI ---
def gr_process_via_http(image):
    btn_update = gr.update(interactive=False, value="Processing...")
    yield None, None, btn_update

    if image is None:
        yield gr.update(value=None, visible=True), gr.update(value="Please upload an image.", visible=True),gr.update(interactive=True, value="Run Prediction")
        return

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    try:
        files = {"file": ("image.png", buf, "image/png")}
        resp = requests.post(API_URL, files=files, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        yield gr.update(value=None, visible=True), gr.update(value=f"❌ Error calling API: {e}", visible=True), gr.update(interactive=True, value="Run Prediction")
        return

    output_image_b64 = data.get("output_image_b64")
    output_image = None
    if output_image_b64:
        img_bytes = base64.b64decode(output_image_b64.split(",")[1])
        output_image = Image.open(io.BytesIO(img_bytes))

    json_text = json.dumps(data["result"], indent=4)
    yield gr.update(value=output_image, visible=True), gr.update(value=json_text, visible=True),gr.update(interactive=True, value="Run Prediction")
    # return gr.update(value=output_image, visible=True), gr.update(value=json_text, visible=True)
    # return output_image, json_text,gr.update(visible=True), gr.update(visible=True)


# with gr.Blocks(title="🧠 Object detection tool") as demo:
#     gr.Markdown("## 🖼️ Upload an Image to Run Prediction")

#     with gr.Row():
#         image_input = gr.Image(type="pil", label="Upload Image")
#         process_button = gr.Button("Process Image", variant="primary")
#         clear_button = gr.Button("Clear")

#     with gr.Row():
#         image_output = gr.Image(label="Processed Output Image", visible=False)
#         json_output = gr.Textbox(label="Predicted JSON Output", lines=20, visible=False)

#     process_button.click(
#         fn=gr_process_via_http,
#         inputs=image_input,
#         outputs=[image_output, json_output, process_button],
#         show_progress=True
#     )
#     clear_button.click(
#         fn=lambda: (
#             gr.update(value=None, visible=False),  
#             gr.update(value=None, visible=False),  
#             gr.update(value=None)                  
#         ),
#         inputs=None,
#         outputs=[image_output, json_output, image_input],
#     )


# if __name__ == "__main__":
#     demo.launch()

# --- Gradio UI ---
with gr.Blocks(title="🧠 Object Detection Tool", css="""
.my-btn button {
    font-size: 16px;
    padding: 12px 25px;
    border-radius: 8px;
    font-weight: bold;
}
.section-box {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #eee;
    background-color: #fafafa;
}
.my-btn + .my-btn {
    margin-left: 10px; /* space between buttons */
}
.main-title {
    text-align: center;   /* center the title */
    font-size: 32px;      /* bigger font */
    font-weight: bold;
    margin-bottom: 10px;
}
""") as demo:
    
    # gr.Markdown("## 🖼️ Object Detection Tool")
    gr.Markdown("<h1 class='main-title'>🖼️ Object Detection Tool</h1>", elem_classes=["main-title"])
    gr.Markdown("Upload an image, click **Process Image**, and view the detected objects and processed image.")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group(elem_classes="section-box"):
                gr.Markdown("### Step 1: Upload Image")
                image_input = gr.Image(type="pil", label="Upload Image")
                gr.Markdown("Supported formats: JPG, PNG. Max size: 5MB.")
                process_button = gr.Button("PROCESS IMAGE", variant="primary", elem_classes=["my-btn"])
                clear_button = gr.Button("CLEAR", variant="secondary", elem_classes=["my-btn"])
        
        with gr.Column(scale=1):
            with gr.Group(elem_classes="section-box"):
                gr.Markdown("### Step 2: View Outputs")
                image_output = gr.Image(label="Processed Output Image", visible=False)
                json_output = gr.Textbox(label="Predicted JSON Output", lines=8, visible=False, interactive=False)
    

    process_button.click(
        fn=gr_process_via_http,
        inputs=[image_input],
        outputs=[image_output, json_output, process_button],
    )

    clear_button.click(
        fn=lambda: (
            gr.update(value=None, visible=False),
            gr.update(value=None, visible=False),
            gr.update(value=None)
        ),
        inputs=None,
        outputs=[image_output, json_output, image_input],
    )

if __name__ == "__main__":
    demo.launch()
    # demo.launch(share=True)
