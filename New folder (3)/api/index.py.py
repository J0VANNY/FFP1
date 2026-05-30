from flask import Flask, render_template, request, redirect, url_for, make_response
import secrets
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

TOKENS_FILE = 'tokens.json'

def load_tokens():
    try:
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_tokens(tokens):
    try:
        with open(TOKENS_FILE, 'w') as f:
            json.dump(tokens, f)
    except:
        pass

def generate_token():
    return secrets.token_urlsafe(32)

@app.route('/')
def index():
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    token = request.cookies.get('access_token')
    device_id = request.cookies.get('device_id')
    
    if not device_id:
        device_id = secrets.token_urlsafe(16)
    
    tokens = load_tokens()
    
    if token and token in tokens:
        stored_device = tokens[token]
        if stored_device == device_id:
            resp = make_response(render_template('gemini-code-1780070106376.html'))
            resp.set_cookie('device_id', device_id, max_age=60*60*24*365, httponly=True, samesite='Lax')
            return resp
        else:
            return "هذا الرابط محجوز على جهاز آخر", 403
    
    new_token = generate_token()
    tokens[new_token] = device_id
    save_tokens(tokens)
    
    resp = make_response(render_template('gemini-code-1780070106376.html'))
    resp.set_cookie('access_token', new_token, max_age=60*60*24*365, httponly=True, samesite='Lax')
    resp.set_cookie('device_id', device_id, max_age=60*60*24*365, httponly=True, samesite='Lax')
    return resp

@app.route('/reset')
def reset():
    resp = make_response(redirect(url_for('quiz')))
    resp.delete_cookie('access_token')
    resp.delete_cookie('device_id')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
