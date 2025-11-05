from fastapi import FastAPI
from pydantic import BaseModel
import openai, stripe, os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_KEY")
stripe.api_key = os.getenv("STRIPE_KEY")

class Input(BaseModel):
    name: str
    role: str
    achievement: str

@app.get("/")
def home():
    return {"message": "LinkedIn Vending Machine Live"}

@app.post("/vend")
def vend(data: Input):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'LinkedIn Post'},
                'unit_amount': 999,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://linkedin-vend.vercel.app/success.html',
        cancel_url='https://linkedin-vend.vercel.app',
    )
    return {"checkout_url": session.url}
