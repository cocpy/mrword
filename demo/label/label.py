from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class LabelWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 设置引用时markup属性必须设置为True
        label_color = Label(text='[color=ff3333]Hello[/color][color=3333ff] Label[/color]', markup=True, pos=[200, 380])
        # 添加label到根控件中
        self.add_widget(label_color)

        # 将“Label”文本标记，单击“Label”文本时会触发绑定的事件，单击“Hello”文本则不会
        label_ref = Label(text='Hello[ref=label] Label[/ref]', markup=True, pos=[400, 120])

        def print_it(instance, value):
            # 传递过来的value值=ref设置的值
            print('User clicked on', value)
        # 绑定触发事件，回调方法
        label_ref.bind(on_ref_press=print_it)
        self.add_widget(label_ref)


class LabelApp(App):
    def build(self):
        return LabelWidget()


LabelApp().run()
