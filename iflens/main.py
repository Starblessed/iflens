import os
import base64

from random import random
from datetime import datetime

from dotenv import load_dotenv

from google import genai
from groq import Groq

from iflens.schema.conditions import ConditionSchema
from iflens.functions.classification import classify_image
from iflens.functions.generation import BASE_GENERATION_PROMPT

from iflens.utils import time_signed_print as print

def check_env_keys():
    keys_to_check = [
        ("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")),
        ("GROQ_API_KEY", os.getenv("GROQ_API_KEY")),
    ]
    
    for name, value in keys_to_check:
        if not value or value == "YOUR_KEY_HERE":
            raise ValueError(f"No {name} found inside .env!")
        
def get_file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1]

def is_image(filename: str) -> bool:
    SUPPORTED_IMAGE_FORMATS: list[str] = [".png", ".jpeg", ".jpg"]
    
    ext = get_file_ext(filename=filename)
    return ext.lower() in SUPPORTED_IMAGE_FORMATS

if __name__ == "__main__":
    
    NUMBER_OF_SAMPLE_IMAGES: int = 1 # Should be equal or smaller than the dataset size
    
    DATASET_PATH: str = os.path.join("examples", "street")
    CONDITIONS_YAML_FILE: str = "conditions-example.yaml"
    
    KEEP_CLASSES: list[str] = ["planet"] # Prevents the tool from varying specific condition classes
    
    GENERATION_MODEL: str = "gemini-3.1-flash-lite-image"
    
    load_dotenv()
    check_env_keys()
    
    print("STEP 0 --- SETUP")
    
    print("- Checking if input and output directories exist")
    
    if not os.path.exists("input"):
        print("- Creating input directory...")
        os.mkdir("input")
    else: print("- Input OK")
        
    if not os.path.exists("output"):
        print("- Creating output directory...")
        os.mkdir("output")
    else: print("- Output OK")
            
    print("- Done!")
        
    print("STEP 1 --- SAMPLING IMAGES TO AUGMENT")
    
    print("- Fetching images...")
    
    images = [f for f in os.listdir(DATASET_PATH) if is_image(f)]
    
    print(f"- {len(images)} images found")
    
    print(f"- Sampling {NUMBER_OF_SAMPLE_IMAGES} images...")
    
    sampled = []
    
    from random import choice
    for i in range(NUMBER_OF_SAMPLE_IMAGES):
        chosen_img = choice(images)
        images.remove(chosen_img)
        
        sampled.append(chosen_img)
        
    print(f"- Sampled {len(sampled)} images.")
    
    print("STEP 2 --- Creating folder with sampled images and annotations")
    
    experiment_time: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    experiment_origin: str = "input"
    experiment_folder: str = os.path.join(experiment_origin, f"{experiment_time}")
    
    os.makedirs(experiment_folder, exist_ok=True)
    
    import shutil
    
    for sample_img in sampled:
        print(f"- Copying image {sample_img}")
        try:
            img_path = os.path.join(DATASET_PATH, sample_img)
            annotation = os.path.splitext(img_path)[0] + ".txt"
            
            shutil.copy(img_path, os.path.join(experiment_folder, sample_img))
            shutil.copy(annotation, os.path.join(experiment_folder, os.path.basename(annotation)))
            
            print("- Done")
        except Exception as e:
            print(f"- Error: {repr(e)}")
            print(f"Skipping...")
    
    print(f"- {len(os.listdir(experiment_folder))} files in experiment folder (expected: {2*NUMBER_OF_SAMPLE_IMAGES})")
    
    print("- STEP 3 --- Generating Augmentations")
    
    client = genai.Client()
    groq_client = Groq()
    
    images = [f for f in os.listdir(experiment_folder) if is_image(f)]
    
    output_folder: str = os.path.join("output", f"{experiment_time}")
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"- Ready to augment {len(images)} images")
    schema = ConditionSchema.from_yaml(path=CONDITIONS_YAML_FILE)
    
    print("[!] Initializing Pipeline...")
    
    for i, image in enumerate(images):
        try:
            print(f"({i+1}/{len(images)})", f"- Image {image}")
            in_filename = os.path.join(experiment_folder, image)
            out_filename = os.path.join(output_folder, f"AUG_{os.path.splitext(image)[0]}.png")
            
            print(f"({i+1}/{len(images)})", "- Classifying image...")

            conditions = classify_image(in_filename, schema, groq_client)
            variation = conditions.get_variation(keep=KEEP_CLASSES)
            
            print(f"({i+1}/{len(images)})", f"- Original Conditions: {conditions.to_prompt()}")
            print('-'*20)
            print(f"({i+1}/{len(images)})", f"- Variation Conditions: {variation.to_prompt()}")
            
            print(f"({i+1}/{len(images)})", "- Preparing image...")
            
            with open(in_filename, "rb") as f:
                image_bytes = f.read()

            print(f"({i+1}/{len(images)})", "- Generating variation...")

            interaction = client.interactions.create(
                model=GENERATION_MODEL,
                input=[
                    {
                    "type": "text",
                    "text": BASE_GENERATION_PROMPT + variation.to_prompt()
                    },
                    {
                        "type": "image",
                        "data": base64.b64encode(image_bytes).decode('utf-8'),
                        "mime_type": "image/png"
                    }
                ],
            )
            assert interaction.output_image and interaction.output_image.data, "Generated image is None!"

            print(f"({i+1}/{len(images)})", f"- Generated successfully! Saving to: {out_filename}")
            
            with open(out_filename, "wb") as f:
                f.write(base64.b64decode(interaction.output_image.data))
                
            print(f"({i+1}/{len(images)})", "- Done!")
        except Exception as e:
            print(f"({i+1}/{len(images)})", f"- Error: {repr(e)}")
            print(f"({i+1}/{len(images)})", "Skipping...")
            continue
