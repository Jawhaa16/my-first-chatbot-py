from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Facebook API endpoints
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your_verify_token")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "your_page_access_token")

@app.route("/webhook", methods=["GET"])
def verify():
    """Webhook verification for Facebook"""
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"]
    return "Hello world", 200

@app.route("/webhook", methods=["POST"])
def handle_messages():
    """Handle incoming messages from Facebook"""
    data = request.get_json()
    
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                
                if messaging_event.get("message"):
                    recipient_id = messaging_event["recipient"]["id"]
                    user_message = messaging_event["message"].get("text")
                    
                    if user_message:
                        send_message(sender_id, "Сайн байна! 👋")
                        send_store_info(sender_id)
                
                if messaging_event.get("postback"):
                    handle_postback(sender_id, messaging_event["postback"])
    
    return "ok", 200

def send_message(recipient_id, message_text):
    """Send a simple text message"""
    message_data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    send_facebook_message(message_data)

def send_store_info(recipient_id):
    """Send store info with buttons"""
    message_data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Манай дэлгүүрийн мэдээлэл:",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Дэлгүүрийн байршил",
                            "payload": "LOCATION"
                        },
                        {
                            "type": "postback",
                            "title": "Хүргэлт",
                            "payload": "DELIVERY"
                        },
                        {
                            "type": "postback",
                            "title": "Урамшуулал",
                            "payload": "PROMO"
                        }
                    ]
                }
            }
        }
    }
    send_facebook_message(message_data)

def handle_postback(sender_id, postback):
    """Handle button clicks"""
    payload = postback.get("payload")
    
    responses = {
        "LOCATION": "📍 Манай дэлгүүр: Улаанбаатар хот, Сүхбаатар дүүрэг, 1-р хороо",
        "DELIVERY": "🚚 Хүргэлт: Улаанбаатарт 2-3 цагийн дотор үнэ төлбөргүй",
        "PROMO": "🎉 Одоо 20% хямдрал бүх бүтээгдэхүүнд!"
    }
    
    if payload in responses:
        send_message(sender_id, responses[payload])

def send_facebook_message(message_data):
    """Send message to Facebook API"""
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(
        "https://graph.facebook.com/v12.0/me/messages",
        json=message_data,
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
