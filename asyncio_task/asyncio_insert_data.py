import asyncio
import threading
import logging
from kivy.event import EventDispatcher


class EventLoopWorker(EventDispatcher):

    # 定义唯一事件
    __events__ = ('on_pulse',)

    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        # 指定目标
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.daemon = True
        self.loop = None
        self._pulse = None
        self._pulse_task = None
        self.src = file_path

    def _run_loop(self):
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._restart_pulse()
        self.loop.run_forever()

    def start(self):
        self._thread.start()

    async def pulse(self):
        """处理具体业务逻辑"""
        from importfile.import_much import import_file
        logging.info("Upload is ready,filepath is %s" % self.src)
        import_file(self.src)
        logging.info("Upload shutdown")
        self.__init__(self.src)

    def _restart_pulse(self):
        """启动或重置任务"""
        if self._pulse_task is not None:
            self._pulse_task.cancel()
        self._pulse_task = self.loop.create_task(self.pulse())

    def on_pulse(self, *_):
        """EventDispatcher事件必须添加的方法"""
        pass
