import json
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi.encoders import jsonable_encoder

class JSendRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            result = await original_handler(request)

            
            if isinstance(result, Response):
                try:
                    data = json.loads(result.body.decode())
                except Exception:
                    data = None
            else:
                data = jsonable_encoder(result)

            if isinstance(data, list):
                payload = {
                    "status": "success",
                    "data": {
                        "items": data
                    }
                }
            else:
                payload = {
                    "status": "success",
                    "data": {
                        "user": data
                    }
                }

            return Response(
                content=json.dumps(payload),
                media_type="application/json"
            )

        return custom_handler
