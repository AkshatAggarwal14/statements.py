from fastapi import FastAPI
import statements
from fastapi.openapi.utils import get_openapi
app = FastAPI(title="Statements API", redoc_url="/")


@app.get("/statement")
async def statement(c_id: str, p_id: str):
    resp = await statements.parse_statement(c_id, p_id)
    return resp


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Statements API",
        version="1.1",
        description="",
        routes=app.routes,
    )
    print(openapi_schema["info"])
    openapi_schema["info"]["x-logo"] = {
        "url": "https://i.ibb.co/zhW9Q8c/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
