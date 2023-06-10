from fastapi import FastAPI
import statements
from fastapi.openapi.utils import get_openapi
app = FastAPI(title="Statements API", redoc_url="/")


@app.get("/statement/{contest_id}/{problem_id}")
async def statement(contest_id: str, problem_id: str):
    resp = await statements.parse_statement(contest_id, problem_id)
    return resp


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return "No Favicon :)"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Statements API",
        version="2.0",
        description="",
        routes=app.routes
    )
    # print(openapi_schema)
    openapi_schema["info"]["x-logo"] = {
        "url": "https://i.ibb.co/zhW9Q8c/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
