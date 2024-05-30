from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from services.exceptions import EntityAlreadyExists, EntityNotExists, EntityNotFound


def exception_container(app: FastAPI) -> None:

    @app.exception_handler(EntityNotExists)
    async def entity_not_exists_exception_handler(
        request: Request, error: EntityNotExists
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"{error.entity}' não existe."},
        )

    @app.exception_handler(EntityAlreadyExists)
    async def entity_already_exists_exception_handler(
        request: Request, error: EntityAlreadyExists
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"'{error.entity}' existente."},
        )

    @app.exception_handler(EntityNotFound)
    async def entity_not_found_exception_handler(
        request: Request, error: EntityNotFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"A entidade '{error.entity}' não foi encontrada."},
        )
