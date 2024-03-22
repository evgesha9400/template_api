from fastapi import FastAPI
from starlette.responses import Response, RedirectResponse

from items.views import items

app = FastAPI(
    title="FastAPI",
    description="Template for FastAPI projects",
    version="0.1.0",
)
app.include_router(items)


# Docs redirect
@app.get(path="/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url="/docs")


# Health check for ECS
@app.get(path="/healthcheck", include_in_schema=False)
async def healthcheck():
    return Response(content="OK", status_code=200)