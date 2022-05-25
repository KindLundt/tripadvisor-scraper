from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel





class TA_ScraperAPP(MDApp):
    def build(self):
        screen = MDScreen()

        # Logo
        screen.add_widget(Image(
            source="C:\Users\mkind\PycharmProjects\TA_scrapers\TA_listings\GUI\GUI_elements\copenhagen-business-school-cbs-vector-logo.png",
            pos_hint ={"center_x":0.5,"center_y":0.7}
        ))

        return screen


TA_ScraperAPP().run()
