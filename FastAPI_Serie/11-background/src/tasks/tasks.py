import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import settings
from src.users.models import User

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")

celery.conf.broker_connection_retry_on_startup = True


def get_email_template_profile_report(user_dict: dict):
    email = EmailMessage()
    email["Subject"] = "Report del Profilo Utente - EventONE"
    email["From"] = settings.smtp_user
    email["To"] = user_dict.get("email", "")

    email_body = (
        f'<div style="background-color: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; max-width: 600px; margin: auto; font-family: Arial, sans-serif;">'
        f'    <h1 style="color: #e74c3c; font-family: Verdana, sans-serif; margin-bottom: 15px;">Ciao, {user_dict.get("username", "")}!</h1>'
        f'    <p style="color: #2ecc71; font-size: 18px; margin-bottom: 20px; font-weight: bold;">Auguri di Buon Natale e Felice Anno Nuovo da tutto il team di EventONE! 🎄🎅</p>'
        f'    <p style="font-size: 18px; margin-bottom: 20px;">Grazie per utilizzare il nostro servizio. Ecco il tuo report del Profilo Utente:</p>'
        f'    <ul style="list-style-type: none; padding: 0; text-align: left; margin: 0 auto;">'
        f'        <li style="font-weight: bold; color: #333;">ID Utente: {user_dict.get("id", "")}</li>'
        f'        <li style="font-weight: bold; color: #333;">Username: {user_dict.get("username", "")}</li>'
        f'        <li style="font-weight: bold; color: #333;">Email: {user_dict.get("email", "")}</li>'
        f'        <li style="font-weight: bold; color: #333;">Amministratore: {"Sì" if user_dict.get("is_admin", False) else "No"}</li>'
        f'        <li style="font-weight: bold; color: #333;">Data di creazione: {user_dict.get("created_at", "")}</li>'
        f'    </ul>'
        f'    <p style="color: #2ecc71; font-size: 18px; margin-bottom: 20px; font-weight: bold;">Che il tuo Natale sia pieno di gioia e felicità!</p>'
        f'    <img src="https://media1.tenor.com/m/GiLLtCNCtksAAAAC/santa-cat-elf-cat.gif" alt="Gatto Natalizio" style="max-width: 100%; margin-top: 20px;">'
        f'</div>'
    )

    email.set_content(email_body, subtype="html")
    return email


@celery.task
def send_email_report_dashboard(user: dict):
    email = get_email_template_profile_report(user)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.smtp_user, settings.smtp_password.get_secret_value())
        server.send_message(email)
