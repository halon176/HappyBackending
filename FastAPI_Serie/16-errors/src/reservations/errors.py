from pydantic import BaseModel



class NotFoundReservationError(BaseModel):
    detail: str = "Reservation not found"