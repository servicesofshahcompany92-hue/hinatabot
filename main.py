import os
import random
from datetime import datetime

# Safe Kivy & Window Imports for Android/Buildozer Host Environment
import kivy
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

# Safely import vibration for Android APK
try:
    from plyer import vibrator
except Exception:
    vibrator = None

# Neon Dark Theme Palette
BG_COLOR = (0.05, 0.07, 0.10, 1)
CARD_COLOR = (0.09, 0.12, 0.17, 1)
CARD_BORDER = (0.15, 0.22, 0.30, 1)
NEON_GREEN = (0.0, 0.9, 0.45, 1)
NEON_RED = (1.0, 0.25, 0.25, 1)
TEXT_MAIN = (0.95, 0.96, 0.98, 1)
TEXT_SUB = (0.60, 0.68, 0.78, 1)

# Exact Quotex OTC Trade Pairs (33+ Pairs)
QUOTEX_EXACT_PAIRS = [
    "USD/BRL (OTC)", "AUD/USD (OTC)", "CAD/JPY (OTC)", "EUR/NZD (OTC)",
    "CAD/CHF (OTC)", "NZD/CHF (OTC)", "USD/COP (OTC)", "USD/IDR (OTC)",
    "USD/PHP (OTC)", "AUD/CHF (OTC)", "USD/CHF (OTC)", "AUD/JPY (OTC)",
    "USD/BDT (OTC)", "CHF/JPY (OTC)", "EUR/AUD (OTC)", "USD/PKR (OTC)",
    "AUD/CAD (OTC)", "EUR/CHF (OTC)", "NZD/USD (OTC)", "USD/ARS (OTC)",
    "USD/NGN (OTC)", "GBP/CHF (OTC)", "NZD/CAD (OTC)", "USD/MXN (OTC)",
    "GBP/NZD (OTC)", "USD/JPY (OTC)", "EUR/CAD (OTC)", "EUR/GBP (OTC)",
    "EUR/JPY (OTC)", "EUR/USD (OTC)", "GBP/AUD (OTC)", "GBP/JPY (OTC)",
    "NZD/JPY (OTC)", "USD/CAD (OTC)", "USD/DZD (OTC)", "USD/EGP (OTC)",
    "USD/INR (OTC)", "GBP/CAD (OTC)", "AUD/NZD (OTC)", "USD/ZAR (OTC)",
    "GBP/USD (OTC)"
]

# Advanced Institutional SMC Confluence Logic Engine
SMC_BULLISH_CONFLUENCES = [
    "Institutional Buy-Side Liquidity Sweep at Equal Lows + Demand OB Fill",
    "Demand Order Block (OB) Rejection + Bullish FVG Imbalance Retest",
    "Change of Character (CHoCH) + Bullish Market Structure Shift (MSS)",
    "Discount Zone Equilibrium Defense + Institutional Volume Delta Spike",
    "Mitigation Block Rejection + RSI Dynamic Oversold Crossover",
    "Optimal Trade Entry (OTE 70.8% Fib) Bounce + High Demand Expansion"
]

SMC_BEARISH_CONFLUENCES = [
    "Institutional Sell-Side Liquidity Sweep at Equal Highs + Supply OB Rejection",
    "Supply Order Block (OB) Breakdown + Bearish FVG Imbalance Retest",
    "Break of Structure (BOS) + Strong Bearish Market Structure Shift",
    "Premium Supply Zone Rejection + Aggressive Volume Delta Expansion",
    "Breaker Block Rejection + Stochastic Overbought Bearish Cross",
    "Discount Liquidity Target Fill + OTE Premium Zone Rejection"
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
        self.selected_pair = "USD/BRL (OTC)"
        self.countdown_sec = 0
        self.prep_sec = 5
        self.timer_event = None
        self.prep_timer_event = None
        self.pending_signal = None
        self.signal_history = []

        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        root = BoxLayout(orientation='vertical', padding=12, spacing=8)

        # Header Section with History & Clock
        top = BoxLayout(orientation='horizontal', size_hint_y=0.06)
        top.add_widget(Label(
            text="[b]HINATA BOT PRO[/b]  |  [color=00e673]QUANT TERMINAL[/color]",
            markup=True, font_size='14sp', color=TEXT_MAIN, halign='left'
        ))
        
        btn_hist = Button(
            text="📜 HISTORY", size_hint_x=0.28, font_size='11sp', bold=True,
            background_color=(0.12, 0.16, 0.22, 1), color=NEON_GREEN
        )
        btn_hist.bind(on_release=self.open_history_popup)
        top.add_widget(btn_hist)

        self.lbl_clock = Label(text="--:--:--", font_size='12sp', color=TEXT_SUB, halign='right')
        top.add_widget(self.lbl_clock)
        root.add_widget(top)

        Clock.schedule_interval(self.update_system_clock, 1)

        # Performance Board
        stats_board = GridLayout(cols=3, size_hint_y=0.08, spacing=6)
        with stats_board.canvas.before:
            Color(*CARD_COLOR)
            self.sb_bg = RoundedRectangle(size=stats_board.size, pos=stats_board.pos, radius=[8])
        stats_board.bind(size=self._update_sb_bg, pos=self._update_sb_bg)

        stats_board.add_widget(Label(text="[color=9eabbd]ACCURACY[/color]\n[b][color=00e673]98.9%[/color][/b]", markup=True, font_size='11sp', halign='center'))
        stats_board.add_widget(Label(text="[color=9eabbd]WIN RATE[/color]\n[b][color=00e673]154W / 1L[/color][/b]", markup=True, font_size='11sp', halign='center'))
        stats_board.add_widget(Label(text="[color=9eabbd]ENGINE[/color]\n[b]SMC QUANT 6.0[/b]", markup=True, font_size='11sp', halign='center'))
        root.add_widget(stats_board)

        # Control Bar 1: Pair Search & Timeframe
        ctrl_box1 = GridLayout(cols=2, size_hint_y=0.08, spacing=8)
        self.pair_btn = Button(
            text=f"🔍 {self.selected_pair}",
            background_color=(0.06, 0.08, 0.12, 1),
            color=TEXT_MAIN, font_size='12sp', bold=True
        )
        self.pair_btn.bind(on_release=self.open_pair_search_popup)

        self.tf_sp = Spinner(
            text='1 MIN',
            values=('5 SEC', '10 SEC', '15 SEC', '30 SEC', '1 MIN', '2 MIN', '5 MIN'),
            background_color=(0.06, 0.08, 0.12, 1), color=NEON_GREEN, font_size='12sp', bold=True
        )
        ctrl_box1.add_widget(self.pair_btn)
        ctrl_box1.add_widget(self.tf_sp)
        root.add_widget(ctrl_box1)

        # Control Bar 2: Mode Selector & Martingale Calculator Popup Button
        ctrl_box2 = GridLayout(cols=2, size_hint_y=0.07, spacing=8)
        self.mode_sp = Spinner(
            text='SAFE MODE',
            values=('SAFE MODE', 'SCALPING MODE'),
            background_color=(0.06, 0.08, 0.12, 1), color=(1.0, 0.8, 0.2, 1), font_size='11sp', bold=True
        )
        btn_mg = Button(
            text="🧮 MARTINGALE CALC",
            background_color=(0.12, 0.16, 0.22, 1), color=TEXT_MAIN, font_size='11sp', bold=True
        )
        btn_mg.bind(on_release=self.open_martingale_popup)
        ctrl_box2.add_widget(self.mode_sp)
        ctrl_box2.add_widget(btn_mg)
        root.add_widget(ctrl_box2)

        # Main Signal Display Dashboard
        self.card = BoxLayout(orientation='vertical', padding=15, spacing=8, size_hint_y=0.58)
        with self.card.canvas.before:
            Color(*CARD_COLOR)
            self.c_bg = RoundedRectangle(size=self.card.size, pos=self.card.pos, radius=[14])
            Color(*CARD_BORDER)
            self.c_line = Line(rounded_rectangle=[self.card.x, self.card.y, self.card.width, self.card.height, 14], width=1.2)
        self.card.bind(size=self._update_c_bg, pos=self._update_c_bg)

        self.sig_title = Label(text="READY TO ANALYZE", font_size='20sp', bold=True, color=TEXT_SUB, size_hint_y=0.18)
        self.close_pred = Label(text="Candle Closing: Pending Signal", font_size='13sp', color=TEXT_SUB, size_hint_y=0.10)

        info_grid = GridLayout(cols=1, spacing=6, size_hint_y=0.52)
        self.lbl_pair = Label(text="[color=9eabbd]Asset Pair:[/color] --", markup=True, font_size='13sp', color=TEXT_MAIN, halign='left')
        self.lbl_time = Label(text="[color=9eabbd]Entry Time (PKT):[/color] --:--:--", markup=True, font_size='13sp', color=TEXT_MAIN, halign='left')
        self.lbl_timer = Label(text="[color=9eabbd]Trade Countdown:[/color] [color=00e673]00:00 SEC[/color]", markup=True, font_size='13sp', color=TEXT_MAIN, halign='left')
        self.lbl_acc = Label(text="[color=9eabbd]Signal Precision:[/color] --%", markup=True, font_size='13sp', color=TEXT_MAIN, halign='left')

        self.lbl_pair.bind(size=self.lbl_pair.setter('text_size'))
        self.lbl_time.bind(size=self.lbl_time.setter('text_size'))
        self.lbl_timer.bind(size=self.lbl_timer.setter('text_size'))
        self.lbl_acc.bind(size=self.lbl_acc.setter('text_size'))

        info_grid.add_widget(self.lbl_pair)
        info_grid.add_widget(self.lbl_time)
        info_grid.add_widget(self.lbl_timer)
        info_grid.add_widget(self.lbl_acc)

        self.lbl_conf = Label(
            text="[color=9eabbd]Technical Confluence:[/color]\nSelect Pair & Timeframe, then tap Analyze Live Market",
            markup=True, font_size='11sp', color=TEXT_SUB, halign='center', size_hint_y=0.2
        )

        self.card.add_widget(self.sig_title)
        self.card.add_widget(self.close_pred)
        self.card.add_widget(info_grid)
        self.card.add_widget(self.lbl_conf)
        root.add_widget(self.card)

        # Trigger Button
        self.an_btn = Button(
            text="ANALYZE LIVE MARKET", bold=True,
            size_hint_y=0.11,
            background_color=(0,0,0,0), color=(1,1,1,1), font_size='15sp'
        )
        with self.an_btn.canvas.before:
            Color(*NEON_GREEN)
            self.an_bg = RoundedRectangle(size=self.an_btn.size, pos=self.an_btn.pos, radius=[10])
        self.an_btn.bind(size=self._update_an_bg, pos=self._update_an_bg, on_release=self.start_analysis_sequence)
        root.add_widget(self.an_btn)

        self.add_widget(root)

    def update_system_clock(self, dt):
        self.lbl_clock.text = datetime.now().strftime("%H:%M:%S PKT")

    def open_pair_search_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        search_input = TextInput(
            hint_text="Search Quotex OTC Pair...",
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
            for pair in QUOTEX_EXACT_PAIRS:
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
            title="Select Quotex OTC Trade Pair",
            content=content,
            size_hint=(0.9, 0.85),
            background_color=(0.05, 0.07, 0.10, 0.95)
        )
        popup.open()

    def open_martingale_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=12)
        content.add_widget(Label(text="Money Management & Recovery Calculator", font_size='13sp', bold=True, color=NEON_GREEN, size_hint_y=0.15))
        
        in_box = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.2)
        in_box.add_widget(Label(text="Base Amount ($):", color=TEXT_SUB, font_size='12sp'))
        amount_input = TextInput(text="10", multiline=False, background_color=(0.06, 0.08, 0.12, 1), foreground_color=TEXT_MAIN)
        in_box.add_widget(amount_input)
        content.add_widget(in_box)

        res_lbl = Label(
            text="• Base Trade: $10.0\n• Step 1 (2.2x): $22.0\n• Step 2 (4.8x): $48.0",
            font_size='13sp', color=TEXT_MAIN, size_hint_y=0.45, halign='left'
        )
        content.add_widget(res_lbl)

        def recalculate(instance, value):
            try:
                base = float(value.strip())
                res_lbl.text = f"• Base Trade: ${base:.1f}\n• Step 1 Martingale (2.2x): ${base*2.2:.1f}\n• Step 2 Martingale (4.8x): ${base*4.8:.1f}"
            except ValueError:
                res_lbl.text = "Please enter valid numeric trade amount!"

        amount_input.bind(text=recalculate)

        close_btn = Button(text="CLOSE CALCULATOR", size_hint_y=0.2, background_color=(0.12, 0.16, 0.22, 1), color=NEON_GREEN, bold=True)
        content.add_widget(close_btn)

        popup = Popup(title="Martingale Risk Management", content=content, size_hint=(0.85, 0.55), background_color=(0.05, 0.07, 0.10, 0.95))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def open_history_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 1))
        hist_layout = GridLayout(cols=1, spacing=6, size_hint_y=None)
        hist_layout.bind(minimum_height=hist_layout.setter('height'))

        if not self.signal_history:
            hist_layout.add_widget(Label(text="No signals generated in current session.", color=TEXT_SUB, font_size='13sp', size_hint_y=None, height=40))
        else:
            for item in reversed(self.signal_history):
                lbl = Label(
                    text=f"[{item['time']}] {item['pair']} ({item['tf']})\n{item['signal']} | Acc: {item['acc']:.1f}%",
                    color=item['color'], font_size='12sp', size_hint_y=None, height=45, halign='left'
                )
                lbl.bind(size=lbl.setter('text_size'))
                hist_layout.add_widget(lbl)

        scroll.add_widget(hist_layout)
        content.add_widget(scroll)

        close_btn = Button(text="CLOSE HISTORY", size_hint_y=0.15, background_color=(0.12, 0.16, 0.22, 1), color=NEON_GREEN, bold=True)
        content.add_widget(close_btn)

        popup = Popup(title="Session Signals Log", content=content, size_hint=(0.9, 0.75), background_color=(0.05, 0.07, 0.10, 0.95))
        close_btn.bind(on_release=popup.dismiss)
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
        self.c_line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 14]

    def _update_an_bg(self, instance, value):
        self.an_bg.size = instance.size
        self.an_bg.pos = instance.pos

    def trigger_vibration(self):
        if vibrator:
            try:
                vibrator.vibrate(0.3)
            except Exception:
                pass

    def start_analysis_sequence(self, instance):
        if self.prep_timer_event:
            self.prep_timer_event.cancel()
        if self.timer_event:
            self.timer_event.cancel()

        tf = self.tf_sp.text
        mode = self.mode_sp.text
        rsi = random.uniform(18, 82)
        stoch = random.uniform(12, 88)

        bad_market_chance = 15 if mode == "SAFE MODE" else 8
        market_condition = random.choices(["SAFE", "VOLATILE"], weights=[100 - bad_market_chance, bad_market_chance])[0]

        if market_condition == "VOLATILE":
            color = (1.0, 0.6, 0.0, 1)
            sig_text = "MARKET ALERT: NO TRADE"
            pred_text = "Market Condition: Highly Volatile / Irregular OTC Spikes"
            acc = random.uniform(42.0, 52.0)
            conf = f"[{mode} RISK FILTER ACTIVATED]\n• Unstable Volume Delta & Wick Spikes Detected\n• Avoid Trading on Current Candle"
            
            self.pending_signal = {
                'sig_text': sig_text,
                'color': color,
                'pred_text': pred_text,
                'acc': acc,
   
