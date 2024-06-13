
from fastapi import APIRouter,Depends
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
from schemas import SignUpModel,LoginModel,OrderModel
from models import User,Product,Order
from database import session,Base,engine
from fastapi import HTTPException,status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


session = scoped_session(sessionmaker(bind=engine))

order_routs=APIRouter(
    prefix="/order"
)



@order_routs.post("/make",status_code=status.HTTP_201_CREATED)
async def make_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Access token is None")


    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        id=order.id,
        quentity=order.quantity,
        status=order.order_status,
        user_id=order.user_id,

    )
    new_order.user=user
    session.add(new_order)
    session.commit()
    response={
        "status":status.HTTP_201_CREATED,
        "message":"Succcessfuly created Order",
        "quentity":new_order.quantity,
        "order_status":new_order.order_status,

    }
    return jsonable_encoder(response)









@order_routs.get("/list",status_code=status.HTTP_200_OK)
async def order_list(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Acces token is None")

    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()
    if current_user.is_staff:
        orders=session.query(Order).all()
        response={
            "message":'Ok',
            "status":status.HTTP_200_OK,
            "data":orders
        }

        return jsonable_encoder(response)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Order list not this user')



# Bittani olish uchun fuksiya

@order_routs.get("/{id}",status_code=status.HTTP_200_OK)
async  def get_one_order(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Acces token is None")
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id)
        response={
            "message":"Ok",
            "status":status.HTTP_200_OK,
            "data":Order,
        }

        return jsonable_encoder(response)


    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Order list not this user')



