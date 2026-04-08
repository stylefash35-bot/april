import os
import requests
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# Список ботов для защиты (клоакинга)
BOT_SIGNATURES = ['googlebot', 'facebookexternalhit', 'twitterbot', 'linkedinbot', 'bot', 'spider', 'crawl']

def get_geo_info(ip):
    """Определяет страну по IP через бесплатный API"""
    try:
        # Если IP локальный, сервис вернет ошибку, поэтому проверяем
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,city').json()
        if response.get('status') == 'success':
            return f"{response.get('country')}, {response.get('city')}"
    except:
        pass
    return "Unknown Country"

def log_visitor(status):
    """Записывает данные о посетителе в файл log.txt"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Получаем реальный IP (на Render он в заголовке X-Forwarded-For)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '')
    geo = get_geo_info(ip)
    
    # Определяем устройство для лога
    device = "Mobile" if any(p in ua.lower() for p in ['iphone', 'android', 'mobile']) else "PC"
    
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{geo}] [{device}] [{status}] | IP: {ip}\n")

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '').lower()
    
    # ЗАЩИТА: Если это бот — показываем «белую» страницу
    if any(sig in ua for sig in BOT_SIGNATURES):
        return render_template('white_page.html')
    
    # Логируем обычного человека
    log_visitor("Viewed Page")
    return render_template('money_page.html')

@app.route('/go')
def click_handler():
    # Логируем нажатие на кнопку
    log_visitor("CLICKED BUTTON!")
    # ЗАМЕНИ ССЫЛКУ НИЖЕ НА СВОЮ
    return redirect("https://tone.affomelody.com/click?pid=95009&offer_id=25&sub1=Liz April")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
