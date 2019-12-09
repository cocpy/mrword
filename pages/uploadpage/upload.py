import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory

from custom_gestures.gesture_box import GestureBox


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


Factory.register('SaveDialog', cls=SaveDialog)


class UploadPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_loop_worker = None

    def dismiss_popup(self):
        # 关闭弹窗
        self._popup.dismiss()

    def show_save(self):
        # 绑定保存和取消的方法
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload file", content=content, size_hint=(0.9, 0.9))
        # 打开窗口
        self._popup.open()

    def save(self, path, filename):
        from asyncio_task.asyncio_insert_data import EventLoopWorker
        file_path = os.path.join(path, filename)
        self.ids.status.text = file_path
        self.event_loop_worker = worker = EventLoopWorker(file_path)
        self.ids.upload_tip.text = "上传已开始，请勿重复上传！！！\n上传地址为下述地址："
        worker.start()

        self.dismiss_popup()

    @staticmethod
    def upload_to_index():
        # 移动趋势
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def upload_to_addword():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'AddWord'


class UploadApp(App):
    def build(self):
        return UploadPage()


if __name__ == '__main__':
    UploadApp().run()
