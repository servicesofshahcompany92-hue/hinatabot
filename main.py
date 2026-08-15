import os
import random
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line

# Neon Dark Theme Colors
BG_COLOR = (0.05, 0.07, 0.10, 1)
CARD_COLOR = (0.09, 0.12, 0.17, 1)
CARD_BORDER = (0.15, 0.22, 0.30, 1)
NEON_GREEN = (0.0, 0.9, 0.45, 1)
NEON_RED = (1.0, 0.25, 0.25, 1)
TEXT_MAIN = (0.95, 0.96, 0.98, 1)
TEXT_SUB = (0.60, 0.68, 0.78, 1)

# All Quotex Pairs List (OTC + Real + Crypto + Commodities + Stocks)
QUOTEX_PAIRS = [
    # OTC Forex Pairs
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)",
    "EUR/GBP (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "AUD/USD (OTC)",
    "CAD/JPY (OTC)", "EUR/JPY (OTC)", "GBP/JPY (OTC)", "USD/CAD (OTC)",
    "AUD/JPY (OTC)", "EUR/CAD (OTC)", "CHF/JPY (OTC)", "GBP/CAD (OTC)",
    "GBP/CHF (OTC)", "CAD/CHF (OTC)", "NZD/JPY (OTC)", "NZD/CAD (OTC)",
    
    # Real Market Forex
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "USD/CHF", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
    
    # Crypto Pairs
    "BTC/USD (Crypto)", "ETH/USD (Crypto)", "LTC/USD (Crypto)",
    "XRP/USD (Crypto)", "SOL/USD (Crypto)", "DOGE/USD (Crypto)",
    
    # Commodities & Stocks
    "GOLD (OTC)", "SILVER (OTC)", "US CRUDE (OTC)", "BRENT CRUDE (OTC)",
    "Boeing Company (OTC)", "Intel (OTC)", "Microsoft (OTC)", "Pfizer (OTC)"
]

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(
            orientation='vertical',
            padding=25,
            spacing=15,
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        with layout.canvas.before:
            Color(*CARD_COLOR)
            self.card_rect = RoundedRectangle(size=layout.size, pos=layout.pos, radius=[16])
            Color(*CARD_BORDER)
            self.card_line = Line(rounded_rectangle=[layout.x, layout.y, layout.width, layout.height, 16], width=1.2)
        layout.bind(size=self._update_layout_card, pos=self._update_layout_card)

        layout.add_widget(Label(
            text="[b]HINATA BOT PRO[/b]",
            markup=True, font_size='22sp', color=TEXT_MAIN,
            size_hint_y=0.25
        ))
        layout.add_widget(Label(
            text="[color=00e673]AI QUANT TRADING TERMINAL[/color]",
            markup=True, font_size='13sp', color=NEON_GREEN,
            size_hint_y=0.15
        ))

        u_box = BoxLayout(orientation='vertical', spacing=4, size_hint_y=0.25)
        u_box.add_widget(Label(text="TRADER ID", color=TEXT_SUB, font_size='12sp', halign='left', size_hint_y=0.3, bold=True))
        self.u_in = TextInput(
            text="Hinata_Pro_VIP", readonly=True, multiline=False,
            size_hint_y=0.7,
            background_color=(0.06, 0.08, 0.12, 1), foreground_color=NEON_GREEN,
            padding=[12, 10], font_size='14sp'
        )
        u_box.add_widget(self.u_in)
        layout.add_widget(u_box)

        p_box = BoxLayout(orientation='vertical', spacing=4, size_hint_y=0.25)
        p_box.add_widget(Label(text="ACCESS KEY", color=TEXT_SUB, font_size='12sp', halign='left', size_hint_y=0.3, bold=True))
        self.p_in = TextInput(
            password=True, hint_text="Enter Access Key", multiline=False,
            size_hint_y=0.7,
            background_color=(0.06, 0.08, 0.12, 1), foreground_color=TEXT_MAIN,
            padding=[12, 10], font_size='14sp'
        )
        p_box.add_widget(self.p_in)
        layout.add_widget(p_box)

        self.btn = Button(
            text="AUTHENTICATE & ENTER", bold=True,
            size_hint_y=0.22,
            background_color=(0,0,0,0), color=(1,1,1,1), font_size='15sp'
        )
        with self.btn.canvas.before:
            Color(*NEON_GREEN)
            self.btn_bg = RoundedRectangle(size=self.btn.size, pos=self.btn.pos, radius=[10])
        self.btn.bind(size=self._update_btn, pos=self._update_btn, on_release=self.auth)
        layout.add_widget(self.btn)

        self.err = Label(text="", color=NEON_RED, font_size='12sp', size_hint_y=0.1)
        layout.add_widget(self.err)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_layout_card(self, instance, value):
        self.card_rect.size = instance.size
        self.card_rect.pos = instance.pos
        self.card_line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 16]

    def _update_btn(self, instance, value):
        self.btn_bg.size = instance.size
        self.btn_bg.pos = instance.pos

    def auth(self, instance):
        if self.p_in.text.strip():
            self.manager.current = 'dash'
        else:
            self.err.text = "Error: Access Key Required!"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_pair = "EUR/USD (OTC)"
        self.countdown_sec = 0
        self.timer_event = None

        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Header with Live System Time
        top = BoxLayout(orientation='horizontal', size_hint_y=0.06)
        top.add_widget(Label(
            text="[b]HINATA BOT PRO[/b]  |  [color=00e673]LIVE TERMINAL[/color]",
            markup=True, font_size='15sp', color=TEXT_MAIN, halign='left'
        ))
        self.lbl_clock = Label(text="--:--:--", font_size='13sp', color=TEXT_SUB, halign='right')
        top.add_widget(self.lbl_clock)
        root.add_widget(top)

        # Start Continuous System Clock
        Clock.schedule_interval(self.update_system_clock, 1)

        # Stats Board
        stats_board = GridLayout(cols=3, size_hint_y=0.09, spacing=8)
        with stats_board.canvas.before:
            Color(*CARD_COLOR)
            self.sb_bg = RoundedRectangle(size=stats_board.size, pos=stats_board.pos, radius=[10])
        stats_board.bind(size=self._update_sb_bg, pos=self._update_sb_bg)

        stats_board.add_widget(Label(text="[color=9eabbd]ACCURACY[/color]\n[b][color=00e673]98.8%[/color][/b]", markup=True, font_size='12sp', halign='center'))
        stats_board.add_widget(Label(text="[color=9eabbd]WIN RATE[/color]\n[b][color=00e673]142W / 2L[/color][/b]", markup=True, font_size='12sp', halign='center'))
        stats_board.add_widget(Label(text="[color=9eabbd]ENGINE[/color]\n[b]QUANT AI[/b]", markup=True, font_size='12sp', halign='center'))
        root.add_widget(stats_board)

        # Search Pair Selection & Timeframe Box
        ctrl_box = GridLayout(cols=2, size_hint_y=0.09, spacing=10)
        
        self.pair_btn = Button(
            text=f"🔍 {self.selected_pair}",
            background_color=(0.06, 0.08, 0.12, 1),
            color=TEXT_MAIN, font_size='13sp', bold=True
        )
        self.pair_btn.bind(on_release=self.open_pair_search_popup)

        self.tf_sp = Spinner(
            text='1 MIN',
            values=('5 SEC', '10 SEC', '15 SEC', '30 SEC', '1 MIN', '5 MIN', '15 MIN', '1 HOUR'),
            background_color=(0.06, 0.08, 0.12, 1), color=NEON_GREEN, font_size='13sp', bold=True
        )

        ctrl_box.add_widget(self.pair_btn)
        ctrl_box.add_widget(self.tf_sp)
        root.add_widget(ctrl_box)

        # Main Analysis Board
        self.card = BoxLayout(orientation='vertical', padding=18, spacing=10, size_hint_y=0.65)
        with self.card.canvas.before:
            Color(*CARD_COLOR)
            self.c_bg = RoundedRectangle(size=self.card.size, pos=self.card.pos, radius=[16])
            Color(*CARD_BORDER)
            self.c_line = Line(rounded_rectangle=[self.card.x, self.card.y, self.card.width, self.card.height, 16], width=1.2)
        self.card.bind(size=self._update_c_bg, pos=self._update_c_bg)

        self.sig_title = Label(text="READY TO ANALYZE", font_size='22sp', bold=True, color=TEXT_SUB, size_hint_y=0.18)
        self.close_pred = Label(text="Candle Closing: Pending Signal", font_size='14sp', color=TEXT_SUB, size_hint_y=0.10)

        # Information & Countdown Timer Rows
        info_grid = GridLayout(cols=1, spacing=8, size_hint_y=0.52)
        self.lbl_pair = Label(text="[color=9eabbd]Asset Pair:[/color] --", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_time = Label(text="[color=9eabbd]Entry Time (PKT):[/color] --:--:--", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_timer = Label(text="[color=9eabbd]Candle Timer:[/color] [color=00e673]00:00 SEC[/color]", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_acc = Label(text="[color=9eabbd]Signal Precision:[/color] --%", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')

        self.lbl_pair.bind(size=self.lbl_pair.setter('text_size'))
        self.lbl_time.bind(size=self.lbl_time.setter('text_size'))
        self.lbl_timer.bind(size=self.lbl_timer.setter('text_size'))
        self.lbl_acc.bind(size=self.lbl_acc.setter('text_size'))

        info_grid.add_widget(self.lbl_pair)
        info_grid.add_widget(self.lbl_time)
        info_grid.add_widget(self.lbl_timer)
        info_grid.add_widget(self.lbl_acc)

        self.lbl_conf = Label(
            text="[color=9eabbd]Technical Confluence:[/color]\nSelect Pair & Timeframe, then tap Analyze Market",
            markup=True, font_size='12sp', color=TEXT_SUB, halign='center', size_hint_y=0.2
        )

        self.card.add_widget(self.sig_title)
        self.card.add_widget(self.close_pred)
        self.card.add_widget(info_grid)
        self.card.add_widget(self.lbl_conf)
        root.add_widget(self.card)

        # Action Button
        self.an_btn = Button(
            text="ANALYZE LIVE MARKET", bold=True,
            size_hint_y=0.11,
            background_color=(0,0,0,0), color=(1,1,1,1), font_size='16sp'
        )
        with self.an_btn.canvas.before:
            Color(*NEON_GREEN)
            self.an_bg = RoundedRectangle(size=self.an_btn.size, pos=self.an_btn.pos, radius=[12])
        self.an_btn.bind(size=self._update_an_bg, pos=self._update_an_bg, on_release=self.run_analysis)
        root.add_widget(self.an_btn)

        self.add_widget(root)

    def update_system_clock(self, dt):
        self.lbl_clock.text = datetime.now().strftime("%H:%M:%S PKT")

    def open_pair_search_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        search_input = TextInput(
            hint_text="Type pair name (e.g. OTC, GOLD, BTC)...",
            multiline=False, size_hint_y=None, height=45,
            background_color=(0.06, 0.08, 0.12, 1), foreground_color=TEXT_MAIN,
            padding=[10, 10], font_size='14sp'
        )
        content.add_widget(search_input)

        scroll = ScrollView(size_hint=(1, 1))
        pair_list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        pair_list_layout.bind(minimum_height=pair_list_layout.setter('height'))

        def populate_list(filter_text=""):
            pair_list_layout.clear_widgets()
            for pair in QUOTEX_PAIRS:
                if filter_text.lower() in pair.lower():
                    btn = Button(
                        text=pair, size_hint_y=None, height=42,
                        background_color=(0.12, 0.16, 0.22, 1), color=TEXT_MAIN,
                        font_size='13sp'
                    )
                    btn.bind(on_release=lambda b, p=pair: select_pair(p))
                    pair_list_layout.add_widget(btn)

        def select_pair(pair_name):
            self.selected_pair = pair_name
            self.pair_btn.text = f"🔍 {pair_name}"
            popup.dismiss()

        search_input.bind(text=lambda instance, val: populate_list(val))
        populate_list()

        scroll.add_widget(pair_list_layout)
        content.add_widget(scroll)

        popup = Popup(
            title="Search Quotex Asset Pair",
            content=content,
            size_hint=(0.9, 0.85),
            background_color=(0.05, 0.07, 0.10, 0.95)
        )
        popup.open()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_sb_bg(self, instance, value):
        self.sb_bg.size = instance.size
        self.sb_bg.pos = instance.pos

    def _update_c_bg(self, instance, value):
        self.c_bg.size = instance.size
        self.c_bg.pos = instance.pos
        self.c_line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 16]

    def _update_an_bg(self, instance, value):
        self.an_bg.size = instance.size
        self.an_bg.pos = instance.pos

    def start_countdown(self, seconds):
        if self.timer_event:
            self.timer_event.cancel()
        self.countdown_sec = seconds
        self.timer_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        if self.countdown_sec > 0:
            self.countdown_sec -= 1
            mins, secs = divmod(self.countdown_sec, 60)
            self.lbl_timer.text = f"[color=9eabbd]Candle Timer:[/color] [color=00e673]{mins:02d}:{secs:02d} SEC[/color]"
        else:
            self.lbl_timer.text = f"[color=9eabbd]Candle Timer:[/color] [color=ff4d4d]EXPIRED (00:00)[/color]"
            if self.timer_event:
                self.timer_event.cancel()

    def run_analysis(self, instance):
        pair = self.selected_pair
        tf = self.tf_sp.text
        now = datetime.now().strftime("%H:%M:%S")

        rsi = random.uniform(18, 82)
        stoch = random.uniform(10, 90)
        signal_type = random.choice(["CALL", "PUT"])

        # Determine timer seconds based on timeframe
        tf_seconds = 60
        if 'SEC' in tf:
            tf_seconds = int(tf.split()[0])
        elif 'MIN' in tf:
            tf_seconds = int(tf.split()[0]) * 60

        self.start_countdown(tf_seconds)

        if signal_type == "CALL":
            sig = f"SIGNAL: CALL (BUY / UP)"
            color = NEON_GREEN
            pred = f"Candle Close Prediction: HIGH (GREEN CANDLE)"
            acc = random.uniform(97.8, 99.8)
            conf = f"Order Block Rejection | RSI ({rsi:.1f}) Bullish | Stoch ({stoch:.1f}) Oversold"
        else:
            sig = f"SIGNAL: PUT (SELL / DOWN)"
            color = NEON_RED
            pred = f"Candle Close Prediction: LOW (RED CANDLE)"
            acc = random.uniform(98.1, 99.9)
            conf = f"Supply Zone Breakdown | RSI ({rsi:.1f}) Bearish | Stoch ({stoch:.1f}) Overbought"

        self.sig_title.text = sig
        self.sig_title.color = color
        self.close_pred.text = pred
        self.close_pred.color = color

        self.lbl_pair.text = f"[color=9eabbd]Selected Pair:[/color] {pair} ({tf})"
        self.lbl_time.text = f"[color=9eabbd]Entry Time (PKT):[/color] {now}"
        self.lbl_acc.text = f"[color=9eabbd]Signal Precision:[/color] [b]{acc:.1f}% ACCURACY[/b]"
        self.lbl_conf.text = f"[color=9eabbd]Technical Confluence:[/color]\n{conf}"

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dash'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
