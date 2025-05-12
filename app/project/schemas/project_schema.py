from pydantic import BaseModel, validator

class CreateProjectRequest(BaseModel):
    name: str

