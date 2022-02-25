from flask import json
from werkzeug.exceptions import HTTPException

from app import create_app

app = create_app()


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    print(response, "asd")
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )

    response.content_type = "application/json"
    return response
