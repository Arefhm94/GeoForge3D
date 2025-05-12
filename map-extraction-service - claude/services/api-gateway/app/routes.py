from fastapi import APIRouter
from services.user_service.app.routers import auth, users
from services.map_service.app.routers import maps, geojson
from services.payment_service.app.routers import payments

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(maps.router, prefix="/maps", tags=["maps"])
router.include_router(geojson.router, prefix="/geojson", tags=["geojson"])
router.include_router(payments.router, prefix="/payments", tags=["payments"])