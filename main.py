from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timedelta
import telepot
import os

# Telegram bot tokeni va chat ID
TELEGRAM_BOT_TOKEN = '7079226259:AAGtOPmSanMnC9VJqpUxZFcg1NXEM6_RKc0'
CHAT_ID = '6110556252'

# JSON fayl yo'li
DATA_FILE = 'products.json'

# Telegram botni sozlash
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

class RequestHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == '/save_product':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            name = data.get('name')
            expiry_date = data.get('expiry_date')

            # Yaroqlilik muddati formatini tekshirish
            try:
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except ValueError:
                self.send_response(400)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b'Invalid date format')
                return

            # Ma'lumotlarni JSON fayliga yozish
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as file:
                    products = json.load(file)
            else:
                products = []

            products.append({
                'name': name,
                'expiry_date': expiry_date.strftime('%Y-%m-%d')
            })

            with open(DATA_FILE, 'w') as file:
                json.dump(products, file, indent=4)

            # Telegram bot orqali ma'lumotlarni yuborish
            bot.sendMessage(CHAT_ID, f"Mahsulot: {name}\nYaroqlilik muddati: {expiry_date.strftime('%Y-%m-%d')}")

            # Yaroqlilik muddati 1 kunga qolganda xabar yuborish
            for product in products:
                product_date = datetime.strptime(product['expiry_date'], '%Y-%m-%d').date()
                if product_date == (datetime.now().date() + timedelta(days=1)):
                    bot.sendMessage(CHAT_ID, f"Eslatma: {product['name']} mahsulotining yaroqlilik muddati 1 kun qolgan.")

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
