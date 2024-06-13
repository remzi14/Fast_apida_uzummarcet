from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username :str
    email :str
    password:Optional[str]
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra ={
            "example":{
                "username":"eshmat",
                "email":"eshmat@gmail.com",
                "password":"eshmat123",
                "is_staff":False,
                "is_active":True,

            }
        }





class LoginModel(BaseModel):
    username_or_email:str
    password:str




    class Config:
        from_attributes=True
        json_schema_extra ={
            "example":{
                "username":"eshmat",
                "password":"eshmat123",
            }
        }




class Setting(BaseModel):
    authjwt_secret_key:str="'d99abb8f90dcf1c0e873d50c8835b83c06640e79d05d26d0673c103bd519e71b'"






class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="pending"
    user_id:Optional[int]



    class Config:
        from_attributes=True
        json_schema_extra ={
            "example":{
                "id":1,
                "quantity":2,
                "order_status":"pending",
                "user_id":1247651,
            }
        }




class Product(BaseModel):
    id:Optional[int]
    name = str
    price = int


    class Config:
        from_attributes=True
        json_schames_extra={
            'example':{
                "name":"shashlik",
                "price":20000,
            }
        }







