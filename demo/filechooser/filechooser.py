from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class MyFileChooser(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class FileChooserBox(BoxLayout):
    loadfile = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_load(self):
        content = MyFileChooser(load=self.load, cancel=self.dismiss_popup)
        # 打开一个弹窗
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        print(path, filename)
        self.dismiss_popup()

    def dismiss_popup(self):
        # 关闭弹窗
        self._popup.dismiss()


class FileChooserApp(App):
    def build(self):
        return FileChooserBox()


if __name__ == '__main__':
    FileChooserApp().run()
