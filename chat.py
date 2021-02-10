import json

import urllib3
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window,WindowBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


# Define out different screens
class StartPage(Screen):
    pass


class ChatPage(Screen):
    def __init__(self, **kwargs):
        super(ChatPage, self).__init__(**kwargs)

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        self.bind(size=self.adjust_fields)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_message()

    def on_key_up(self, instance, keyboard, keycode, text=None, modifiers=None):
        if keycode == 40:
            self.receive_message()

    def send_message(self):
        message = self.ids.new_message.text
        if message:
            self.update_chat_history(f"[color=dd2020]你[/color] > {message}")
            self.ids.new_message.text = ""

    def receive_message(self):
        message = self.ids.chat_history.text.split('>')[-1]
        qyk_msg = self.get_qingyunke_message(message)
        self.incoming_message('菲菲', qyk_msg)

    def incoming_message(self, username, message):
        self.update_chat_history(f"[color=20dd20]{username}[/color] > {message}")

    def update_chat_history(self, message):
        self.ids.chat_history.text += '\n' + message

        self.ids.scroll_layout.height = self.ids.chat_history.texture_size[1] + 15
        self.ids.chat_history.height = self.ids.chat_history.texture_size[1]
        self.ids.chat_history.text_size = (self.ids.chat_history.width * 0.98, None)

        self.ids.history.scroll_to(self.ids.scroll_to_point)

    def update_chat_history_layout(self, *args):
        self.ids.scroll_layout.height = self.ids.chat_history.texture_size[1] + 15
        self.ids.chat_history.height = self.ids.chat_history.texture_size[1]
        self.ids.chat_history.text_size = (self.ids.chat_history.width * 0.98, None)

    def get_qingyunke_message(self, msg):
        http = urllib3.PoolManager()
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(msg)
        html = http.request('Get', url)
        data = html.data.decode()
        data = json.loads(data)
        html.release_conn()
        return data['content']

    def adjust_fields(self, *args):
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.ids.history.height = new_height

        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.ids.new_message.width = new_width

        Clock.schedule_once(self.update_chat_history_layout, 0.01)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('chat.kv')


class ChatApp(App):
    def build(self):
        return kv

    def on_start(self):
        WindowBase.softinput_mode = 'below_target'
        # Start Page init
        start_button = self.root.get_screen("Start").ids.start
        animation = Animation(color=(1, 1, 1, 1), duration=1)
        animation += Animation(color=(1, 1, 1, 0), duration=1)
        animation.repeat = True
        animation.start(start_button)

        # Chat Page init
        chat_page = self.root.get_screen("Chat")
        chat_page.ids.history.height = Window.size[1] * 0.9
        chat_page.ids.new_message.width = Window.size[0] * 0.8


if __name__ == '__main__':
    ChatApp().run()
