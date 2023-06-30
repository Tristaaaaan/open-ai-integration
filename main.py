from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
import openai
import threading


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def generate_text(self):

        openai.api_key = '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'
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


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):
        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
