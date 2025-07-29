from pydantic import BaseModel, Field


class Base(BaseModel):
    name: str = Field()


b = Base(name="sags")
print(b.model_dump_json())
