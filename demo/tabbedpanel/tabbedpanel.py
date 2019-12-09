from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel


class TabbedPanelTest(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TabbedPanelApp(App):
    def build(self):
        return TabbedPanelTest()


if __name__ == '__main__':
    TabbedPanelApp().run()
