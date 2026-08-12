from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from pathlib import Path

import random
import yaml

from pprint import pprint
from tabulate import tabulate

@dataclass
class Condition:
    name: str
    prompt: str
    
@dataclass
class ConditionClass:
    name: str
    conditions: dict[str, Condition]
    
    def get(self, key: str) -> Condition:
        condition = self.conditions.get(key, None)
        if not condition:
            raise(ValueError(f"Invalid {self.name} condition: {key}"))
        
        return condition
    
    def get_random(self, exclude: list[str] | None = None) -> Condition:
        exclude = [] if not exclude else exclude
        return random.choice([condition for condition in self.conditions.values() if condition not in exclude])
    
@dataclass
class ConditionSchema:
    classes: dict[str, ConditionClass]
    
    def __getitem__(self, key: str) -> ConditionClass:
        condition_class = self.classes.get(key, None)
        if not condition_class:
            raise(ValueError(f"Invalid condition class: {condition_class}"))
        return condition_class
    
    @classmethod
    def from_yaml(cls, path: str | Path) -> ConditionSchema:
        with open(path, 'r', encoding='utf8') as f:
            raw = yaml.safe_load(f)
            
        classes = {}
        for class_name, values in raw.items():
            conditions = {
                condition_name: Condition(
                    name=condition_name,
                    prompt=str(prompt)
                    ) for condition_name, prompt in values.items()
            }
            
            classes[class_name] = ConditionClass(
                name=class_name,
                conditions=conditions
                )
        return cls(classes)
    
    def to_markdown(self):
        md = "# Schema\n\n"
        for condition_class in self.classes.values():
            rows = [[c.name, c.prompt] for c in condition_class.conditions.values()]
            
            table = tabulate(rows, headers=["Name", "Description"], tablefmt="github")
            
            md += f"## Attribute: {condition_class.name}\n\n{table}\n\n"
        
        return md
            

@dataclass
class ImageConditions:
    conditions: dict[str, Condition]
    schema: ConditionSchema
    
    @classmethod
    def from_dict(cls, schema: ConditionSchema, data: dict[str, str]):
        conditions = {class_name: schema[class_name].get(condition_name) for class_name, condition_name in data.items()}
        return cls(conditions=conditions, schema=schema)
    
    def get_variation(self, keep: list[str] | None = None) -> ImageConditions:
        keep = keep if keep else []
        variation = {}
        for condition_class in self.schema.classes.values():
            if condition_class.name in keep: continue
            value = self.conditions.get(condition_class.name)
            variation[condition_class.name] = condition_class.get_random(exclude=[value.name]).name if value else None
        return ImageConditions.from_dict(schema=self.schema, data=variation)
    
    def to_prompt(self):
        return "\n".join([condition.prompt for condition in self.conditions.values()])
            
if __name__ == "__main__":
    path = "conditions-example.yaml"
    
    schema = ConditionSchema.from_yaml(path=path)
    
    print(schema.to_markdown())