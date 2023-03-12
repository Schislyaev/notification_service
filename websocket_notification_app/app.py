import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import create_connection, notification
from core.settings import settings

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/docs',
    openapi_url='/api/docs.json',
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            'name': settings.project_name,
            'description': 'Send notifications by websocket',
        },
    ]
)


app.include_router(notification.router, prefix='/api/v1', tags=['Notifications'])
app.include_router(create_connection.router, prefix='/api/v1', tags=['Notifications socket'])


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
