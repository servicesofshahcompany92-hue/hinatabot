import math
import threading
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

# ==========================================
# 1. COMPACT LOGIN SCREEN
# ==========================================
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        with layout.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        layout.add_widget(Label(
            text="HINATA BOT",
            font_size='18sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.25
        ))

        self.user_input = TextInput(
            hint_text="Enter License Key",
            multiline=False,
            size_hint_y=0.2,
            padding=[10, 8]
        )
        layout.add_widget(self.user_input)

        login_btn = Button(
            text="LOGIN",
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
            self.status_lbl.text = "Please enter key!"

# ==========================================
# 2. COMPLETE MAIN DASHBOARD INTERFACE
# ==========================================
class OverlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)

        with main_layout.canvas.before:
            Color(0.1, 0.1, 0.15, 0.95)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # 1. Header
        main_layout.add_widget(Label(
            text="HINATA BOT v2.0",
            font_size='16sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.08
        ))

        # 2. Control Row: Pair Selection & Timeframe Selection
        control_row = BoxLayout(spacing=8, size_hint_y=0.12)
        
        # Quotex Pair Dropdown
        self.pair_spinner = Spinner(
            text='EUR/USD (OTC)',
            values=(
                'EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 
                'AUD/CAD (OTC)', 'USD/BRL (OTC)', 'EUR/GBP (OTC)',
                'EUR/USD', 'GBP/USD', 'USD/JPY'
            ),
            size_hint_x=0.6,
            font_size='11sp'
        )
        self.pair_spinner.bind(text=self.on_pair_change)
        control_row.add_widget(self.pair_spinner)

        # Expiry Time Selection Dropdown
        self.time_spinner = Spinner(
            text='1 MIN',
            values=('1 MIN', '2 MIN', '5 MIN'),
            size_hint_x=0.4,
            font_size='11sp'
        )
        self.time_spinner.bind(text=self.on_time_change)
        control_row.add_widget(self.time_spinner)

        main_layout.add_widget(control_row)

        # 3. Live Price & Candle Timer Row
        self.timer_label = Label(
            text="Price: 1.08500 | Candle: 00:60",
            font_size='12sp',
            color=(0.8, 0.8, 0.9, 1),
            size_hint_y=0.08
        )
        main_layout.add_widget(self.timer_label)

        # 4. Live Signal Screen Box
        self.signal_label = Label(
            text="ANALYZING MARKET...",
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.4
        )
        main_layout.add_widget(self.signal_label)

        # 5. Technical Indicators Info Box
        self.stats_label = Label(
            text="RSI: -- | EMA9: -- | EMA21: --",
            font_size='11sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.12
        )
        main_layout.add_widget(self.stats_label)

        # 6. Action Button
        scan_btn = Button(
            text="FORCE SCAN NOW",
            font_size='12sp',
            bold=True,
            size_hint_y=0.12,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        scan_btn.bind(on_press=self.reset_data)
        main_layout.add_widget(scan_btn)

        self.add_widget(main_layout)

        # State Variables
        self.prices = []
        self.countdown = 60
        self.latest_price = 1.0850
        self.current_rsi = "--"
        self.ema9 = "--"
        self.ema21 = "--"
        self.step_counter = 0

        # Background Thread & Timers
        threading.Thread(target=self.market_engine, daemon=True).start()
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.update_ui, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pair_change(self, spinner, text):
        self.prices.clear()
        self.signal_label.text = f"SWITCHED TO {text}"

    def on_time_change(self, spinner, text):
        if '1' in text:
            self.countdown = 60
        elif '2' in text:
            self.countdown = 120
        elif '5' in text:
            self.countdown = 300

    def update_timer(self, dt):
        self.countdown -= 1
        if self.countdown <= 0:
            time_text = self.time_spinner.text
            self.countdown = 60 if '1' in time_text else (120 if '2' in time_text else 300)

    # Fast Math Indicators
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

    def market_engine(self):
        while True:
            self.step_counter += 1
            delta = math.sin(self.step_counter * 0.2) * 0.0006 + (math.cos(self.step_counter * 0.1) * 0.0002)
            self.latest_price = round(self.latest_price + delta, 5)
            self.prices.append(self.latest_price)

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
            time.sleep(2)

    def update_ui(self, dt):
        mins = self.countdown // 60
        secs = self.countdown % 60
        self.timer_label.text = f"Price: {self.latest_price:.5f} | Candle: {mins:02d}:{secs:02d}"
        self.stats_label.text = f"RSI: {self.current_rsi} | EMA9: {self.ema9} | EMA21: {self.ema21}"

        if len(self.prices) < 15:
            self.signal_label.text = f"LOADING TICKS... ({len(self.prices)}/15)"
            return

        try:
            r_val = float(self.current_rsi)
            e9_val = float(self.ema9)
            e21_val = float(self.ema21)

            if r_val < 35 and e9_val > e21_val:
                self.signal_label.text = "🔥 CALL (BUY) SIGNAL!"
                self.signal_label.color = (0, 1, 0, 1)
            elif r_val > 65 and e9_val < e21_val:
                self.signal_label.text = "🔻 PUT (SELL) SIGNAL!"
                self.signal_label.color = (1, 0, 0, 1)
            else:
                self.signal_label.text = "WAITING FOR SIGNAL..."
                self.signal_label.color = (0.7, 0.7, 0.7, 1)
        except ValueError:
            pass

    def reset_data(self, instance):
        self.prices.clear()
        self.signal_label.text = "RE-ANALYZING..."

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(OverlayScreen(name='overlay'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
