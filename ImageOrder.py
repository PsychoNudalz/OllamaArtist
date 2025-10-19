from pydantic import BaseModel

class ImageOrder(BaseModel):
    Text: str = ""
    Style: str = ""
    Age: int = 0
    Seed: int = 0
    Width: int = 512
    Height: int = 512

    def to_json(self) -> str:
        """Return a JSON string representation of the model."""
        # Pydantic’s json() already gives a pretty‑printed string.
        # If you prefer a compact form, use ensure_ascii=False.
        return self.model_dump_json(indent=None, ensure_ascii=False)
    @staticmethod
    def to_string_prompt()-> str:
        fields = ImageOrder.model_fields  # Pydantic v2
        field_list = [f"{name}: {field.annotation.__name__}" for name, field in fields.items()]
        fields_str = ", ".join(field_list)
        return fields_str