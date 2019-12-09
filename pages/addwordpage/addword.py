from kivy.app import App
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from db.sqlite3_connect import select_data, insert_data

from custom_gestures.gesture_box import GestureBox
from utils.common import num_of_word_to_study


class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text
        self.insert_today()

    def insert_today(self):
        """today表添加数据"""
        global word_id
        try:
            word_id = int(self.obj_text)
        except ValueError:
            select_id = "SELECT id FROM word WHERE word = '%s'" % self.obj_text
            rows = select_data(select_id)
            for row in rows:
                for col in row:
                    word_id = col
        finally:
            # 插入数据并更新word表添加次数
            insert_sql = "INSERT INTO today(word_id) SELECT '%d' WHERE NOT EXISTS(SELECT 1 FROM today WHERE word_id = '%d')" % (
            word_id, word_id)
            update_sql = "UPDATE word SET add_times = add_times + 1 WHERE id = '%d'" % word_id
            insert_data(insert_sql)
            insert_data(update_sql)
            print('%s is successful to add' % self.obj_text)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """将选择和焦点行为添加到视图中"""


class SelectableButton(RecycleDataViewBehavior, Button):
    """Add selection support to the Button"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def on_press(self):
        popup = TextInputPopup(self)


class AddWordPage(GestureBox):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_items.clear()
        self.word_num = num_of_word_to_study()
        # self.ids.rv_random_button.text = "Add %d words with random" % self.word_num
        self.get_words()

    def get_words(self):
        """获取待遍历的数据"""
        rows = select_data("SELECT id,word FROM word ORDER BY add_times")
        for row in rows:
            for col in row:
                self.data_items.append(col)

    def add_random_words(self):
        """添加n个随机的单词"""
        # sql = "INSERT INTO today(word_id) SELECT id FROM word WHERE NOT EXISTS(SELECT 1 FROM today WHERE word_id = id) AND add_times = 0 ORDER BY RANDOM() limit 50"
        self.word_num = num_of_word_to_study()
        res = select_data("SELECT id FROM word WHERE add_times = 0 ORDER BY RANDOM() limit %d" % self.word_num)
        for row in res:
            row_id = row[0]
            insert_data("UPDATE word SET add_times = 1 WHERE id = '%d'" % row_id)
            insert_data("INSERT INTO today(word_id) VALUES('%d')" % row_id)

    @staticmethod
    def add_word_to_review():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Review'

    @staticmethod
    def add_word_to_info():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Info'

    def add_word_refresh(self):
        self.clear_widgets()
        self.__init__()


class AddWordApp(App):
    title = "AddWord"

    def build(self):
        return AddWordPage()


if __name__ == "__main__":
    AddWordApp().run()
