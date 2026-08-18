from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

# Global variable to store live TradingView signal data
tv_signal_data = {
    "action": "WAITING",  # "UP", "DOWN", "NO_TRADE"
    "pair": "EUR/USD",
    "accuracy": 0.0,
    "received_time": 0
}

# ==========================================
# 1. TRADINGVIEW WEBHOOK SERVER ENGINE
# ==========================================
class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global tv_signal_data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
            action = str(payload.get("action", "")).upper()
            pair = payload.get("pair", "EUR/USD")
            accuracy = float(payload.get("accuracy", 95.0))

            if action in ["BUY", "CALL", "UP"]:
                tv_signal_data["action"] = "UP"
            elif action in ["SELL", "PUT", "DOWN"]:
                tv_signal_data["action"] = "DOWN"
            elif action in ["NO_TRADE", "WAIT", "SIDEWAYS"]:
                tv_signal_data["action"] = "NO_TRADE"
            
            tv_signal_data["pair"] = pair
            tv_signal_data["accuracy"] = accuracy
            tv_signal_data["received_time"] = time.time()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        except Exception:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def start_webhook_server():
    try:
        server = HTTPServer(('0.0.0.0', 8080), WebhookHandler)
        server.serve_forever()
    except Exception:
        pass

# Start Background Webhook Listener Thread
threading.Thread(target=start_webhook_server, daemon=True).start()

# ==========================================
# 2. LOGIN SCREEN
# ==========================================
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=12)

        with layout.canvas.before:
            Color(0.06, 0.06, 0.1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        layout.add_widget(Label(
            text="HINATA BOT PRO | TRADINGVIEW",
            font_size='18sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.25
        ))

        self.user_input = TextInput(
            hint_text="Enter VIP License Key",
            multiline=False,
            size_hint_y=0.2,
            padding=[10, 10]
        )
        layout.add_widget(self.user_input)

        login_btn = Button(
            text="ACCESS DASHBOARD",
            font_size='14sp',
            bold=True,
            size_hint_y=0.2,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        login_btn.bind(on_press=self.validate_login)
        layout.add_widget(login_btn)

        self.status_lbl = Label(text="", font_size='11sp', color=(1, 0, 0, 1), size_hint_y=0.15)
        layout.add_widget(self.status_lbl)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def validate_login(self, instance):
        if self.user_input.text.strip():
            self.manager.current = 'overlay'
        else:
            self.status_lbl.text = "Enter valid key!"

# ==========================================
# 3. TRADINGVIEW LIVE DASHBOARD SCREEN
# ==========================================
class OverlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        with main_layout.canvas.before:
            Color(0.08, 0.08, 0.12, 0.95)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # 1. Header & Live Time
        self.header_label = Label(
            text="HINATA BOT | Live Time: --:--:--",
            font_size='14sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.08
        )
        main_layout.add_widget(self.header_label)

        # 2. Controls Row
        control_row = BoxLayout(spacing=6, size_hint_y=0.12)
        
        self.pair_spinner = Spinner(
            text='EUR/USD (OTC)',
            values=(
                'EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 
                'AUD/CAD (OTC)', 'USD/BRL (OTC)', 'EUR/GBP (OTC)',
                'NZD/USD (OTC)', 'USD/CAD (OTC)', 'Crypto IDX (OTC)',
                'Gold / XAUUSD (OTC)', 'EUR/USD', 'GBP/USD', 'USD/JPY', 'BTC/USD'
            ),
            size_hint_x=0.6,
            font_size='11sp'
        )
        self.pair_spinner.bind(text=self.on_pair_change)
        control_row.add_widget(self.pair_spinner)

        self.expiry_spinner = Spinner(
            text='5 SEC',
            values=('5 SEC', '10 SEC', '15 SEC', '30 SEC', '1 MIN', '2 MIN', '5 MIN'),
            size_hint_x=0.4,
            font_size='11sp'
        )
        control_row.add_widget(self.expiry_spinner)
        main_layout.add_widget(control_row)

        # 3. Server Status Feed
        self.price_label = Label(
            text="Engine: Active | Listener Port: 8080",
            font_size='12sp',
            color=(0.8, 0.8, 0.9, 1),
            size_hint_y=0.08
        )
        main_layout.add_widget(self.price_label)

        # 4. Signal Banner
        self.signal_box = Label(
            text="LISTENING FOR TRADINGVIEW ALERTS...",
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.35
        )
        main_layout.add_widget(self.signal_box)

        # 5. Accuracy Rate Display
        self.accuracy_label = Label(
            text="Signal Accuracy: Waiting for TV Data...",
            font_size='14sp',
            bold=True,
            color=(0.2, 0.8, 1, 1),
            size_hint_y=0.1
        )
        main_layout.add_widget(self.accuracy_label)

        # 6. Technical Stats
        self.stats_label = Label(
            text="Source: TradingView Live Webhook Stream",
            font_size='11sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.12
        )
        main_layout.add_widget(self.stats_label)

        # 7. Force Reset Control
        scan_btn = Button(
            text="FORCE RE-CONNECT FEED",
            font_size='12sp',
            bold=True,
            size_hint_y=0.12,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        scan_btn.bind(on_press=self.reset_data)
        main_layout.add_widget(scan_btn)

        self.add_widget(main_layout)

        # Kivy Main Loop Scheduler
        Clock.schedule_interval(self.update_ui, 0.5)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pair_change(self, spinner, text):
        self.signal_box.text = f"LISTENING FOR {text} ALERTS..."
        self.signal_box.color = (1, 1, 1, 1)

    def update_ui(self, dt):
        global tv_signal_data
        current_time_str = time.strftime("%H:%M:%S")
        self.header_label.text = f"HINATA BOT | Live Time: {current_time_str}"

        now = time.time()
        expiry = self.expiry_spinner.text

        # Show Signal if received in the last 15 seconds
        if tv_signal_data["received_time"] > 0 and (now - tv_signal_data["received_time"]) <= 15:
            action = tv_signal_data["action"]
            accuracy = tv_signal_data["accuracy"]

            if action == "UP":
                self.signal_box.text = f"🔥 TRADINGVIEW CALL / UP ({expiry})\nCONFIRMED ENTRY SIGNAL"
                self.signal_box.color = (0, 1, 0, 1)
                self.accuracy_label.text = f"TradingView Signal Accuracy: {accuracy}%"

            elif action == "DOWN":
                self.signal_box.text = f"🔻 TRADINGVIEW PUT / DOWN ({expiry})\nCONFIRMED ENTRY SIGNAL"
                self.signal_box.color = (1, 0, 0, 1)
                self.accuracy_label.text = f"TradingView Signal Accuracy: {accuracy}%"

            elif action == "NO_TRADE":
                self.signal_box.text = "⚠️ NO TRADE ZONE!\nTRADINGVIEW: SIDEWAYS MARKET"
                self.signal_box.color = (1, 0.8, 0, 1)
                self.accuracy_label.text = "Signal Accuracy: RISKY (SKIP ENTRY)"
        else:
            self.signal_box.text = "LISTENING FOR TRADINGVIEW ALERTS..."
            self.signal_box.color = (0.7, 0.7, 0.7, 1)
            self.accuracy_label.text = "Signal Accuracy: Waiting for TV Data..."

    def reset_data(self, instance):
        global tv_signal_data
        tv_signal_data["received_time"] = 0
        self.signal_box.text = "RE-LISTENING TO TRADINGVIEW FEED..."

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(OverlayScreen(name='overlay'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
