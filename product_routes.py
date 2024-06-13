
from fastapi import APIRouter,Depends
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
from schemas import SignUpModel,LoginModel,OrderModel
from models import User,Product,Order
from database import session,Base,engine
from fastapi import HTTPException,status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from schemas import Product

session = scoped_session(sessionmaker(bind=engine))

product_routes=APIRouter(
    prefix="/product"
)


@product_routes.post("/crete",status_code=status.HTTP_201_CREATED)
async def create_product(product:Product,Authorize=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is None")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.id_staff:
        new_product=Product(
            name=product.name,
            price=product.price
        )

        new_product.user=user
        session.add(new_product)
        session.commit()

        response={
            "status":status.HTTP_201_CREATED,
            "message":"Succesfuly created product",
            "data":{
                "name":new_product.name,
                "price":new_product.price
            }
        }

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Bu saxifa faqat admin uchun")



#product delete



@product_routes.delete("/{id}/delete",status_code=status.HTTP_200_OK)
async def product_delete(id:int,Authorize=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is None")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        product=session.query(Product).filter(Product.id==id).first()
        if product:
            session.delete(product)
            session.commit()
            respnse={
                "message":"OK",
                "status":200


            }


            return jsonable_encoder(respnse)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product {id} not found")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only Superuser is allowed to product")




#Product list uchun cod

@product_routes.get("/list",status_code=status.HTTP_200_OK)
async def product_list(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Acces token is None")

    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()
    if current_user.is_staff:
        product=session.query(Product).all()
        response={
            "message":'Ok',
            "status":status.HTTP_200_OK,
            "data":product
        }

        return jsonable_encoder(response)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Product list not this user')


