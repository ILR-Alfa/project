from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.window import Window  # Добавьте импорт
from kivy.lang import Builder
import os
import sys

# Функция для получения правильного пути к ресурсам
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Если запускается из собранного EXE
    except Exception:
        base_path = os.path.abspath(".")  # Если запускается из исходного кода
    return os.path.join(base_path, relative_path)

# Основной макет
class TimerLayout(BoxLayout):
    main_time = NumericProperty(50 * 60)  # Основной таймер (в секундах)
    short_time = NumericProperty(10 * 60)  # Короткий таймер (в секундах)
    is_dark_mode = BooleanProperty(False)  # Темная тема
    slider_pos = NumericProperty(0)  # Позиция шарика переключения темы
    main_timer_running = BooleanProperty(False)
    short_timer_running = BooleanProperty(False)
    sun_image = StringProperty("")
    moon_image = StringProperty("")
    sun_shine_image = StringProperty("")
    moon_shine_image = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем пути к изображениям через resource_path
        self.sun_image = resource_path("assets/sun.png")
        self.moon_image = resource_path("assets/moon.png")
        self.sun_shine_image = resource_path("assets/sun_shine.png")
        self.moon_shine_image = resource_path("assets/moon_shine.png")
        sound_path = resource_path("assets/alarm.mp3")
        self.update_images()  
        self.alarm_sound = SoundLoader.load(sound_path)
        if not self.alarm_sound:
            print(f"Ошибка: файл {sound_path} не загружен")

        
    def play_sound(self):
        """ Воспроизводит звук уведомления """
        if self.alarm_sound:
            self.alarm_sound.play()
        else:
            print("Ошибка: звук не загружен")


    def update_images(self):
        """ Меняет изображения солнца/луны в зависимости от темы """
        if self.is_dark_mode:
           self.ids.sun_image.source = self.sun_image  # Обычное солнце
           self.ids.moon_image.source = self.moon_shine_image  # Светящаяся луна
        else:
           self.ids.sun_image.source = self.sun_shine_image  # Светящееся солнце
           self.ids.moon_image.source = self.moon_image  # Обычная луна

    def toggle_theme(self):
        """ Переключение темы """
        self.is_dark_mode = not self.is_dark_mode
        target_pos = 1 if self.is_dark_mode else 0
        anim = Animation(slider_pos=target_pos, duration=0.3)  # Плавная анимация
        self.update_images()
        anim.start(self)

    def on_touch_down(self, touch):
        """ Обработка нажатий для переключения темы """
        if hasattr(self, 'ids') and 'theme_switch' in self.ids:
            if self.ids.theme_switch.collide_point(*touch.pos):
                self.toggle_theme()
        return super().on_touch_down(touch)

    def start_timers(self):
        """ Запуск таймеров """
        if not self.main_timer_running and not self.short_timer_running:
            Clock.schedule_interval(self.update_main_timer_clock, 1)
            self.main_timer_running = True

    def pause_timers(self):
        """ Приостановка таймеров """
        if self.main_timer_running:
            Clock.unschedule(self.update_main_timer_clock)
            self.main_timer_running = False
        if self.short_timer_running:
            Clock.unschedule(self.update_short_timer_clock)
            self.short_timer_running = False

    def update_main_timer_clock(self, dt):
        """ Обновление основного таймера """
        if self.main_time > 0:
            self.main_time -= 1
        else:
            self.main_timer_running = False
            Clock.unschedule(self.update_main_timer_clock)
            self.start_short_timer()
            self.play_sound() 

    def start_short_timer(self):
        """ Запуск короткого таймера после завершения основного """
        if not self.short_timer_running:
            Clock.schedule_interval(self.update_short_timer_clock, 1)
            self.short_timer_running = True

    def update_short_timer_clock(self, dt):
        """ Обновление короткого таймера """
        if self.short_time > 0:
            self.short_time -= 1
        else:
            self.short_timer_running = False
            Clock.unschedule(self.update_short_timer_clock)
            self.play_sound()  

    def format_time(self, seconds):
        """ Форматирует время в MM:SS """
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def parse_time_input(self, time_str):
        """ Парсит время из строки в формате MM:SS """
        try:
            minutes, seconds = map(int, time_str.split(':'))
            if 0 <= minutes <= 99 and 0 <= seconds <= 59:
                return minutes * 60 + seconds
            else:
                print("Ошибка: недопустимое значение времени")
                return None
        except ValueError:
            print("Ошибка: введите время в формате MM:SS")
            return None

    def update_main_timer(self, time_str):
        """ Обновляет основной таймер из строки """
        new_time = self.parse_time_input(time_str)
        if new_time is not None:
            self.main_time = new_time
        self.ids.main_time_input.text = self.format_time(self.main_time)

    def update_short_timer(self, time_str):
        """ Обновляет короткий таймер из строки """
        new_time = self.parse_time_input(time_str)
        if new_time is not None:
            self.short_time = new_time
        self.ids.short_time_input.text = self.format_time(self.short_time)

    def animate_button(self, button):
        """ Анимация кнопки """
        if not hasattr(button, 'scale_factor'):
            button.scale_factor = 1
        anim = Animation(scale_factor=0.9, duration=0.1) + \
               Animation(scale_factor=1, duration=0.1)
        anim.start(button)


class TimerApp(App):
    def build(self):
        self.icon = resource_path("assets/icon.ico")

        Window.minimum_width = 700
        Window.minimum_height = 500

        return TimerLayout()


if __name__ == "__main__":
    TimerApp().run()