from ninja import NinjaAPI
from apps.library.api import router as library_router

api = NinjaAPI(
    title="Library Management API",
    version="1.0.0",
    description="Учебный проект API для управления библиотекой (Лабораторная работа №1)"
)

api.add_router("/", library_router)