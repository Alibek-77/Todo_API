from fastapi import FastAPI
from database import Base,engine
from routers import auth,todos
from pathlib import Path
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter
import logging
app=FastAPI(title="Student API",description="API for control students",version="1.0.0")
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
Base.metadata.create_all(bind=engine)
log_path=Path("logs")/"app.log"
log_path.parent.mkdir(exist_ok=True,parents=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),                    
        logging.FileHandler("logs/app.log")             
    ]
)
app.include_router(auth.router)
app.include_router(todos.router)
@app.get("/",tags=["Health"])
def health_check():
    return {"status":"ok","version":"1.0.0"}
