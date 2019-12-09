import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from db.sqlite3_connect import insert_data, select_data, create_table
from custom_gestures.gesture_box import GestureBox


class SaveImageDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ResetDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MePage(GestureBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sql = 'SELECT * FROM user WHERE id=1'
        res = select_data(sql)
        self.ids.name_input.text = res[0][1]
        self.ids.me_word_num_box_input.text = str(res[0][2])
        self.ids.month_or_week.text = res[0][3]
        self.head_path = res[0][4]
        self.background_path = res[0][5]
        self.ids.me_main_box.canvas.before.children[0].source = self.background_path
        self.ids.test_image_box.canvas.after.children[2].source = self.head_path

    def dismiss_popup(self):
        """关闭弹窗"""
        self._popup.dismiss()

    def save_head_image(self, path, filename):
        """保存头像路径"""
        self.head_path = os.path.join(path, filename)
        self.ids.test_image_box.canvas.after.children[2].source = self.head_path
        self.dismiss_popup()

    @staticmethod
    def write_image_to_c0c(file_path):
        """将图片写入头像图片中"""
        with open(file_path, "rb") as f:
            file_data = f.read()
            with open('image/c0c.jpg', 'wb') as w:
                w.write(file_data)

    def show_head_image(self):
        """点击头像回调方法"""
        content = SaveImageDialog(save=self.save_head_image, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save_background_image(self, path, filename):
        """保存背景路径，重启生效"""
        self.background_path = os.path.join(path, filename)
        # self.canvas.children[0].children[0].source = self.background_path
        self.ids.me_main_box.canvas.before.children[0].source = self.background_path
        self.dismiss_popup()

    @staticmethod
    def write_image_to_back(file_path):
        """将文件写入背景图片中"""
        with open(file_path, "rb") as f:
            file_data = f.read()
            with open('image/back.jpg', 'wb') as w:
                w.write(file_data)

    def change_background_button(self):
        """点击change按钮回调方法"""
        content = SaveImageDialog(save=self.save_background_image, cancel=self.dismiss_popup)
        self._popup = Popup(title="Upload image", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save_all_changes(self):
        """保存修改"""
        name = self.ids.name_input.text
        try:
            num = int(self.ids.me_word_num_box_input.text)
        except ValueError:
            num = 50
        is_month = self.ids.month_or_week.text
        sql = "UPDATE user SET name='"+name+"',is_month='"+is_month+"',word_num='"+str(num)+"',head_image='"+self.head_path +"',background_image='"+self.background_path+"' WHERE id = 1"
        print(sql)
        insert_data(sql)

        # 改变头像、背景文件
        self.write_image_to_back(self.background_path)
        self.write_image_to_c0c(self.head_path)

        self.clear_widgets()
        self.__init__()
        self.set_change_value()
        self.return_info_button()

    def month_or_week(self):
        """月/周统计视图"""
        current = self.ids.month_or_week.text
        if current == 'Month':
            self.ids.month_or_week.text = 'Week'
        elif current == 'Week':
            self.ids.month_or_week.text = 'Month'

    def reset_all(self):
        """执行重置"""
        # 清除表内所有数据
        create_table()
        if os.name == 'posix':
            path = os.getcwd() + '/image'
        else:
            path = os.getcwd() + '\\image'
        # 更改头像
        c0c_path = os.path.join(path, 'c0c.jpg')
        c0c_bak_path = os.path.join(path, 'c0c_bak.jpg')
        self.write_image_to_c0c(c0c_bak_path)
        # 更改背景
        back_path = os.path.join(path, 'back.jpg')
        back_bak_path = os.path.join(path, 'back_bak.jpg')
        self.write_image_to_back(back_bak_path)
        # 更改名字 更改每日单词数 更改按月显示
        sql = "UPDATE user SET name='C0C',is_month='Month',word_num=50,head_image='"+c0c_path+"',background_image='"+back_path+"' WHERE id = 1"
        insert_data(sql)

        # 关闭弹窗
        self.dismiss_popup()
        self.clear_widgets()
        self.__init__()
        self.set_change_value()

    def reset_all_tip(self):
        """点击reset回调方法，弹出提示框"""
        content = ResetDialog(save=self.reset_all, cancel=self.dismiss_popup)
        self._popup = Popup(title="Reset all", content=content, size_hint=(0.6, 0.3))
        self._popup.open()

    def return_info_button(self):
        """返回主页"""
        self.clear_widgets()
        self.__init__()
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    def set_change_value(self):
        """设置改变的值"""
        # info页面
        info = App.get_running_app().screen_manager.get_screen('Info')
        # name
        info.children[0].ids.slide_name_label.text = self.ids.name_input.text
        # head
        info.children[0].ids.head_image_box.canvas.after.children[2].source = self.head_path
        # background
        info.children[0].ids.main_box.canvas.before.children[2].source = self.background_path

        # upload页面
        upload = App.get_running_app().screen_manager.get_screen('Upload')
        upload.children[0].ids.upload_main_box.canvas.before.children[1].source = self.background_path

    def return_review_button(self):
        """跳转到Review"""
        self.clear_widgets()
        self.__init__()
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Review'

    def return_upload_button(self):
        """跳转到Upload"""
        self.clear_widgets()
        self.__init__()
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Upload'
