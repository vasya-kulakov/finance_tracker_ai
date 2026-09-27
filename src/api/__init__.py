from fastapi import APIRouter
from .admin import router as admin_router
from .family import router as family_router
from .test import router as test_router
from .transactions import router as trans_router
from .grade import router as grade_router

main_router = APIRouter()

main_router.include_router(admin_router)
main_router.include_router(family_router)
main_router.include_router(test_router)
main_router.include_router(trans_router)
main_router.include_router(grade_router)


