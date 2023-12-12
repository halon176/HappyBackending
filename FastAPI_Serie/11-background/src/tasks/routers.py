from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databese import get_async_session
from src.security import JWTBearer
from src.tasks.tasks import send_email_report_dashboard
from src.users.models import User

router = APIRouter(prefix="/report")


@router.get("/user")
async def get_user_report(background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session),
                          user_id: int = Depends(JWTBearer())):
    query = select(User).where(User.id == user_id)
    user: User = await session.scalar(query)

    # comando di esecuzione sincrona
    # send_email_report_dashboard(user.__json__())

    # comando di esecuzione con BackgroundTasks di fastapi
    background_tasks.add_task(send_email_report_dashboard, user.__json__())

    # comando di esecuzione con Celery, lui lo serializza da solo ma se anche qui aggiungete __json__() non cambia
    #send_email_report_dashboard.delay(user)
    return {"message": "La richiesta è stata accettata e la mail verrà inviata a breve."}
