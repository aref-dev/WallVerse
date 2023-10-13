from quote_manager import QuoteGen
from wallpaper import WallpaperGen
import customtkinter
import pyglet
import darkdetect
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem
from home_tab import HomeTab
from quotes_tab import QuotesTab
from style_tab import StyleTab
from preferences_tab import PreferencesTab

# Adding custom font for title:
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("ui_fonts/Fuggles-Regular.ttf")


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class UserInterface(customtkinter.CTk):
    def __init__(self, quote_obj: QuoteGen, wallpaper_obj: WallpaperGen):
        super().__init__()
        self.quote = quote_obj
        self.wallpaper = wallpaper_obj

        self.title("Fortune's Window")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

        self.icon_img = Image.open("icon.png")
        self.icon_menu = (MenuItem("Refresh", self.set_wallpaper),
                          MenuItem("Show app", self.show_app),
                          MenuItem("Exit", self.exit_app))
        self.icon = pystray.Icon("TrayIcon", self.icon_img, "Fortune's Window", menu=self.icon_menu)
        self.icon.run_detached()

        self.tabview.add("Home")
        self.tabview.add("Quotes")
        self.tabview.add("Style")
        self.tabview.add("Preferences")

        # self.t = threading.Thread(target=darkdetect.listener, args=(self.dark_mode_trace,))
        # self.t.daemon = True
        # self.t.start()

        self.protocol("WM_DELETE_WINDOW", self.iconify)

        # Validate and invalidate commands for number only fields
        # %P is for validating text if change is allowed
        # https://www.pythontutorial.net/tkinter/tkinter-validation/
        self.v_cmd = (self.register(self.only_allow_digit), "%P")

        self.home_tab = HomeTab(self)
        self.quotes_tab = QuotesTab(self)
        self.style_tab = StyleTab(self)
        self.preferences_tab = PreferencesTab(self)

    def set_wallpaper(self):
        input_text = None
        text_color = None
        self.quote.set_quote_pack(self.quotes_tab.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        if self.style_tab.cowsay_toggle_value.get() == 1:
            input_text = self.quote.pass_to_cowsay(random_quote, cowsay_character=self.style_tab.cowsay_char.get())
        elif self.style_tab.cowsay_toggle_value.get() == 0:
            input_text = random_quote

        self.wallpaper.set_font(font=f"fonts/{self.style_tab.font_style_var.get()}",
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
        self.destroy()

    def only_allow_digit(self, value):
        return value.isdigit() or value == ""


if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()
