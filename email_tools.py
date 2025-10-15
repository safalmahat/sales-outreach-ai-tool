from agents import function_tool
import sendgrid
from sendgrid.helpers.mail import Mail,Email,To,Content 
import os

@function_tool
def send_email(body: str):
    """ Send out an email with the given body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SANDGRID_API_KEY'))
    from_email = Email("")  # Change to your verified sender
    to_email = To("")  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Sales email", content).get()
    sg.client.mail.send.post(request_body=mail)
    print(mail)
    return {"status": "success"}