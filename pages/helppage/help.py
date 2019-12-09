from kivy.app import App
from custom_gestures.gesture_box import GestureBox


class HelpPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.help_box_label_note.text = '''
首页：
1、认识：单词的发音、拼写和解释你可以迅速回忆起来。
2、模糊：发音有小许错误，或拼写错了几个字母，
或解释好像知道但又不能清楚的说出口。
3、不认识：单词的发音、拼写和解释完全没印象。
4、下拉刷新页面。

个人设置：
1、点击头像可更换新头像。
2、每日学习单词量：设置每日学习单词量（不包括每
日需要复习的单词）。
3、更改背景：自定义页面背景。
4、上传文件：导入单词本。
5、Month：当前为月数据显示，点击更换为周数据显示。
6、重置：清除所有数据，恢复默认设置，请谨慎操作。
做出任何修改时请一定要单击"‘保存"保存修改。

学习记录：
1、纵坐标代表着单词数，横坐标代表日期。
2、下拉刷新数据。

导入单词：
1、点击"上传文件"后选择包含单词的文件，会自动从互
联网获取单词数据，请保持应用在后台运行。
2、在获取过程中，请保持网络畅通。

添加单词：
1、点击单词或其对应的ID，即可添加单词到今日学习计划中，
添加完单词后在首页下拉刷新页面。
2、随即添加：随机添加（计划数量-已学习数
量）个单词。
3、刷新：刷新页面。

        '''

    @staticmethod
    def help_to_info():
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = "Info"


class HelpApp(App):
    def build(self):
        return HelpPage()


if __name__ == "__main__":
    HelpApp().run()
