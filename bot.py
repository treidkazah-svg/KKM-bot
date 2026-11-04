import os, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BALANCE = 100.0
BOT_ON = True

class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200); self.end_headers(); self.wfile.write(b"KKM OK")
 def do_HEAD(self):
  self.send_response(200); self.end_headers()
 def log_message(self,*a): return
def run_web():
 HTTPServer(("0.0.0.0", int(os.environ.get("PORT",10000))), H).serve_forever()

def get_price():
 try:
  r=requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=10).json()
  return float(r['items'][0]['curr'])/31.1035
 except: return 2650.0

def send_tg(msg):
 try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT_ID, "text":msg})
 except: pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
 global BOT_ON; BOT_ON=True
 send_tg("#START_EA")
 await update.message.reply_text("🟢 БОТ ҚОСЫЛДЫ!\n\nЛогика: 7 стратегия -> 4 дурыс болса да киреди!\n90% -> 0.05 лот, ТП 500-700\n70% -> 0.03 лот, ТП 300-500\n50% -> 0.01 лот, ТП 200-300\n\n/status - Плюс/Минус\n/stop - Токтату\n/close - Жабу\n/balance - Баланс")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 global BOT_ON; BOT_ON=False
 send_tg("#STOP_EA")
 await update.message.reply_text("🛑 БОТ ТОКТАТЫЛДЫ!")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 p=get_price()
 await update.message.reply_text(f"📊 XAUUSD: {p:.1f}\n💰 Баланс: {BALANCE}$\n🤖 Бот: {'КОСУЛЫ' if BOT_ON else 'ОШИРУЛИ'}")

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text(f"💰 БАЛАНС: {BALANCE}$")

async def close_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 send_tg("#C
