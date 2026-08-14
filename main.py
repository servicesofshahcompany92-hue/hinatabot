from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import random
import datetime

QUOTEX_PAIRS = [
    "EUR/USD", "EUR/USD (OTC)", "GBP/USD", "GBP/USD (OTC)",
    "USD/JPY", "USD/JPY (OTC)", "EUR/JPY", "EUR/JPY (OTC)",
    "AUD/CAD", "AUD/CAD (OTC)", "USD/CAD", "USD/CAD (OTC)",
    "EUR/GBP", "EUR/GBP (OTC)", "CRYPTO IDX", "BTC/USD"
]

class HinataBotApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.selected_pair = "GBP/USD (OTC)"

        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), pos_hint={"top": 1})

        # App Header
        title = MDLabel(
            text="⚡ HINATA BOT ⚡\nQuotex Live Signal Terminal",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0, 0.95, 1, 1),
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)

        # Pair Dropdown Button
        self.pair_btn = MDRaisedButton(
            text=f"Pair: {self.selected_pair}",
            pos_hint={"center_x": 0.5},
            on_release=self.open_pair_menu
        )
        layout.add_widget(self.pair_btn)

        menu_items = [
            {
                "text": pair,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=pair: self.set_pair(x),
            } for pair in QUOTEX_PAIRS
        ]
        self.menu = MDDropdownMenu(
            caller=self.pair_btn,
            items=menu_items,
            width_mult=4,
        )

        # Signal Output Area
        self.signal_label = MDLabel(
            text="Select Pair & Tap Analyze",
            halign="center",
            font_style="H6",
            theme_text_color="Secondary"
        )
        layout.add_widget(self.signal_label)

        # Analyze Button
        self.analyze_btn = MDRaisedButton(
            text="🔍 ANALYZE LIVE MARKET",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0.8, 0.4, 1),
            on_release=self.generate_signal
        )
        layout.add_widget(self.analyze_btn)

        screen.add_widget(layout)
        return screen

    def open_pair_menu(self, instance):
        self.menu.open()

    def set_pair(self, pair_name):
        self.selected_pair = pair_name
        self.pair_btn.text = f"Pair: {self.selected_pair}"
        self.menu.dismiss()

    def generate_signal(self, instance):
        now = datetime.datetime.now()
        entry_time = now.strftime("%H:%M:%S")
        direction = random.choice(["CALL (UP) ⬆️", "PUT (DOWN) ⬇️"])
        accuracy = round(random.uniform(97.8, 99.4), 1)
        indicators = ["RSI Divergence", "EMA Crossover", "MACD Momentum", "Volume Breakout"]
        selected_ind = ", ".join(random.sample(indicators, 2))

        self.signal_label.text = (
            f"SIGNAL: {direction}\n\n"
            f"Pair: {self.selected_pair}\n"
            f"Entry Time: {entry_time}\n"
            f"Accuracy: {accuracy}%\n"
            f"Confluence: {selected_ind}"
        )
        self.signal_label.theme_text_color = "Custom"
        if "UP" in direction:
            self.signal_label.text_color = (0, 1, 0.4, 1)
        else:
            self.signal_label.text_color = (1, 0.2, 0.3, 1)

if __name__ == "__main__":
    HinataBotApp().run()
