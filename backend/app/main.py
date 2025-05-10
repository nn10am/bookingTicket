from fastapi import FastAPI
from .db.base import Base
from .db.session import engine
from .controllers.userController import router as user_router
from .controllers.authController import router as auth_router
from .controllers.eventController import router as event_router

from .models import bookingModel, eventModel, userModel, tempReserveModel

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(event_router)


# Root
@app.get("/")
def root():
    return {"message": "Booking Ticket API is up and running!"}


Base.metadata.create_all(bind=engine)
