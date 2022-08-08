from fastapi import FastAPI
import statements
from fastapi.openapi.utils import get_openapi
app = FastAPI(title="Statements API", redoc_url="/")


@app.get("/statement")
def statement(c_id: str, p_id: str):
    return statements.parse_statement(c_id, p_id)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return "No Favicon :)"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Statements API",
        version="1.3",
        description="",
        routes=app.routes
    )
    # print(openapi_schema)
    openapi_schema["info"]["x-logo"] = {
        "url": "logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
