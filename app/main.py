from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import List
from pydantic import BaseModel
import smtplib

# Initialize the app
app = FastAPI()

# Define the required data models
class User(BaseModel):
    username: str
    email: str
    password: str

class EmailTemplate(BaseModel):
    subject: str
    body: str

class EmailNotification(BaseModel):
    user: User
    template: EmailTemplate

# Create a list of users
users = [
    User(username="john", email="john@example.com", password="password"),
    User(username="jane", email="jane@example.com", password="password123")
]

# Create a list of email templates
templates = [
    EmailTemplate(subject="Welcome to our Service!", body="Thank you for registering with us! We hope you enjoy our service!"),
    EmailTemplate(subject="Password Reset", body="You recently requested to reset your password. Please click on the link below to reset your password.")
]

# Create an endpoint to send email notifications
@app.post("/send_email")
def send_email(notification: EmailNotification):
    # Connect to the SMTP server
    server = smtplib.SMTP("smtp.example.com")
    server.starttls()
    server.login("username", "password")

    # Send the email notification
    server.sendmail(
        notification.template.subject,
        notification.template.body,
        notification.user.email
    )

    # Close the connection
    server.quit()

    # Return success response
    return JSONResponse(
        status_code=200,
        content={"message": "Email notification sent successfully!"}
    )