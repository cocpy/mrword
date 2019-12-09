# kivy不会自动安装这个包，下载https://github.com/kivy-garden/garden.matplotlib
# 并手动添加到 Lib\site-packages\kivy\garden\matplotlib
# 或者执行gaiden install matplotlib 命令
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App

# pip install matplotlib==2.2.2
import matplotlib.pyplot as plt
# pip install numpy
import numpy as np

from utils.common import get_day_list
from db.sqlite3_connect import select_data
from custom_gestures import gesture_box as gesture


def draw_map():

    # 如果存在上一个窗口，则关闭
    plt.close()

    num_sql = "SELECT is_month FROM user WHERE id=1"
    num_res = select_data(num_sql)[0][0]
    if num_res == 'Week':
        num = 7
        title = 'Week Data'
    else:
        num = 30
        title = 'Month Data'
    num_add = num + 1
    res_date = get_day_list(num)
    x = np.arange(num_add)  # 即array([0,1,2...N])

    sql = "SELECT create_date,COUNT(id) FROM known WHERE create_date>"+res_date[0]+" GROUP BY create_date ORDER BY create_date"
    res = select_data(sql)
    date, count, date_data, count_data = [], [], [], []

    for i in res:
        date.append(i[0])
        count.append(i[1])
    for s in res_date:
        if s in date:
            index = date.index(s)
            count_data.append(count[index])
        else:
            count_data.append(0)

        if s[-2:].endswith(('0', '5', '01')):
            date_data.append(s[-2:])
        else:
            date_data.append('')

    # 随机生成几种颜色，reshape第二个参数-1指随着N变化，第一维度填满有剩就来填第二维
    # 生成的是随机的N组三通道(r,g,b)的颜色
    colors = np.random.rand(num_add * 3).reshape(num_add, -1)

    plt.title(title)  # 设置窗格标题
    plt.bar(x, count_data, alpha=0.8, color=colors, tick_label=date_data)
    # 显示上方数字
    for x, y in zip(x, count_data):
        if y == 0:
            y_num = ''
        else:
            y_num = y
        plt.text(x, y + 0.05, y_num, ha='center', va='bottom')


class ReviewPage(gesture.GestureBox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        draw_map()
        self.orientation = 'vertical'
        self.bind(on_top_to_bottom_line=self.top_to_bottom)
        self.bind(on_left_to_right_line=self.left_to_right)
        self.bind(on_right_to_left_line=self.right_to_left)
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def top_to_bottom(self, touch):
        self.clear_widgets()
        self.__init__()

    @staticmethod
    def left_to_right(touch):
        App.get_running_app().screen_manager.transition.direction = 'right'
        App.get_running_app().screen_manager.current = 'Info'

    @staticmethod
    def right_to_left(touch):
        App.get_running_app().screen_manager.transition.direction = 'left'
        App.get_running_app().screen_manager.current = 'AddWord'


class ReviewApp(App):
    def build(self):
        return ReviewPage()


if __name__ == "__main__":
    ReviewApp().run()
