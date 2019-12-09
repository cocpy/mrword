from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager

# 引入页面
from pages.indexpage.index import IndexPage
from pages.uploadpage.upload import UploadPage
from pages.addwordpage.addword import AddWordPage
from pages.infopage.info import InfoPage
from pages.mepage.me import MePage
from pages.reviewpage.review import ReviewPage
from pages.helppage.help import HelpPage


class MyApp(App):
    def build(self):
        # 加载kv文件
        self.load_kv("pages/indexpage/index.kv")
        self.load_kv("pages/uploadpage/upload.kv")
        self.load_kv("pages/addwordpage/addword.kv")
        self.load_kv("pages/infopage/info.kv")
        self.load_kv("pages/mepage/me.kv")
        self.load_kv('pages/helppage/help.kv')
        self.screen_manager = ScreenManager()
        pages = {'Index': IndexPage(), 'Upload': UploadPage(), 'AddWord': AddWordPage(), 'Info': InfoPage(),
                 'Me': MePage(), 'Review': ReviewPage(), 'Help': HelpPage()}
        for item, page in pages.items():
            self.default_page = page
            screen = Screen(name=item)
            # 添加页面
            screen.add_widget(self.default_page)
            # 向屏幕管理器添加页面
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    recite_app = MyApp()
    # 设置标题
    recite_app.title = '51斩百词'
    recite_app.run()
