from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
import sqlite3
import os
from database import DatabaseManager
from ai_integration import AIAssistant

# Set window size for mobile-like development
Window.size = (360, 640)

class QuestionCard(MDCard):
    question = StringProperty('')
    answer = StringProperty('')
    show_answer = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.elevation = 5
        self.padding = 20
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.content = MDBoxLayout(orientation='vertical', spacing=10)
        self.question_label = MDLabel(
            text=self.question,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=200
        )
        self.answer_label = MDLabel(
            text=self.answer,
            halign="center",
            font_style="Body1",
            size_hint_y=None,
            height=200,
            opacity=0
        )
        
        self.content.add_widget(self.question_label)
        self.content.add_widget(self.answer_label)
        self.add_widget(self.content)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            dx = touch.dx
            if abs(dx) > 50:  # Threshold for swipe
                if dx > 0 and not self.show_answer:  # Swipe right
                    self.show_answer = True
                    anim = Animation(opacity=1, duration=0.3)
                    anim.start(self.answer_label)
                elif dx < 0 and self.show_answer:  # Swipe left
                    self.show_answer = False
                    anim = Animation(opacity=0, duration=0.3)
                    anim.start(self.answer_label)
            return True
        return super().on_touch_move(touch)

class StudyScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.ai = AIAssistant()
        self.current_question_index = 0
        self.questions = []
        self.load_questions()
    
    def load_questions(self):
        self.questions = self.db.get_all_questions()
        if self.questions:
            self.show_question()
    
    def show_question(self):
        if self.questions:
            question_data = self.questions[self.current_question_index]
            self.ids.question_card.question = question_data[1]  # question text
            self.ids.question_card.answer = question_data[2] or "No answer available"  # answer text
    
    def next_question(self):
        if self.questions:
            self.current_question_index = (self.current_question_index + 1) % len(self.questions)
            self.show_question()
    
    def previous_question(self):
        if self.questions:
            self.current_question_index = (self.current_question_index - 1) % len(self.questions)
            self.show_question()
    
    def bookmark_question(self):
        if self.questions:
            question_id = self.questions[self.current_question_index][0]
            self.db.bookmark_question(question_id)
    
    def generate_ai_answer(self):
        if self.questions:
            question = self.questions[self.current_question_index][1]
            answer = self.ai.generate_answer(question)
            if answer:
                self.ids.question_card.answer = answer
                # Update the answer in the database
                question_id = self.questions[self.current_question_index][0]
                self.db.update_answer(question_id, answer)
    
    def mark_as_understood(self):
        if self.questions:
            question_id = self.questions[self.current_question_index][0]
            self.db.mark_as_understood(question_id)
            self.next_question()

class AddQuestionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
    
    def add_question(self):
        question = self.ids.question_input.text
        answer = self.ids.answer_input.text
        subject = self.ids.subject_input.text
        
        if question and subject:
            self.db.add_question(question, answer, subject)
            self.ids.question_input.text = ''
            self.ids.answer_input.text = ''
            self.ids.subject_input.text = ''

class SmritifyApp(MDApp):
    def build(self):
        # Set theme
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Create navigation layout
        self.nav_layout = MDNavigationLayout()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Create navigation drawer
        self.nav_drawer = MDNavigationDrawer()
        self.nav_drawer_list = MDList()
        
        # Add navigation items
        study_item = OneLineListItem(
            text="Study Mode",
            on_release=lambda x: self.switch_screen('study')
        )
        add_item = OneLineListItem(
            text="Add Questions",
            on_release=lambda x: self.switch_screen('add_question')
        )
        
        self.nav_drawer_list.add_widget(study_item)
        self.nav_drawer_list.add_widget(add_item)
        self.nav_drawer.add_widget(self.nav_drawer_list)
        
        # Load KV string
        Builder.load_string("""
<StudyScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        MDTopAppBar:
            title: "Study Mode"
            left_action_items: [["menu", lambda x: app.nav_drawer.set_state("open")]]
            elevation: 10
        
        QuestionCard:
            id: question_card
        
        MDBoxLayout:
            size_hint_y: None
            height: 60
            spacing: 20
            padding: 10
            
            MDFloatingActionButton:
                icon: "arrow-left"
                on_release: root.previous_question()
            
            MDFloatingActionButton:
                icon: "bookmark"
                on_release: root.bookmark_question()
            
            MDFloatingActionButton:
                icon: "robot"
                on_release: root.generate_ai_answer()
            
            MDFloatingActionButton:
                icon: "check"
                on_release: root.mark_as_understood()
            
            MDFloatingActionButton:
                icon: "arrow-right"
                on_release: root.next_question()

<AddQuestionScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Add Questions"
            left_action_items: [["menu", lambda x: app.nav_drawer.set_state("open")]]
            elevation: 10
        
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 20
                size_hint_y: None
                height: self.minimum_height
                
                MDTextField:
                    id: question_input
                    hint_text: "Enter your question"
                    mode: "rectangle"
                    size_hint_y: None
                    height: 100
                
                MDTextField:
                    id: answer_input
                    hint_text: "Enter the answer (optional)"
                    mode: "rectangle"
                    size_hint_y: None
                    height: 100
                
                MDTextField:
                    id: subject_input
                    hint_text: "Enter subject"
                    mode: "rectangle"
                
                MDRaisedButton:
                    text: "Add Question"
                    on_release: root.add_question()
                    pos_hint: {"center_x": 0.5}
""")
        
        # Add screens
        self.screen_manager.add_widget(StudyScreen(name='study'))
        self.screen_manager.add_widget(AddQuestionScreen(name='add_question'))
        
        # Add screen manager to navigation layout
        self.nav_layout.add_widget(self.screen_manager)
        self.nav_layout.add_widget(self.nav_drawer)
        
        return self.nav_layout
    
    def switch_screen(self, screen_name):
        """Switch to the specified screen and close the navigation drawer"""
        self.screen_manager.current = screen_name
        self.nav_drawer.set_state("close")

if __name__ == '__main__':
    SmritifyApp().run() 