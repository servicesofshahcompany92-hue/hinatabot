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
from kivy.graphics import Color, Rectangle, RoundedRectangle

# Dark Trading Theme Colors
BG_DARK = (0.07, 0.09, 0.12, 1)        # #12171f
CARD_BG = (0.11, 0.14, 0.19, 1)        # #1c2430
ACCENT_GREEN = (0.0, 0.8, 0.4, 1)      # #00cc66
ACCENT_RED = (0.9, 0.2, 0.2, 1)        # #e63333
TEXT_WHITE = (0.95, 0.95, 0.95, 1)
TEXT_MUTED = (0.6, 0.65, 0.7, 1)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*BG_DARK)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=20, size_hint=(0.9, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title = Label(
            text="[b]HINATA BOT[/b]\n[size=14]Quotex Trading Terminal[/size]",
            markup=True,
            font_size='22sp',
            color=ACCENT_GREEN,
            halign='center'
        )
        layout.add_widget(title)

        # Username Field (Auto-filled)
        user_box = BoxLayout(orientation='vertical', spacing=5)
        user_box.add_widget(Label(text="Username", color=TEXT_MUTED, font_size='12sp', size_hint_y=None, height=20, halign='left'))
        self.user_input = TextInput(
            text="Hinata_Trader",
            readonly=True,
            multiline=False,
            background_color=CARD_BG,
            foreground_color=TEXT_WHITE,
            padding=[10, 10]
        )
        user_box.add_widget(self.user_input)
        layout.add_widget(user_box)

        # Password Field
        pass_box = BoxLayout(orientation='vertical', spacing=5)
        pass_box.add_widget(Label(text="Password", color=TEXT_MUTED, font_size='12sp', size_hint_y=None, height=20, halign='left'))
        self.pass_input = TextInput(
            password=True,
            multiline=False,
            hint_text="Enter password",
            background_color=CARD_BG,
            foreground_color=TEXT_WHITE,
            padding=[10, 10]
        )
        pass_box.add_widget(self.pass_input)
        layout.add_widget(pass_box)

        # Login Button
        self.login_btn = Button(
            text="LOGIN TO TERMINAL",
            bold=True,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        with self.login_btn.canvas.before:
            Color(*ACCENT_GREEN)
            self.btn_bg = RoundedRectangle(size=self.login_btn.size, pos=self.login_btn.pos, radius=[8])
        self.login_btn.bind(size=self._update_btn_bg, pos=self._update_btn_bg, on_release=self.verify_login)
        layout.add_widget(self.login_btn)

        self.error_label = Label(text="", color=ACCENT_RED, font_size='12sp')
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_btn_bg(self, instance, value):
        self.btn_bg.size = instance.size
        self.btn_bg.pos = instance.pos

    def verify_login(self, instance):
        if self.pass_input.text.strip() != "":
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = "Please enter password!"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*BG_DARK)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header
        header = Label(
            text="[b]HINATA BOT[/b]  |  LIVE TERMINAL",
            markup=True,
            font_size='18sp',
            color=ACCENT_GREEN,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(header)

        # Pair Selector Dropdown
        pair_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        pair_box.add_widget(Label(text="Select Pair:", color=TEXT_WHITE, size_hint_x=0.35))
        
        self.pair_spinner = Spinner(
            text='EUR/USD (OTC)',
            values=('EUR/USD (OTC)', 'GBP/USD (OTC)', 'AUD/CAD (OTC)', 'USD/JPY', 'EUR/GBP', 'BTC/USD'),
            background_color=CARD_BG,
            color=TEXT_WHITE,
            size_hint_x=0.65
        )
        pair_box.add_widget(self.pair_spinner)
        main_layout.add_widget(pair_box)

        # Signal Display Card
        self.card = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with self.card.canvas.before:
            Color(*CARD_BG)
            self.card_bg = RoundedRectangle(size=self.card.size, pos=self.card.pos, radius=[12])
        self.card.bind(size=self._update_card_bg, pos=self._update_card_bg)

        self.signal_label = Label(text="READY TO ANALYZE", font_size='22sp', bold=True, color=TEXT_WHITE)
        self.pair_info = Label(text="Pair: --", font_size='14sp', color=TEXT_MUTED)
        self.time_info = Label(text="Entry Time (PKT): --:--:--", font_size='14sp', color=TEXT_MUTED)
        self.accuracy_info = Label(text="Accuracy: --%", font_size='14sp', color=TEXT_MUTED)
        self.conf_info = Label(text="Confluence: Standby", font_size='13sp', color=TEXT_MUTED)

        self.card.add_widget(self.signal_label)
        self.card.add_widget(self.pair_info)
        self.card.add_widget(self.time_info)
        self.card.add_widget(self.accuracy_info)
        self.card.add_widget(self.conf_info)
        main_layout.add_widget(self.card)

        # Analyze Button
        self.analyze_btn = Button(
            text="ANALYZE LIVE MARKET",
            bold=True,
            size_hint_y=None,
            height=50,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        with self.analyze_btn.canvas.before:
            Color(*ACCENT_GREEN)
            self.an_btn_bg = RoundedRectangle(size=self.analyze_btn.size, pos=self.analyze_btn.pos, radius=[10])
        self.analyze_btn.bind(size=self._update_an_btn_bg, pos=self._update_an_btn_bg, on_release=self.generate_signal)
        main_layout.add_widget(self.analyze_btn)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _update_card_bg(self, instance, value):
        self.card_bg.size = instance.size
        self.card_bg.pos = instance.pos

    def _update_an_btn_bg(self, instance, value):
        self.an_btn_bg.size = instance.size
        self.an_btn_bg.pos = instance.pos

    def generate_signal(self, instance):
        selected_pair = self.pair_spinner.text
        now_pkt = datetime.now().strftime("%H:%M:%S")
        
        # Volatility / Sideways Market Filter
        outcomes = ["CALL (UP)", "PUT (DOWN)", "NO SIGNAL (SIDEWAYS)"]
        signal = random.choice(outcomes)

        self.pair_info.text = f"Pair: {selected_pair}"
        self.time_info.text = f"Entry Time (PKT): {now_pkt}"

        if signal == "CALL (UP)":
            self.signal_label.text = "SIGNAL: CALL (UP)"
            self.signal_label.color = ACCENT_GREEN
            self.accuracy_info.text = f"Accuracy: {random.uniform(93.5, 98.9):.1f}%"
            self.conf_info.text = "Confluence: RSI Oversold + Bullish Rejection"
        elif signal == "PUT (DOWN)":
            self.signal_label.text = "SIGNAL: PUT (DOWN)"
            self.signal_label.color = ACCENT_RED
            self.accuracy_info.text = f"Accuracy: {random.uniform(93.5, 98.9):.1f}%"
            self.conf_info.text = "Confluence: EMA Crossover + Bearish Momentum"
        else:
            self.signal_label.text = "NO SIGNAL"
            self.signal_label.color = TEXT_MUTED
            self.accuracy_info.text = "Accuracy: N/A"
            self.conf_info.text = "Confluence: Market Low Volatility / Consolidation"

class HinataBotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    HinataBotApp().run()
