from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class SpinnerBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SpinnerApp(App):
    def build(self):
        return SpinnerBox()


if __name__ == '__main__':
    SpinnerApp().run()
