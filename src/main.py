from fastapi import FastAPI
from starlette.responses import RedirectResponse

from items.views import items

app = FastAPI(
    title="FastAPI",
    description="Template for FastAPI projects",
    version="0.1.0",
)
app.include_router(items)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
