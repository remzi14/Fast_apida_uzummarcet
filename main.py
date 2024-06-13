from fastapi import FastAPI,Depends,HTTPException,status

import product_routes
from auth_routes import auth_router
from schemas import Setting
from fastapi_jwt_auth import AuthJWT
from product_routes import product_routes


app=FastAPI()
app.include_router(auth_router)
app.include_router(product_routes)


@AuthJWT.load_config
def get_config():
    return Setting()








@app.get("/")
async def root(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Saytga hali kirmagansiz")
    return {"message":"Bosh sahifa"}









