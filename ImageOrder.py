from typing import Any
from pydantic import BaseModel
import json

class ImageOrder(BaseModel):
    Text: str = ""
    Style: str = ""
    Age: int = 0

    def to_json(self) -> str:
        """Return a JSON string representation of the model."""
        # Pydantic’s json() already gives a pretty‑printed string.
        # If you prefer a compact form, use ensure_ascii=False.
        return self.model_dump_json(indent=None, ensure_ascii=False)