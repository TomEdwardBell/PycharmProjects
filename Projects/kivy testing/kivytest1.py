import kivy

from kivy.app import App
from kivy.uix.widget import Widget


class CustomWidget(Widget):
    pass


class CustomWidgetApp(App):
    def build(self):
        return CustomWidget()


customWidget = CustomWidgetApp()

customWidget.run()