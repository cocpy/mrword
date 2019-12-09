from kivy.app import App
from kivy.uix.widget import Widget


class ImageWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ImageApp(App):
    def build(self):
        return ImageWidget()


if __name__=='__main__':
    ImageApp().run()