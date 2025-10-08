from pathlib import Path
import os
from utils.load_model import model
import json
from fastapi.responses import JSONResponse
from PIL import Image

output_folder = str(os.getcwd()/Path('output'))
image_output_f=output_folder+'\images'
json_output_f=output_folder+'\json'
os.makedirs(output_folder,exist_ok=True)
os.makedirs(image_output_f,exist_ok=True)
os.makedirs(json_output_f,exist_ok=True)

## core functions
def get_next_filename(base_folder):
    i = 1
    while (Path(base_folder) / f"{i}.png").exists():
        i += 1
    return str(Path(base_folder) / f"{i}.png")

def predict_output(image_path, output_filenm,model=model):
    results = model(image_path)
    output = results[0].to_json()
    json_data=json.loads(output)
    json_f=output_filenm.split('\\')[-1].replace('.png','.txt')
    json_path=os.path.join(json_output_f,json_f)
    with open(json_path, 'w') as f:
        json.dump(json_data, f,indent=4)
    results[0].save(output_filenm)
    # return {
    #         "result": json_data,
    #         "output_image": output_filenm,
    #         "json_file": json_path
    #     }
    annotated_img = results[0].plot()
    output_img = Image.fromarray(annotated_img[..., ::-1])

    return {
            "result": json_data,
            "output_image": output_img,
            "json_file": json_path
        }

def predict_image(image_path):
    output_filenm=get_next_filename(image_output_f)
    return predict_output(image_path,output_filenm)


