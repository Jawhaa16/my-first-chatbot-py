# Facebook Messenger Chatbot Setup

## Шаардлагатай:
1. Facebook Developer Account
2. Facebook Page
3. Python 3.7+

## Суулгах:

```bash
# Python сангуудыг суулгах
pip install -r requirements.txt
```

## Facebook токен авах:

1. Facebook Developer (https://developers.facebook.com/) руу орох
2. New App үүсгэх
3. Messenger Product нэмэх
4. Page Access Token авах
5. Webhook Verify Token үүсгэх (өөрөө)

## Тохируулах:

`.env` файлд токенийг нэмэх:
```
VERIFY_TOKEN=your_verify_token
PAGE_ACCESS_TOKEN=your_page_access_token
```

## Явуулах:

```bash
python app.py
```

App `http://localhost:5000/webhook` дээр ажиллана.

## Webhook холбох:

Facebook Developer portal-д:
1. Webhook URL: `https://your-domain.com/webhook`
2. Verify Token: `.env` дээрх token
3. Subscribe to: `messages`, `messaging_postbacks`

## Features:

✅ Үйлчүүлэгчээс мессеж хүлээх
✅ "Сайн байна!" гэж хариулах
✅ Дэлгүүрийн мэдээлэл харуулах
✅ 3 товчлуур: Байршил, Хүргэлт, Урамшуулал
