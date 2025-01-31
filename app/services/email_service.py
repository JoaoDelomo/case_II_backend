import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"  # Servidor SMTP do Gmail
SMTP_PORT = 587
SMTP_USER = "teleconnect.verifier@gmail.com"  # E-mail oficial do site
SMTP_PASSWORD = "pmab eftg fyus clud"  # Senha do aplicativo (ou token SMTP)

def send_email(to_email: str, subject: str, body: str):
    """
    Envia um e-mail para o cliente.
    """
    try:
        # Configura o e-mail
        message = MIMEMultipart()
        message["From"] = SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Conecta ao servidor SMTP e envia o e-mail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        raise RuntimeError(f"Falha ao enviar e-mail: {str(e)}")
