import os, threading, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
 def do_HEAD(self):
  self.send_response(200); self.end_headers()
 def log_message(self,*a): return

def run_web():
 HTTPServer(("0.0.0.0", int(os.environ.get("PORT",10000))), H).serve_forever()

def send_tg(msg):
 try:
  requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", data={"chat_id":CHAT_ID, "text":msg})
 except: pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
 send_tg("START_EA")
 await update.message.reply_text("BOT KOSYLDI! 7 strategiya zhymys istep zhatyr")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 send_tg("STOP_EA")
 await update.message.reply_text("BOT TOKTATYLDY!")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text("BOT ZHUMYS ISTEP Zhatyr. XAUUSD izdep zhatyr...")

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text("BALANS: 100$")

async def close_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
 send_tg("CLOSE_ALL")
 await update.message.reply_text("JABUGA BUYRYK KETTI!")

def main():
 threading.Thread(target=run_web,daemon=True).start()
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(CommandHandler("stop",stop_cmd))
 app.add_handler(CommandHandler("status",status_cmd))
 app.add_handler(CommandHandler("balance",balance_cmd))
 app.add_handler(CommandHandler("close",close_cmd))
 print("BOT RUNNING")
 app.run_polling()

if __name__=="__main__":
 main()
