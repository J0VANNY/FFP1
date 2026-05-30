import os
import secrets
from flask import Flask, render_template, request, make_response

# تحديد مسار فولدر القوالب بدقة لبيئة Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, '..', 'templates')
app = Flask(__name__, template_folder=template_dir)

# كود الماستر بتاعك (بيفتح من أي جهاز وفي أي وقت)
MASTER_TOKEN = "jovany_master_2026"

# الـ 20 كود العشوائيين لأصحابك
AUTHORIZED_TOKENS = {
    "xR7vQ2": None, "bN9mK1": None, "pL5tW8": None, "jH3gB6": None, "fD2sS4": None,
    "zA1xX9": None, "cC8vV7": None, "bB6nN5": None, "mM4kK3": None, "lL2pP1": None,
    "oO9iI8": None, "uU7yY6": None, "tT5rR4": None, "eE3wW2": None, "qQ1aA9": None,
    "sS8dD7": None, "fF6gG5": None, "hH4jJ3": None, "kK2lL1": None, "zZ9xX8": None
}

@app.route('/')
def index():
    token = request.args.get('token')
    
    if not token or (token != MASTER_TOKEN and token not in AUTHORIZED_TOKENS):
        return "عذراً، هذا الرابط غير صحيح أو انتهت صلاحيته.", 403

    if token == MASTER_TOKEN:
        return render_template('gemini-code-1780070106376.html')

    device_cookie = request.cookies.get('device_signature')

    if AUTHORIZED_TOKENS[token] is None:
        new_device_id = secrets.token_hex(16)
        AUTHORIZED_TOKENS[token] = new_device_id
        
        response = make_response(render_template('gemini-code-1780070106376.html'))
        response.set_cookie('device_signature', new_device_id, max_age=31536000, httponly=True)
        return response

    if AUTHORIZED_TOKENS[token] == device_cookie:
        return render_template('gemini-code-1780070106376.html')
    else:
        return "⚠️ عذراً، حدث خطأ غير متوقع في الاتصال بالسيرفر (تنفيذ الكود 502). يرجى مراجعة مسؤول المنصة.", 403
