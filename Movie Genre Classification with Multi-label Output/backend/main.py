from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from pydantic import model_validator
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

if __package__:
    from .database.db_funs import get_all_data, save_data
    from .loader.load import mlb, model, tfidf
    from .preprocessing.preproces import preprocess_plot
    from .utils.logger import get_logger
else:
    from database.db_funs import get_all_data, save_data
    from loader.load import mlb, model, tfidf
    from preprocessing.preproces import preprocess_plot
    from utils.logger import get_logger

logger = get_logger(__name__)

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

app = FastAPI(title="My API")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = [
        {key: value for key, value in error.items() if key != "input"}
        for error in exc.errors()
    ]
    logger.warning(
        "Request validation failed for %s %s: %s",
        request.method,
        request.url.path,
        errors,
    )
    is_invalid_json = any(error.get("type") == "json_invalid" for error in errors)
    return JSONResponse(
        status_code=422,
        content={
            "message": (
                "Request body must be valid JSON. Use double quotes around keys "
                "and string values, and remove trailing commas or comments."
                if is_invalid_json
                else "Request validation failed."
            ),
            "detail": jsonable_encoder(errors),
        },
    )


class Item(BaseModel):
    name: str
    price: float

class MovieRequest(BaseModel):
    title: str = Field(..., min_length=1)
    plot: str = Field(..., min_length=1)

    @model_validator(mode="before")
    @classmethod
    def unwrap_data(cls, value: Any) -> Any:
        if isinstance(value, dict) and set(value) == {"data"}:
            return value["data"]
        return value


class MoviePredictionResponse(BaseModel):
    id: str
    title: str
    predicted_genres: list[str]
    # probabilities: dict[str, float]


class MovieHistoryResponse(BaseModel):
    id: str
    title: str
    plot: str
    predicted_genres: list[str]



@app.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/info")
def info(request: Request):
    client_host = request.client.host if request.client else None
    logger.info("Info request from %s", client_host or "unknown")
    return {
        "ip": client_host,
        "url": str(request.url),
        "method": request.method,
        "user_agent": request.headers.get("user-agent"),
    }


@app.get("/health")
@limiter.limit("5/minute")
def health(request: Request):
    return {"status": "ok"}


@app.post("/predict", response_model=MoviePredictionResponse)
@limiter.limit("5/minute")
def predict_movie(request: Request, data: MovieRequest) -> MoviePredictionResponse:
    client_host = request.client.host if request.client else "unknown"
    logger.info("Prediction requested by %s for title=%r", client_host, data.title)

    cleaned_plot = preprocess_plot(data.plot)
    plot_vector = tfidf.transform([cleaned_plot])
    probabilities = model.predict_proba(plot_vector)
    prediction = (probabilities >= 0.2).astype(int)
    predicted_genres = list(mlb.inverse_transform(prediction)[0])
    logger.info("Predicted genres for %r: %s", data.title, predicted_genres)

    saved_prediction = save_data(
        {
            "title": data.title,
            "plot": data.plot,
            "predicted_genres": predicted_genres,
        }
    )
    movie_id = str(saved_prediction["[INFO]"])
    logger.info("Saved prediction with id=%s", movie_id)

    return MoviePredictionResponse(
        id=movie_id,
        title=data.title,
        predicted_genres=predicted_genres,
    )

  
@app.get("/history")
def history():
    movies = get_all_data()["[INFO]"]
    logger.info("Retrieved %d prediction records", len(movies))
    return {"History": movies}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)