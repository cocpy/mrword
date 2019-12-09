import os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from db.sqlite3_connect import select_data, insert_data
from custom_gestures import gesture_nd as gesture
from utils.common import num_of_word_to_study


class ImageButton(ButtonBehavior, Image):
    """使用图片按钮"""
    pass


class InfoPage(gesture.GestureBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 读取下一个单词
        self.read_random_word()
        self.set_name()
        self.review_res = []

    def know_button_press(self):
        """Know 按钮被点击时执行该方法"""
        # 清除已认识的单词
        self.delete_today_word()
        self.insert_known_word()
        self.read_random_word()
        # self.__init__()

    def indistinct_button_press(self):
        """Indistinct 按钮被点击时执行该方法"""
        # 添加两个旧单词
        self.insert_unknown_word()
        self.insert_unknown_word()
        self.read_random_word()
        # self.__init__()

    def unknown_button_press(self):
        """Unknown 按钮被点击时执行该方法"""
        # 添加三个旧单词
        self.insert_unknown_word()
        self.insert_unknown_word()
        self.insert_unknown_word()
        self.read_random_word()
        # self.__init__()

    def read_random_word(self):
        """随机读取一条数据"""
        sql = "SELECT * FROM word WHERE id = (SELECT word_id FROM today ORDER BY RANDOM() limit 1)"
        rows = select_data(sql)
        if len(rows) == 0:
            # 先清除所有widgets
            self.ids.main_box.clear_widgets()
            # 添加需要显示的widgets
            # self.ids.main_box.add_widget(self.ids.personal_box)
            word_to_study = num_of_word_to_study()
            if word_to_study == 0:
                sql = "SELECT word_id FROM known WHERE id NOT IN(SELECT id FROM known WHERE (create_date > date('now','-1 day') AND add_times >= 0) OR (create_date > date('now','-3 day') AND add_times >= 1) OR (create_date > date('now','-7 day') AND add_times >= 2) OR (create_date > date('now','-14 day') AND add_times >= 3) OR (create_date > date('now','-30 day') AND add_times >= 4) OR (create_date > date('now','-60 day') AND add_times >= 5) OR (create_date > date('now','-150 day') AND add_times >= 6) OR (create_date > date('now','-365 day') AND add_times >= 7) OR (create_date > date('now','-770 day') AND add_times >= 8))"
                self.review_res = select_data(sql)
                if not len(self.review_res) > 0:
                    self.ids.main_box.add_widget(Label(text='[ref=review word]点击这段文字来开始复习达到遗忘临界点的单词!\n下拉刷新![/ref]',
                                                       markup=True, color=(0, 0, 0, 1), halign='center', font_name="site_packages/DroidSansFallback.ttf", on_ref_press=self.review_word))
                else:
                    self.ids.main_box.add_widget(Label(text='今日学习任务完成!', color=(0, 0, 0, 1), font_name="site_packages/DroidSansFallback.ttf"))
            else:
                self.ids.main_box.add_widget(Label(text='[ref=add word]还需添加 %s 个单词!\n下拉刷新![/ref]' % word_to_study,
                                                   markup=True, color=(0, 0, 0, 1), font_name="site_packages/DroidSansFallback.ttf",
                                                   on_ref_press=self.press_word_to_study_label))
        else:
            # 清除存在的三个 按钮和标签
            self.ids.main_box.clear_widgets(children=[self.ids.three_labels_box, self.ids.box_button_anchor])
            # 绑定点击任意位置执行方法
            self.ids.main_box.bind(on_touch_down=self.anywhere_touch_down)

            self.ids.word_to_study.text = rows[0][1]
            self.ids.phonetic.text = rows[0][3]

    def show_detail_word(self):
        """显示被隐藏的部分"""
        word = self.ids.word_to_study.text
        sql = "SELECT * FROM word WHERE word = '%s'" % word
        rows = select_data(sql)
        self.ids.main_box.clear_widgets(children=[self.ids.box_button_anchor, self.ids.three_labels_box])
        self.ids.main_box.add_widget(self.ids.three_labels_box)
        self.ids.main_box.add_widget(self.ids.box_button_anchor)

        from utils.common import sub_str_len
        self.ids.word_to_study.text = rows[0][1]
        self.ids.explain_word.text = sub_str_len(rows[0][2].strip(), 3)
        self.ids.phonetic.text = rows[0][3]
        self.ids.examples_en.text = rows[0][4]
        self.ids.examples_cn.text = rows[0][5]

    def insert_unknown_word(self):
        """插入一条数据"""
        word = self.ids.word_to_study.text
        sql = "INSERT INTO today (word_id) SELECT id FROM word WHERE word = '%s'" % word
        insert_data(sql)

    def delete_today_word(self):
        """删除一条数据"""
        word = self.ids.word_to_study.text
        sql = "DELETE FROM today WHERE id = (SELECT id FROM today WHERE word_id = (SELECT id FROM word WHERE word = '%s') LIMIT 1)" % word
        insert_data(sql)

    def insert_known_word(self):
        """known表添加一条数"""
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        word = self.ids.word_to_study.text
        sql = "INSERT INTO known(word_id,create_date) SELECT (SELECT id FROM word WHERE word = '%s'),'%s' WHERE NOT EXISTS(SELECT 1 FROM known WHERE word_id = (SELECT id FROM word WHERE word = '%s'))" % (word, now, word)
        print(sql)
        insert_data(sql)

    def play_word(self):
        """播放MP3文件"""
        word = self.ids.word_to_study.text
        storage_path = 'mp3/%s.mp3' % word
        if os.name == 'nt':
            self.window_play_word(storage_path)
        elif os.name == 'posix':
            self.unix_play_word(storage_path)

    @staticmethod
    def window_play_word(storage_path):
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load(storage_path)
        sound.play()

    @staticmethod
    def unix_play_word(storage_path):
        # 安装Pyjnius
        from jnius import autoclass
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        if player.isPlaying():
            player.stop()
            player.reset()
        try:
            player.setDataSource(storage_path)
            player.prepare()
            player.start()
        except:
            player.reset()

    def review_word(self, a, b):
        """复习单词"""
        # sql = "SELECT word_id FROM known WHERE id NOT IN(SELECT id FROM known WHERE (create_date > date('now','-1 day') AND add_times >= 0) OR (create_date > date('now','-3 day') AND add_times >= 1) OR (create_date > date('now','-7 day') AND add_times >= 2) OR (create_date > date('now','-14 day') AND add_times >= 3) OR (create_date > date('now','-30 day') AND add_times >= 4) OR (create_date > date('now','-60 day') AND add_times >= 5) OR (create_date > date('now','-150 day') AND add_times >= 6) OR (create_date > date('now','-365 day') AND add_times >= 7) OR (create_date > date('now','-770 day') AND add_times >= 8))"
        # res = select_data(sql)
        for word_id_tuple in self.review_res:
            word_id = word_id_tuple[0]
            # 插入数据并更新word表添加次数
            insert_sql = "INSERT INTO today(word_id) SELECT '%d' WHERE NOT EXISTS(SELECT 1 FROM today WHERE word_id = '%d')" % (word_id, word_id)
            update_sql = "UPDATE known SET add_times = add_times + 1 WHERE word_id = '%d'" % word_id
            insert_data(insert_sql)
            insert_data(update_sql)

    def refresh_button(self):
        """刷新页面"""
        # 先清空所有widgets
        self.ids.main_box.clear_widgets()
        # 添加需要的显示widgets
        # self.ids.main_box.add_widget(self.ids.personal_box)
        self.ids.main_box.add_widget(self.ids.word_phonetic_box)
        # 随机读取一个单词
        self.read_random_word()

    def anywhere_touch_down(self, instance, args):
        """单击任意位置都会执行这个方法"""
        print("info.py anywhere_touch_down is running")
        self.ids.main_box.unbind(on_touch_down=self.anywhere_touch_down)
        self.play_word()
        self.show_detail_word()

    def set_name(self):
        """为name赋值"""
        sql = 'SELECT name FROM user WHERE id=1'
        res = select_data(sql)
        self.ids.slide_name_label.text = res[0][0]

    @staticmethod
    def press_word_to_study_label(instance, args):
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'AddWord'

    @staticmethod
    def me_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Me'

    @staticmethod
    def add_word_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'AddWord'

    @staticmethod
    def review_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Review'

    @staticmethod
    def upload_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Upload'

    @staticmethod
    def help_slide_button():
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'Help'
