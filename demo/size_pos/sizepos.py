from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class SizePosFloat(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SizePosApp(App):
    def build(self):
        return SizePosFloat()


if __name__ == '__main__':
    SizePosApp().run()
