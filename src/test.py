from pydantic import BaseModel, HttpUrl


class Base(BaseModel):
    title: str
    data: str
    number: int


b = Base(title="sgas", data="aga", number=1)
match b:
    case b.title:
        print("Hello world")
    case b.data:
        print("Bye-bye world")
    case _:
        print("What is it")


print(HttpUrl("https://storage.yandexcloud.net/clothing-store/dacf817d-da36-47fe-ab39-2881b3f0a590/lion-removebg-preview.png?AWSAccessKeyId=YCAJELU7ww0Zb0a-lcECoB45i&Signature=xJBEQ2OxXILjN66bvxv0SBHBw28%3D&Expires=1754463451"))