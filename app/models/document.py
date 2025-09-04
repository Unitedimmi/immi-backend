from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    email: str
    filename: str
    visa_type: str      
    status: Optional[str] = "Pending"  # status like "Submitted", "Reviewed", etc.
    file_data: bytes
