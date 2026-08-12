from groq import Groq
from iflens.schema.conditions import ConditionSchema, ImageConditions

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt

import base64
import json

VISION_MODEL = "qwen/qwen3.6-27b"

CLASSIFICATION_BASE_PROMPT = "Given the schema below, provide a JSON classifying each attribute of the image in the format {attribute: name}, where the name is not None, according to the available names:\n"

def __get_condition_classification_prompt(condition_schema: ConditionSchema) -> str:
    return CLASSIFICATION_BASE_PROMPT + condition_schema.to_markdown()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

@retry(stop=stop_after_attempt(3))
def classify_image(image_path: str,
                   condition_schema: ConditionSchema,
                   client: Groq,
                   model: str = VISION_MODEL) -> ImageConditions:
    base64_image = encode_image(image_path=image_path)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": __get_condition_classification_prompt(condition_schema=condition_schema)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )
    
    obj = completion.choices[0].message.content
    
    assert obj is not None, "No JSON provided in the response!"
    
    return ImageConditions.from_dict(schema=condition_schema, data=json.loads(obj))

if __name__ == "__main__":
    
    load_dotenv()
    client = Groq()
    condition_schema = ConditionSchema.from_yaml(path="conditions-example.yaml")
    
    image_path = r"examples\street\example.png"
    
    conditions = classify_image(image_path=image_path,
                                condition_schema=condition_schema,
                                client=client)
    
    print(conditions.to_prompt())
    
    print("-- Variation below --")
    
    print(conditions.get_variation().to_prompt())
    