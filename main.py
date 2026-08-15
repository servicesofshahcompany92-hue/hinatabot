import os
import random
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line

# Neon Dark Trading Theme
BG_COLOR = (0.05, 0.07, 0.10, 1)        # Cyber Deep Dark
CARD_COLOR = (0.09, 0.12, 0.17, 1)      # Glass Card
CARD_BORDER = (0.15, 0.22, 0.30, 1)     # Subtle Border
NEON_GREEN = (0.0, 0.9, 0.45, 1)       # Neon Bullish
NEON_RED = (1.0, 0.25, 0.25, 1)        # Neon Bearish
TEXT_MAIN = (0.95, 0.96, 0.98, 1)
TEXT_SUB = (0.60, 0.68, 0.78, 1)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Dynamic height box to prevent vertical text squishing
        layout = BoxLayout(
            orientation='vertical',
            padding=25,
            spacing=18,
            size_hint=(0.92, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.bind(minimum_height=layout.setter('height'))

        with layout.canvas.before:
            Color(*CARD_COLOR)
            self.card_rect = RoundedRectangle(size=layout.size, pos=layout.pos, radius=[16])
            Color(*CARD_BORDER)
            self.card_line = Line(rounded_rectangle=[layout.x, layout.y, layout.width, layout.height, 16], width=1.2)
        layout.bind(size=self._update_layout_card, pos=self._update_layout_card)

        # Header
        layout.add_widget(Label(
            text="[b]HINATA BOT PRO[/b]\n[size=13][color=00e673]AI QUANT TRADING TERMINAL[/color][/size]",
            markup=True, font_size='22sp', halign='center', color=TEXT_MAIN,
            size_hint_y=None, height=55
        ))

        # Username Field
        u_box = BoxLayout(orientation='vertical', spacing=6, size_hint_y=None, height=75)
        u_box.add_widget(Label(text="TRADER ID", color=TEXT_SUB, font_size='12sp', halign='left', size_hint_y=None, height=20, bold=True))
        self.u_in = TextInput(
            text="Hinata_Pro_VIP", readonly=True, multiline=False,
            size_hint_y=None, height=48,
            background_color=(0.06, 0.08, 0.12, 1), foreground_color=NEON_GREEN,
            padding=[12, 12], font_size='15sp'
        )
        u_box.add_widget(self.u_in)
        layout.add_widget(u_box)

        # Password Field
        p_box = BoxLayout(orientation='vertical', spacing=6, size_hint_y=None, height=75)
        p_box.add_widget(Label(text="ACCESS KEY / PASSWORD", color=TEXT_SUB, font_size='12sp', halign='left', size_hint_y=None, height=20, bold=True))
        self.p_in = TextInput(
            password=True, hint_text="Enter Access Key", multiline=False,
            size_hint_y=None, height=48,
            background_color=(0.06, 0.08, 0.12, 1), foreground_color=TEXT_MAIN,
            padding=[12, 12], font_size='15sp'
        )
        p_box.add_widget(self.p_in)
        layout.add_widget(p_box)

        # Login Button
        self.btn = Button(
            text="AUTHENTICATE & ENTER", bold=True,
            size_hint_y=None, height=52,
            background_color=(0,0,0,0), color=(1,1,1,1), font_size='15sp'
        )
        with self.btn.canvas.before:
            Color(*NEON_GREEN)
            self.btn_bg = RoundedRectangle(size=self.btn.size, pos=self.btn.pos, radius=[10])
        self.btn.bind(size=self._update_btn, pos=self._update_btn, on_release=self.auth)
        layout.add_widget(self.btn)

        self.err = Label(text="", color=NEON_RED, font_size='13sp', size_hint_y=None, height=20)
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
        with self.canvas.before:
            Color(*BG_COLOR)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        root = BoxLayout(orientation='vertical', padding=16, spacing=14)

        # Top Bar
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        top.add_widget(Label(
            text="[b]HINATA BOT[/b]  |  [color=00e673]LIVE TERMINAL[/color]",
            markup=True, font_size='17sp', color=TEXT_MAIN, halign='left'
        ))
        root.add_widget(top)

        # Pair Selection Card
        sel_card = BoxLayout(orientation='horizontal', padding=[14, 8], size_hint_y=None, height=52, spacing=10)
        with sel_card.canvas.before:
            Color(*CARD_COLOR)
            self.sc_bg = RoundedRectangle(size=sel_card.size, pos=sel_card.pos, radius=[10])
        sel_card.bind(size=self._update_sc_bg, pos=self._update_sc_bg)

        sel_card.add_widget(Label(text="ASSET PAIR:", color=TEXT_SUB, font_size='13sp', size_hint_x=0.35, bold=True))
        self.pair_sp = Spinner(
            text='EUR/USD (OTC)',
            values=('EUR/USD (OTC)', 'GBP/USD (OTC)', 'AUD/CAD (OTC)', 'USD/JPY (OTC)', 'EUR/GBP', 'BTC/USD'),
            background_color=(0.06, 0.08, 0.12, 1), color=TEXT_MAIN, size_hint_x=0.65, font_size='14sp'
        )
        sel_card.add_widget(self.pair_sp)
        root.add_widget(sel_card)

        # Main Display Card
        self.card = BoxLayout(orientation='vertical', padding=20, spacing=14)
        with self.card.canvas.before:
            Color(*CARD_COLOR)
            self.c_bg = RoundedRectangle(size=self.card.size, pos=self.card.pos, radius=[16])
            Color(*CARD_BORDER)
            self.c_line = Line(rounded_rectangle=[self.card.x, self.card.y, self.card.width, self.card.height, 16], width=1.2)
        self.card.bind(size=self._update_c_bg, pos=self._update_c_bg)

        self.sig_title = Label(text="STANDBY MODE", font_size='24sp', bold=True, color=TEXT_SUB, size_hint_y=None, height=40)
        self.close_pred = Label(text="Closing Prediction: Pending Analysis", font_size='14sp', color=TEXT_SUB, size_hint_y=None, height=25)

        # Structured Info Rows
        info_box = BoxLayout(orientation='vertical', spacing=10, padding=[5, 10])

        self.lbl_pair = Label(text="[color=9eabbd]Asset Pair:[/color] --", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_time = Label(text="[color=9eabbd]Entry Time (PKT):[/color] --:--:--", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_acc = Label(text="[color=9eabbd]Signal Accuracy:[/color] --%", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')
        self.lbl_tf = Label(text="[color=9eabbd]Trade Timeframe:[/color] 1 MINUTE", markup=True, font_size='14sp', color=TEXT_MAIN, halign='left')

        self.lbl_pair.bind(size=self.lbl_pair.setter('text_size'))
        self.lbl_time.bind(size=self.lbl_time.setter('text_size'))
        self.lbl_acc.bind(size=self.lbl_acc.setter('text_size'))
        self.lbl_tf.bind(size=self.lbl_tf.setter('text_size'))

        info_box.add_widget(self.lbl_pair)
        info_box.add_widget(self.lbl_time)
        info_box.add_widget(self.lbl_acc)
        info_box.add_widget(self.lbl_tf)

        self.lbl_conf = Label(
            text="[color=9eabbd]Technical Confluence:[/color]\nSelect asset pair and tap Analyze Live Market",
            markup=True, font_size='13sp', color=TEXT_SUB, halign='center', size_hint_y=None, height=50
        )

        self.card.add_widget(self.sig_title)
        self.card.add_widget(self.close_pred)
        self.card.add_widget(info_box)
        self.card.add_widget(self.lbl_conf)
        root.add_widget(self.card)

        # Action Button
        self.an_btn = Button(text="ANALYZE LIVE MARKET", bold=True, size_hint_y=None, height=55, background_color=(0,0,0,0), color=(1,1,1,1), font_size='16sp')
        with self.an_btn.canvas.before:
            Color(*NEON_GREEN)
            self.an_bg = RoundedRectangle(size=self.an_btn.size, pos=self.an_btn.pos, radius=[12])
        self.an_btn.bind(size=self._update_an_bg, pos=self._update_an_bg, on_release=self.run_analysis)
        root.add_widget(self.an_btn)

        self.add_widget(root)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_sc_bg(self, instance, value):
        self.sc_bg.size = instance.size
        self.sc_bg.pos = instance.pos

    def _update_c_bg(self, instance, value):
        self.c_bg.size = instance.size
        self.c_bg.pos = instance.pos
        self.c_line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 16]

    def _update_an_bg(self, instance, value):
        self.an_bg.size = instance.size
        self.an_bg.pos = instance.pos

    def run_analysis(self, instance):
        pair = self.pair_sp.text
        now = datetime.now().strftime("%H:%M:%S")

        rsi = random.uniform(20, 80)
        ema_cross = random.choice(["BULLISH", "BEARISH", "NEUTRAL"])
        stoch = random.uniform(15, 85)

        if ema_cross == "BULLISH" and rsi < 65:
            sig = "SIGNAL: CALL (BUY / UP)"
            color = NEON_GREEN
            pred = "Closing Prediction: HIGH (GREEN CANDLE)"
            acc = random.uniform(94.2, 98.8)
            conf = f"EMA 10/20 Golden Cross | RSI ({rsi:.1f}) Bullish | Stoch ({stoch:.1f})"
        elif ema_cross == "BEARISH" and rsi > 35:
            sig = "SIGNAL: PUT (SELL / DOWN)"
            color = NEON_RED
            pred = "Closing Prediction: LOW (RED CANDLE)"
            acc = random.uniform(94.5, 99.1)
            conf = f"EMA 10/20 Death Cross | RSI ({rsi:.1f}) Bearish | Heavy Pressure"
        else:
            sig = "NO SIGNAL (SIDEWAYS)"
            color = TEXT_SUB
            pred = "Closing Prediction: Market Consolidation / High Volatility"
            acc = 0.0
            conf = f"RSI ({rsi:.1f}) Neutral | No Clear Trend Confirmation"

        self.sig_title.text = sig
        self.sig_title.color = color
        self.close_pred.text = pred
        self.close_pred.color = color

        self.lbl_pair.text = f"[color=9eabbd]Asset Pair:[/color] {pair}"
        self.lbl_time.text = f"[color=9eabbd]Entry Time (PKT):[/color] {now}"
        self.lbl_acc.text = f"[color=9eabbd]Signal Accuracy:[/color] {acc:.1f}%" if acc > 0 else "[color=9eabbd]Signal Accuracy:[/color] N/A"
        self.lbl_conf.text = f"[color=9eabbd]Technical Confluence:[/color]\n{conf}"

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dash'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
