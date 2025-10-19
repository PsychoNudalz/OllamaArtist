from pydantic import BaseModel


class ImageOrder(BaseModel):
    Text: str = ""
    Style: str = ""
    Age: int = 0
    Seed: int = 0
    Width: int = 720
    Height: int = 720

    def to_json(self) -> str:
        """Return a JSON string representation of the model."""
        # Pydantic’s json() already gives a pretty‑printed string.
        # If you prefer a compact form, use ensure_ascii=False.
        return self.model_dump_json(indent=None, ensure_ascii=False)

    @staticmethod
    def to_string_prompt_format() -> str:
        fields = ImageOrder.model_fields  # Pydantic v2
        field_list = [f"{name}: {field.annotation.__name__}" for name, field in fields.items()]
        fields_str = ", ".join(field_list)
        return fields_str

    def to_prompt(self) -> str:
        prompt = f"{self.Text}, (({self.Style}))"
        if self.Age > 0:
            prompt += f", aged by {self.Age} years"
        return prompt
