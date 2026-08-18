import json
import threading
import time
import math
from urllib.request import Request, urlopen

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

# ==========================================
# 1. LOGIN SCREEN
# ==========================================
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        with layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        layout.add_widget(Label(
            text="HINATA BOT LOGIN",
            font_size='22sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.2
        ))

        self.user_input = TextInput(
            hint_text="Enter License Key",
            multiline=False,
            size_hint_y=0.15,
            padding=[10, 10]
        )
        layout.add_widget(self.user_input)

        login_btn = Button(
            text="START OTC BOT",
            font_size='18sp',
            bold=True,
            size_hint_y=0.15,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        login_btn.bind(on_press=self.validate_login)
        layout.add_widget(login_btn)

        self.status_lbl = Label(
            text="Status: Ready",
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.1
        )
        layout.add_widget(self.status_lbl)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def validate_login(self, instance):
        if self.user_input.text.strip() != "":
            self.manager.current = 'overlay'
        else:
            self.status_lbl.text = "Please enter a key!"
            self.status_lbl.color = (1, 0, 0, 1)

# ==========================================
# 2. OVERLAY DASHBOARD (OTC ANALYZER)
# ==========================================
class OverlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        with layout.canvas.before:
            Color(0.1, 0.1, 0.16, 0.95)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        layout.add_widget(Label(
            text="HINATA BOT - REAL & OTC ANALYZER",
            font_size='18sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.12
        ))

        # Main Signal Output
        self.signal_label = Label(
            text="ANALYZING OTC MARKET STRUCTURE...",
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.35
        )
        layout.add_widget(self.signal_label)

        # Timer & Price Display
        self.timer_label = Label(
            text="Candle Timer: 00:60 | Price: --",
            font_size='14sp',
            color=(0.7, 0.7, 0.9, 1),
            size_hint_y=0.13
        )
        layout.add_widget(self.timer_label)

        # Technical Metrics
        self.stats_label = Label(
            text="RSI: -- | EMA 9: -- | EMA 21: --",
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.12
        )
        layout.add_widget(self.stats_label)

        # Mode Selection & Controls
        btn_box = BoxLayout(spacing=10, size_hint_y=0.18)
        
        self.mode_btn = Button(
            text="MODE: OTC MARKET",
            font_size='12sp',
            bold=True,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.mode_btn.bind(on_press=self.toggle_mode)
        btn_box.add_widget(self.mode_btn)

        scan_btn = Button(
            text="REFRESH DATA",
            font_size='12sp',
            bold=True,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        scan_btn.bind(on_press=self.reset_data)
        btn_box.add_widget(scan_btn)

        layout.add_widget(btn_box)
        self.add_widget(layout)

        # Logic Variables
        self.prices = []
        self.countdown = 60
        self.latest_price = 1.0850
        self.current_rsi = "--"
        self.ema9 = "--"
        self.ema21 = "--"
        self.is_otc = True
        self.step_counter = 0

        # Threads and Clocks
        threading.Thread(target=self.market_data_engine, daemon=True).start()
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.update_ui, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_mode(self, instance):
        self.is_otc = not self.is_otc
        self.prices.clear()
        if self.is_otc:
            self.mode_btn.text = "MODE: OTC MARKET"
            self.mode_btn.background_color = (0.2, 0.6, 0.8, 1)
        else:
            self.mode_btn.text = "MODE: REAL MARKET"
            self.mode_btn.background_color = (0.2, 0.8, 0.4, 1)

    def update_timer(self, dt):
        self.countdown -= 1
        if self.countdown <= 0:
            self.countdown = 60

    # Indicator Formulas
    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return None
        k = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for p in prices[period:]:
            ema = (p * k) + (ema * (1 - k))
        return ema

    def calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return None
        gains, losses = [], []
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100
        return 100 - (100 / (1 + (avg_gain / avg_loss)))

    def market_data_engine(self):
        while True:
            try:
                if not self.is_otc:
                    # Real Market Public Stream
                    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=eur"
                    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    res = urlopen(req, timeout=5)
                    data = json.loads(res.read().decode())
                    price = float(data['tether']['eur'])
                else:
                    # OTC Market Price Stream Simulation Engine
                    self.step_counter += 1
                    delta = math.sin(self.step_counter * 0.3) * 0.0008 + (math.cos(self.step_counter * 0.1) * 0.0003)
                    price = round(self.latest_price + delta, 5)

                self.latest_price = price
                self.prices.append(price)
                if len(self.prices) > 50:
                    self.prices.pop(0)

                if len(self.prices) >= 15:
                    r = self.calculate_rsi(self.prices, 14)
                    e9 = self.calculate_ema(self.prices, 9)
                    e21 = self.calculate_ema(self.prices, 21)

                    if r and e9 and e21:
                        self.current_rsi = f"{r:.1f}"
                        self.ema9 = f"{e9:.5f}"
                        self.ema21 = f"{e21:.5f}"
            except Exception:
                pass
            time.sleep(2)

    def update_ui(self, dt):
        mode_text = "OTC" if self.is_otc else "REAL"
        self.timer_label.text = f"[{mode_text}] Timer: 00:{self.countdown:02d} | Price: {self.latest_price:.4f}"
        self.stats_label.text = f"RSI: {self.current_rsi} | EMA9: {self.ema9} | EMA21: {self.ema21}"

        if len(self.prices) < 15:
            self.signal_label.text = f"BUILDING {mode_text} TICKS... ({len(self.prices)}/15)"
            return

        try:
            r_val = float(self.current_rsi)
            e9_val = float(self.ema9)
            e21_val = float(self.ema21)

            # Strict Technical Confluence Execution
            if r_val < 35 and e9_val > e21_val:
                self.signal_label.text = f"🔥 {mode_text} CALL (BUY) CONFIRMED!"
                self.signal_label.color = (0, 1, 0, 1)
            elif r_val > 65 and e9_val < e21_val:
                self.signal_label.text = f"🔻 {mode_text} PUT (SELL) CONFIRMED!"
                self.signal_label.color = (1, 0, 0, 1)
            else:
                self.signal_label.text = "WAITING FOR MARKET SETUP..."
                self.signal_label.color = (0.8, 0.8, 0.8, 1)
        except ValueError:
            pass

    def reset_data(self, instance):
        self.prices.clear()
        self.signal_label.text = "RECONNECTING..."

# ==========================================
# 3. APP MANAGER
# ==========================================
class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(OverlayScreen(name='overlay'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
