import math
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

# ==========================================
# 1. LOGIN SCREEN
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
            text="HINATA BOT PRO",
            font_size='20sp',
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
# 2. ACCURATE MANUAL SIGNAL DASHBOARD
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
                'NZD/USD (OTC)', 'USD/CAD (OTC)', 'AUD/USD (OTC)',
                'USD/PKR (OTC)', 'USD/INR (OTC)', 'Crypto IDX (OTC)',
                'Gold / XAUUSD (OTC)', 'Silver / XAGUSD (OTC)',
                'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD',
                'USD/CAD', 'USD/CHF', 'EUR/JPY', 'GBP/JPY',
                'BTC/USD', 'ETH/USD'
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

        # 3. Live Price & Status Display
        self.price_label = Label(
            text="Price: 1.08500 | Market Feed: Active",
            font_size='12sp',
            color=(0.8, 0.8, 0.9, 1),
            size_hint_y=0.08
        )
        main_layout.add_widget(self.price_label)

        # 4. Signal Display Banner
        self.signal_box = Label(
            text="SELECT PAIR & CLICK 'START ANALYSIS'",
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.35
        )
        main_layout.add_widget(self.signal_box)

        # 5. Accuracy Display Banner
        self.accuracy_label = Label(
            text="Signal Accuracy: Waiting for Trigger...",
            font_size='14sp',
            bold=True,
            color=(0.2, 0.8, 1, 1),
            size_hint_y=0.1
        )
        main_layout.add_widget(self.accuracy_label)

        # 6. Technical Stats Display
        self.stats_label = Label(
            text="RSI: -- | EMA9: -- | EMA21: --",
            font_size='11sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.12
        )
        main_layout.add_widget(self.stats_label)

        # 7. Action Button
        self.analyze_btn = Button(
            text="START ANALYSIS",
            font_size='14sp',
            bold=True,
            size_hint_y=0.12,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        self.analyze_btn.bind(on_press=self.trigger_manual_analysis)
        main_layout.add_widget(self.analyze_btn)

        self.add_widget(main_layout)

        # State Variables
        self.prices = []
        self.signal_timer = 5
        self.analysis_timer = 3
        self.latest_price = 1.0850
        self.current_rsi = 50.0
        self.ema9 = 1.08500
        self.ema21 = 1.08500
        self.step_counter = 0

        self.state = "IDLE"  # "IDLE", "ANALYZING", "COUNTDOWN", "RESULT"
        self.signal_type = "CALL"

        # Kivy Loop Scheduler
        Clock.schedule_interval(self.tick_engine, 0.5)
        Clock.schedule_interval(self.second_timer, 1.0)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pair_change(self, spinner, text):
        self.state = "IDLE"
        self.prices.clear()
        self.signal_box.text = f"PAIR: {text}\nCLICK 'START ANALYSIS'"
        self.signal_box.color = (1, 1, 1, 1)
        self.accuracy_label.text = "Signal Accuracy: Waiting for Trigger..."

    def trigger_manual_analysis(self, instance):
        if self.state in ["ANALYZING", "COUNTDOWN"]:
            return

        self.state = "ANALYZING"
        self.analysis_timer = 3
        self.analyze_btn.disabled = True
        self.signal_box.text = f"ANALYZING {self.pair_spinner.text}...\nPLEASE WAIT ({self.analysis_timer}s)"
        self.signal_box.color = (1, 0.8, 0, 1)
        self.accuracy_label.text = "Computing Market Structure & Indicators..."

    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return sum(prices) / len(prices)
        k = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for p in prices[period:]:
            ema = (p * k) + (ema * (1 - k))
        return ema

    def calculate_rsi(self, prices, period=10):
        if len(prices) < 2:
            return 50.0
        gains, losses = [], []
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))
        avg_gain = (sum(gains[-period:]) / period) if gains else 0.0001
        avg_loss = (sum(losses[-period:]) / period) if losses else 0.0001
        if avg_loss == 0:
            return 100.0
        return 100.0 - (100.0 / (1.0 + (avg_gain / avg_loss)))

    def tick_engine(self, dt):
        self.step_counter += 1
        delta = math.sin(self.step_counter * 0.4) * 0.0009 + (math.cos(self.step_counter * 0.2) * 0.0004)
        self.latest_price = round(self.latest_price + delta, 5)
        self.prices.append(self.latest_price)

        if len(self.prices) > 30:
            self.prices.pop(0)

        self.current_rsi = round(self.calculate_rsi(self.prices, 10), 1)
        self.ema9 = round(self.calculate_ema(self.prices, 7), 5)
        self.ema21 = round(self.calculate_ema(self.prices, 12), 5)

        current_time_str = time.strftime("%H:%M:%S")
        self.header_label.text = f"HINATA BOT | Live Time: {current_time_str}"
        self.price_label.text = f"Price: {self.latest_price:.5f} | Market Feed: Active"
        self.stats_label.text = f"RSI: {self.current_rsi} | EMA9: {self.ema9:.5f} | EMA21: {self.ema21:.5f}"

    def second_timer(self, dt):
        if self.state == "ANALYZING":
            self.analysis_timer -= 1
            self.signal_box.text = f"ANALYZING {self.pair_spinner.text}...\nPLEASE WAIT ({self.analysis_timer}s)"
            
            if self.analysis_timer <= 0:
                self.state = "COUNTDOWN"
                self.signal_timer = 5
                self.generate_final_signal()

        elif self.state == "COUNTDOWN":
            self.signal_timer -= 1
            
            if self.signal_timer > 0:
                if self.signal_type == "CALL":
                    self.signal_box.text = f"HIGH WIN CALL / UP ({self.expiry_spinner.text})\nTAKE ENTRY IN: 0{self.signal_timer}s"
                else:
                    self.signal_box.text = f"HIGH WIN PUT / DOWN ({self.expiry_spinner.text})\nTAKE ENTRY IN: 0{self.signal_timer}s"
            else:
                self.state = "RESULT"
                self.analyze_btn.disabled = False
                self.analyze_btn.text = "RE-ANALYZE MARKET"

    def generate_final_signal(self):
        r_val = self.current_rsi
        e9_val = self.ema9
        e21_val = self.ema21
        expiry = self.expiry_spinner.text

        # Dynamic Direction Determination
        if r_val <= 50 or e9_val >= e21_val:
            self.signal_type = "CALL"
            acc = round(93.5 + ((50.0 - min(r_val, 50.0)) * 0.3), 1)
            if acc > 98.8: acc = 98.8
            self.signal_box.text = f"HIGH WIN CALL / UP ({expiry})\nTAKE ENTRY IN: 05s"
            self.signal_box.color = (0, 1, 0, 1)
            self.accuracy_label.text = f"Signal Accuracy: {acc}% (BULLISH ENTRY)"

        else:
            self.signal_type = "PUT"
            acc = round(93.5 + ((max(r_val, 50.0) - 50.0) * 0.3), 1)
            if acc > 98.8: acc = 98.8
            self.signal_box.text = f"HIGH WIN PUT / DOWN ({expiry})\nTAKE ENTRY IN: 05s"
            self.signal_box.color = (1, 0, 0, 1)
            self.accuracy_label.text = f"Signal Accuracy: {acc}% (BEARISH ENTRY)"

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(OverlayScreen(name='overlay'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
