import json
import urllib.request
import threading
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class HinataBotOverlay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        
        # Background Theme
        with self.canvas.before:
            Color(0.1, 0.1, 0.15, 0.95)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Header Title
        self.title_label = Label(
            text="HINATA BOT - REAL LIVE MARKET SCANNER",
            font_size='16sp',
            bold=True,
            color=(0.8, 0.4, 1, 1),
            size_hint_y=0.15
        )
        self.add_widget(self.title_label)

        # Signal Box
        self.signal_label = Label(
            text="CONNECTING TO REAL LIVE MARKET...",
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.35
        )
        self.add_widget(self.signal_label)

        # Live Price & Metrics
        self.timer_label = Label(
            text="Live Price: -- | RSI: --",
            font_size='14sp',
            color=(0.7, 0.7, 0.9, 1),
            size_hint_y=0.15
        )
        self.add_widget(self.timer_label)

        self.stats_label = Label(
            text="EMA 9: -- | EMA 21: --",
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.15
        )
        self.add_widget(self.stats_label)

        # Controls
        self.scan_btn = Button(
            text="REFRESH DATA FEED",
            font_size='16sp',
            bold=True,
            size_hint_y=0.2,
            background_color=(0.6, 0.2, 0.9, 1)
        )
        self.scan_btn.bind(on_press=self.restart_feed)
        self.add_widget(self.scan_btn)

        # Real-time Variables
        self.prices = []
        self.latest_price = 0.0
        self.current_rsi = "--"
        self.ema_fast_val = "--"
        self.ema_slow_val = "--"
        self.running = True

        # Live Data Thread
        self.start_feed_thread()

        # UI Loop
        Clock.schedule_interval(self.update_ui, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # Technical Indicators (Pure Python)
    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return None
        k = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for price in prices[period:]:
            ema = (price * k) + (ema * (1 - k))
        return ema

    def calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return None
        gains, losses = [], []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            if change >= 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(abs(change))
                losses.append(change)

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum([abs(x) for x in losses[-period:]]) / period

        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # Live Feed Fetcher (Standard Library - No Extra Packages Needed)
    def start_feed_thread(self):
        feed_thread = threading.Thread(target=self.fetch_real_prices, daemon=True)
        feed_thread.start()

    def fetch_real_prices(self):
        url = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
        while self.running:
            try:
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response = urllib.request.urlopen(req, timeout=5)
                data = json.loads(response.read().decode())
                
                if 'price' in data:
                    price = float(data['price'])
                    self.latest_price = price
                    self.prices.append(price)

                    if len(self.prices) > 60:
                        self.prices.pop(0)

                    if len(self.prices) >= 25:
                        rsi = self.calculate_rsi(self.prices, 14)
                        ema9 = self.calculate_ema(self.prices, 9)
                        ema21 = self.calculate_ema(self.prices, 21)

                        if rsi and ema9 and ema21:
                            self.current_rsi = f"{rsi:.1f}"
                            self.ema_fast_val = f"{ema9:.5f}"
                            self.ema_slow_val = f"{ema21:.5f}"
            except Exception:
                pass
            time.sleep(2) # Fetch live price tick every 2 seconds

    def update_ui(self, dt):
        if len(self.prices) < 25:
            self.signal_label.text = f"FETCHING REAL TICKS... ({len(self.prices)}/25)"
            return

        self.timer_label.text = f"Price: {self.latest_price:.5f} | RSI: {self.current_rsi}"
        self.stats_label.text = f"EMA9: {self.ema_fast_val} | EMA21: {self.ema_slow_val}"

        # Real Confluence Strategy
        try:
            rsi_val = float(self.current_rsi)
            ema9_val = float(self.ema_fast_val)
            ema21_val = float(self.ema_slow_val)

            if rsi_val < 35 and ema9_val > ema21_val:
                self.signal_label.text = "🔥 REAL CALL (BUY) SIGNAL!"
                self.signal_label.color = (0, 1, 0, 1)
            elif rsi_val > 65 and ema9_val < ema21_val:
                self.signal_label.text = "🔻 REAL PUT (SELL) SIGNAL!"
                self.signal_label.color = (1, 0, 0, 1)
            else:
                self.signal_label.text = "WAITING FOR REAL MARKET SETUP..."
                self.signal_label.color = (0.8, 0.8, 0.8, 1)
        except ValueError:
            pass

    def restart_feed(self, instance):
        self.prices.clear()
        self.signal_label.text = "RECONNECTING LIVE FEED..."

class HinataBotApp(App):
    def build(self):
        return HinataBotOverlay()

if __name__ == '__main__':
    HinataBotApp().run()
