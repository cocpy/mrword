from kivy.app import App
from kivy.uix.widget import Widget


class ButtonWidget(Widget):
    pass


class ButtonApp(App):
    def build(self):
        return ButtonWidget()


ButtonApp().run()
