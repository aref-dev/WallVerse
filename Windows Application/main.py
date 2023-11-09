from quote_manager import QuoteGen
from wallpaper import WallpaperGen
import customtkinter
import darkdetect
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem
from home_tab import HomeTab
from quotes_tab import QuotesTab
from style_tab import StyleTab
from preferences_tab import PreferencesTab
from settings_manager import SettingsManager
import os, sys, platform
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class UserInterface(customtkinter.CTk):
    def __init__(self, quote_obj: QuoteGen, wallpaper_obj: WallpaperGen):
        super().__init__()
        self.quote = quote_obj
        self.wallpaper = wallpaper_obj
        self.settings = SettingsManager()

        self.title("WallVerse")
        if platform.system() == "Windows":
            self.iconbitmap(resource_path(os.path.join("ui_resources", "icon.ico")))
        elif platform.system() == "Darwin":
            pass
        elif platform.system() == "Linux":
            pass

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

        self.icon_img = Image.open(resource_path(os.path.join("ui_resources", "icon.ico")))

        if platform.system() == "Windows":
            self.icon_menu = (MenuItem("Refresh", self.set_wallpaper),
                              MenuItem("Show app", self.show_app),
                              MenuItem("Exit", self.exit_app))
        elif platform.system() == "Darwin":
            self.icon_menu = (MenuItem("Refresh", self.set_wallpaper, visible=False),
                              MenuItem("Show app", self.show_app, visible=False),
                              MenuItem("Exit", self.exit_app))
        elif platform.system() == "Linux":
            pass

        self.icon = pystray.Icon("WallVerse", self.icon_img, menu=self.icon_menu)
        self.icon.run_detached()

        self.tabview.add("Home")
        self.tabview.add("Quotes")
        self.tabview.add("Style")
        self.tabview.add("Preferences")

        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.resizable(height=False, width=False)
        self.geometry("600x650")
        self.tabview.grid(sticky="n")
        self.grid_propagate(False)

        # Validate and invalidate commands for number only fields
        # %P is for validating text if change is allowed
        # https://www.pythontutorial.net/tkinter/tkinter-validation/
        self.v_cmd = (self.register(self.only_allow_digit), "%P")

        self.home_tab = HomeTab(self)
        self.quotes_tab = QuotesTab(self)
        self.style_tab = StyleTab(self)
        self.preferences_tab = PreferencesTab(self)

        self.current_theme = darkdetect.theme()
        self.check_dark_mode()

        if self.settings.get_value("set_as_wallpaper?") == 1:
            self.set_wallpaper()
        if self.settings.get_value("start_with_os?") == 1:
            self.withdraw()

    def set_wallpaper(self):
        input_text = None
        text_color = None
        self.quote.set_quote_pack(self.quotes_tab.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        if self.style_tab.cowsay_toggle_value.get() == 1:
            input_text = self.quote.pass_to_cowsay(random_quote, cowsay_character=self.style_tab.cowsay_char.get())
        elif self.style_tab.cowsay_toggle_value.get() == 0:
            input_text = random_quote

        if self.settings.get_value("text_size") == "":
            self.settings.set_value("text_size", 20)
            self.style_tab.text_size_var.set("20")
        if self.settings.get_value("refresh_int") == "":
            self.settings.set_value("refresh_int", 30)
            self.preferences_tab.interval_period.set("30")
            self.preferences_tab.interval_by_string.set("minutes")

        try:
            self.wallpaper.set_font(font=self.style_tab.font_preview_window.font_style_path.get(),
                                    font_size=int(self.style_tab.text_size_var.get()))
        except AttributeError:
            self.wallpaper.set_font(font=resource_path(self.settings.get_value("font_path")),
                                    font_size=int(self.style_tab.text_size_var.get()))
        self.wallpaper.set_screen_size(method="auto")

        if darkdetect.isLight():
            bg_color = self.style_tab.light_theme_background_color_value.get()
            text_color = self.style_tab.light_theme_text_color_value.get()
            img_path = self.style_tab.light_theme_background_image_path.get()
            if self.style_tab.light_theme_background_type_option_var.get() == "Solid":
                self.wallpaper.set_canvas(canvas_type="solid", bg_color=bg_color)
            elif self.style_tab.light_theme_background_type_option_var.get() == "Image":
                self.wallpaper.set_canvas(canvas_type="image", path=img_path)
        elif darkdetect.isDark():
            bg_color = self.style_tab.dark_theme_background_color_value.get()
            text_color = self.style_tab.dark_theme_text_color_value.get()
            img_path = self.style_tab.dark_theme_background_image_path.get()
            if self.style_tab.dark_theme_background_type_option_var.get() == "Solid":
                self.wallpaper.set_canvas(canvas_type="solid", bg_color=bg_color)
            elif self.style_tab.dark_theme_background_type_option_var.get() == "Image":
                self.wallpaper.set_canvas(canvas_type="image", path=img_path)

        self.wallpaper.draw_wallpaper(input_text=input_text, text_color=text_color)
        self.wallpaper.set_wallpaper()
        self.preferences_tab.handle_interval_callback()

    def create_image(self, width, height, color1, color2):
        # Generate an image and draw a pattern
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=color2)
        dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=color2)

    def show_app(self):
        self.deiconify()

    def exit_app(self):
        self.icon.stop()
        self.quit()
        self.destroy()

    def only_allow_digit(self, value):
        if value == "0":
            return False
        else:
            return value.isdigit() or value == ""

    def check_dark_mode(self):
        if darkdetect.theme() != self.current_theme:
            self.style_tab.dark_mode_trace()
            self.current_theme = darkdetect.theme()
        self.after(2000, self.check_dark_mode)


if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()
