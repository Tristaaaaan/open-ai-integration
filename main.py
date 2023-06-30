from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
import openai
import threading
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def generate_text(self):
        if not self.ids.api_key_ai.text:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")
        else:
            openai.api_key = self.ids.api_key_ai.text
            threading.Thread(target=self.trigger_question).start()

    def trigger_question(self):

        question = self.ids.heard_speech.text
        # Send the user's question to ChatGPT
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt="give the following question in the style of a quiz answer using as few words as possible " + question,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_text = response.choices[0].text.strip()

        self.ids.open_ai_content.text = generated_text

    def clear(self):
        self.ids.open_ai_content.text = 'Open AI Content'
        self.ids.heard_speech.text = 'Inquiry'

    def error_dialog(self, message):

        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text=message,
            buttons=[close_button],
            auto_dismiss=False
        )
        self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        self.dialog.dismiss()


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):
        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
