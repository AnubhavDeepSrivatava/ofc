from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = {
            "code": ErrorCodes.value_required if error["type"] == "missing" else ErrorCodes.invalid_input,
            "message": error["msg"]
        }
    return JSONResponse(status_code=400, content={"status": "fail", "data": errors})


async def logic_exception_handler(request: Request, exc: logic_exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "fail", 
            "data": { "code": exc.code, "message": exc.message}
        }
    )

