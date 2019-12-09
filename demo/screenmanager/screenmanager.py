from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# 创建两个页面
class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class ScreenManagerBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        self.add_widget(sm)


class ScreenManagerApp(App):
    def build(self):
        return ScreenManagerBox()


if __name__ == '__main__':
    ScreenManagerApp().run()
