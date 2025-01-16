from fastapi import FastAPI

from app.settings import get_settings
from app.routers.users import router as users_router
from app.routers.authentication import router as authentication_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router

settings = get_settings()


def create_app():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    app.include_router(authentication_router,prefix='/auth',tags=["Authentication"])
    app.include_router(users_router, tags=["Users"])
    app.include_router(orders_router, tags=["Orders"])
    app.include_router(products_router, tags=["Products"])

    return app
