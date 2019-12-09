from kivy.app import App
from kivy.uix.widget import Widget


class OtherWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def on_checkbox_active(checkbox, value):
            if value:
                print('The checkbox', checkbox, 'is active')
            else:
                print('The checkbox', checkbox, 'is inactive')

        # 通过id获取到CheckBox部件并绑定方法
        self.ids.demo_checkbox.bind(active=on_checkbox_active)

        def switch_callback(instance, value):
            print('the switch', instance, 'is', value)
        self.ids.demo_switch.bind(active=switch_callback)


class OtherApp(App):
    def build(self):
        return OtherWidget()


if __name__ == '__main__':
    OtherApp().run()
