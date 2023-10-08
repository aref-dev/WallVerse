import cowsay
from quote import QuoteGen
from wallpaper import WallpaperGen
import customtkinter
from tkinter import filedialog as fd
from pathlib import Path
import pyglet
from CTkColorPicker import *
import threading
import darkdetect
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem


# Adding custom font for title:
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("ui_fonts/Fuggles-Regular.ttf")

# Defining fonts:
TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class UserInterface(customtkinter.CTk):
    def __init__(self, quote_obj: QuoteGen, wallpaper_obj: WallpaperGen):
        super().__init__()
        self.quote = quote_obj
        self.wallpaper = wallpaper_obj

        self.app = customtkinter.CTk()
        self.app.title("Fortune's Window")
        self.app.geometry("600x800")

        self.tabview = customtkinter.CTkTabview(self, width=600)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

        self.icon_img = Image.open("icon.png")
        self.icon_menu = (MenuItem("Refresh", self.set_wallpaper), MenuItem("Exit", self.destroy))
        self.icon = pystray.Icon("TrayIcon", self.icon_img, "Fortune's Window", menu=self.icon_menu)
        self.icon.run_detached()

        self.tabview.add("Home")
        self.tabview.add("Quotes")
        self.tabview.add("Style")
        self.tabview.add("Preferences")

        self.t = threading.Thread(target=darkdetect.listener, args=(self.dark_mode_trace,))
        self.t.daemon = True
        self.t.start()

        # Home tab
        self.home_title = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Welcome to Fortune's Window", font=TITLE_FONT)
        self.home_title.grid(row=0, column=0, columnspan=2, padx=100, pady=(30, 0), sticky="EW")

        self.home_info = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Revisit your favorite quotes, or be surprised!", font=ELEMENT_FONT)
        self.home_info.grid(row=1, column=0, columnspan=2, padx=100, pady=20, sticky="EW")

        self.auto_set_btn = customtkinter.CTkButton(
            self.tabview.tab("Home"), text="Set as Wallpaper", command=self.set_wallpaper, fg_color="purple",font=ELEMENT_FONT)
        self.auto_set_btn.grid(row=3, column=0, columnspan=2, padx=100, pady=10, sticky="EW")

        # Quotes Tab
        self.quote_radio_value = customtkinter.StringVar(value="fortune")

        self.fortune_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="The original fortune from OpenBSD", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="fortune")
        self.fortune_radio.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.franklin_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Quotes form Poor Richard's Almanack by Benjamin Franklin",
            font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="franklin")
        self.franklin_radio.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.custom_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Your own collection (one quote on each line):", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="custom")
        self.custom_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkTextbox(
            self.tabview.tab("Quotes"), height=100)
        self.text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

        self.text_box.insert(index=0.1, text=self.load_textbox_file())

        self.text_box_save_btn = customtkinter.CTkButton(
            self.tabview.tab("Quotes"), text="Save", command=self.update_textbox,font=ELEMENT_FONT)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.refresh_wallpaper_btn1 = customtkinter.CTkButton(
            self.tabview.tab("Quotes"), text="Refresh wallpaper!", command=self.set_wallpaper, fg_color="purple",font=ELEMENT_FONT)
        self.refresh_wallpaper_btn1.grid(row=5, column=2, padx=10, pady=10, sticky="EW")

        # Style tab
        self.font_setting_label = customtkinter.CTkLabel(self.tabview.tab("Style"), text="Font setting",
                                                           font=HEADING_FONT)
        self.font_setting_label.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        self.text_size_var = customtkinter.IntVar(value=18)

        self.text_size_edit_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text size:",font=ELEMENT_FONT)

        self.text_size_edit_label.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.text_size_edit_options = customtkinter.CTkEntry(
            self.tabview.tab("Style"), textvariable=self.text_size_var)

        self.text_size_edit_options.grid(row=2, column=1, padx=10, pady=10, sticky="EW")

        font_path = Path("fonts")

        available_fonts = [font.name for font in font_path.iterdir()]

        self.font_style_var = customtkinter.StringVar(value=available_fonts[0])

        self.font_style_edit_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Font type:",font=ELEMENT_FONT)
        self.font_style_edit_label.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

        self.font_combobox = customtkinter.CTkComboBox(
            self.tabview.tab("Style"), values=available_fonts, variable=self.font_style_var)

        self.font_combobox.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="EW")

        # LIGHT-MODE THEME OPTIONS
        self.light_theme_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Light mode theme settings", font=HEADING_FONT)
        self.light_theme_label.grid(row=4, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text color:",font=ELEMENT_FONT)
        self.light_theme_text_color_label.grid(row=5, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_value = customtkinter.StringVar(value="#000000")

        self.light_theme_text_color_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                            text="Choose text color",
                                                                            command=self.set_light_theme_text_color,
                                                                            font=ELEMENT_FONT)
        self.light_theme_text_color_picker_button.grid(row=5, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Background:")
        self.light_theme_background_type_label.grid(row=6, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.light_theme_background_type_options_combobox = customtkinter.CTkComboBox(self.tabview.tab("Style"),
                                                                                      values=["Solid", "Image"],
                                                                                      variable=self.light_theme_background_type_option_var,
                                                                                      font=ELEMENT_FONT)
        self.light_theme_background_type_options_combobox.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var.trace('w', self.handle_light_mode_callback)
        self.handle_light_mode_callback()

        self.light_theme_background_color_value = customtkinter.StringVar(value="#ffffff")
        self.light_theme_background_image_path = customtkinter.StringVar()

        # DARK-MODE THEME OPTIONS
        self.dark_theme_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Dark mode theme settings", font=HEADING_FONT)
        self.dark_theme_label.grid(row=8, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text color:",font=ELEMENT_FONT)
        self.dark_theme_text_color_label.grid(row=9, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_value = customtkinter.StringVar(value="#ffffff")

        self.dark_theme_text_color_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                           text="Choose text color",
                                                                           command=self.set_dark_theme_text_color,
                                                                           font=ELEMENT_FONT)
        self.dark_theme_text_color_picker_button.grid(row=9, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Background:",font=ELEMENT_FONT)
        self.dark_theme_background_type_label.grid(row=10, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.dark_theme_background_type_options_combobox = customtkinter.CTkComboBox(self.tabview.tab("Style"),
                                                                                     values=["Solid", "Image"],
                                                                                     variable=self.dark_theme_background_type_option_var,
                                                                                     font=ELEMENT_FONT)
        self.dark_theme_background_type_options_combobox.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var.trace('w', self.handle_dark_mode_callback)
        self.handle_dark_mode_callback()

        self.dark_theme_background_color_value = customtkinter.StringVar(value="#000000")
        self.dark_theme_background_image_path = customtkinter.StringVar()

        # COWSAY
        self.cowsay_toggle_value = customtkinter.IntVar(value=1)
        self.cowsay_char = customtkinter.StringVar(value="tux")

        self.cowsay_setting_label = customtkinter.CTkLabel(self.tabview.tab("Style"), text="Cowsay setting", font=HEADING_FONT)
        self.cowsay_setting_label.grid(row=12, column=1, padx=10, pady=10, sticky="EW")

        self.cowsay_toggle_checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Style"), offvalue=0, onvalue=1,
                                                                text= "Cowsay",
                                                                variable=self.cowsay_toggle_value,
                                                                font=ELEMENT_FONT)

        self.cowsay_toggle_checkbox.grid(row=13, column=0, padx=50, pady=10, sticky="EW")

        self.cowsay_toggle_label = customtkinter.CTkLabel(self.tabview.tab("Style"), text="Pick cowsay character:",font=ELEMENT_FONT)
        self.cowsay_toggle_label.grid(row=14, column=0, padx=50, pady=10, sticky="EW")

        self.cowsay_char_combobox = customtkinter.CTkComboBox(self.tabview.tab("Style"), values=cowsay.main.CHARS,
                                                              variable=self.cowsay_char,font=ELEMENT_FONT)

        self.cowsay_char_combobox.grid(row=14, column=1, padx=10, pady=10, sticky="EW")

        self.refresh_wallpaper_btn2 = customtkinter.CTkButton(
            self.tabview.tab("Style"), text="Refresh wallpaper!", command=self.set_wallpaper, fg_color="purple",font=ELEMENT_FONT)
        self.refresh_wallpaper_btn2.grid(row=15, column=1, padx=10, pady=10, sticky="EW")

        # Preferences Tab
        self.interval_period = customtkinter.IntVar(value=1)
        self.interval_by_string = customtkinter.StringVar(value="Hour")

        self.refresh_interval_label = customtkinter.CTkLabel(
            self.tabview.tab("Preferences"), text="Refresh every:", font=ELEMENT_FONT)
        self.refresh_interval_label.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.interval_entry = customtkinter.CTkEntry(
            self.tabview.tab("Preferences"), font=ELEMENT_FONT, textvariable=self.interval_period)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)

        self.interval_hour = customtkinter.CTkRadioButton(
            self.tabview.tab("Preferences"), text="Hour", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="Hour")
        self.interval_hour.grid(row=0, column=2, padx=(20,0), pady=10, sticky="EW")

        self.interval_minute = customtkinter.CTkRadioButton(
            self.tabview.tab("Preferences"), text="Minutes", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="Minutes")
        self.interval_minute.grid(row=0, column=3, padx=(0,10), pady=10, sticky="EW")

        self.interval_by_string.trace('w', self.handle_interval_callback)

    def handle_light_mode_callback(self, *args):
        if self.light_theme_background_type_option_var.get() == "Solid":

            self.light_theme_background_color_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background color:",font=ELEMENT_FONT)
            self.light_theme_background_color_label.grid(row=7, column=0, padx=10, pady=10, sticky="EW")

            self.light_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.tabview.tab("Style"), text="Choose background color",
                                        command=self.set_light_theme_background_color,font=ELEMENT_FONT))
            self.light_theme_background_color_picker_button.grid(row=7, column=1, padx=10, pady=10, sticky="EW")

        elif self.light_theme_background_type_option_var.get() == "Image":

            self.light_theme_background_image_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background image:",font=ELEMENT_FONT)
            self.light_theme_background_image_label.grid(row=7, column=0, padx=10, pady=10, sticky="EW")
            self.light_theme_background_image_picker_button = (
                customtkinter.CTkButton(self.tabview.tab("Style"), text="Choose background image",font=ELEMENT_FONT,
                                        command=self.set_light_theme_background_image))

            self.light_theme_background_image_picker_button.grid(row=7, column=1, padx=10, pady=10, sticky="EW")

    def handle_dark_mode_callback(self, *args):
        if self.dark_theme_background_type_option_var.get() == "Solid":

            self.dark_theme_background_color_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background color:",font=ELEMENT_FONT)
            self.dark_theme_background_color_label.grid(row=11, column=0, padx=10, pady=10, sticky="EW")

            self.dark_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.tabview.tab("Style"), text="Choose background color",
                                        command=self.set_dark_theme_background_color,font=ELEMENT_FONT))
            self.dark_theme_background_color_picker_button.grid(row=11, column=1, padx=10, pady=10, sticky="EW")

        elif self.dark_theme_background_type_option_var.get() == "Image":

            self.dark_theme_background_image_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background image:",font=ELEMENT_FONT)
            self.dark_theme_background_image_label.grid(row=11, column=0, padx=10, pady=10, sticky="EW")
            self.dark_theme_background_image_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                                     text="Choose background image",
                                                                                     command=self.set_dark_theme_background_image,
                                                                                     font=ELEMENT_FONT)
            self.dark_theme_background_image_picker_button.grid(row=11, column=1, padx=10, pady=10, sticky="EW")

    def load_textbox_file(self):
        with open(file="quote_packs/custom.txt", mode="r") as file:
            return file.read()

    def update_textbox(self):
        with open(file="quote_packs/custom.txt", mode="w") as file:
            file.write(self.text_box.get(0.1, customtkinter.END))

    def set_wallpaper(self):
        self.quote.set_quote_pack(self.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        if self.cowsay_toggle_value.get() == 1:
            input_text = self.quote.pass_to_cowsay(random_quote, cowsay_character=self.cowsay_char.get())
        elif self.cowsay_toggle_value.get() == 0:
            input_text = random_quote

        self.wallpaper.set_font(font=f"fonts/{self.font_style_var.get()}",
                                font_size=self.text_size_var.get())
        self.wallpaper.set_screen_size(method="auto")

        if darkdetect.isLight():
            bg_color = self.light_theme_background_color_value.get()
            text_color = self.light_theme_text_color_value.get()
            img_path = self.light_theme_background_image_path.get()
            if self.light_theme_background_type_option_var.get() == "Solid":
                self.wallpaper.set_canvas(canvas_type="solid", bg_color=bg_color)
            elif self.light_theme_background_type_option_var.get() == "Image":
                self.wallpaper.set_canvas(canvas_type="image", path=img_path)
        elif darkdetect.isDark():
            bg_color = self.dark_theme_background_color_value.get()
            text_color = self.dark_theme_text_color_value.get()
            img_path = self.dark_theme_background_image_path.get()
            if self.dark_theme_background_type_option_var.get() == "Solid":
                self.wallpaper.set_canvas(canvas_type="solid", bg_color=bg_color)
            elif self.dark_theme_background_type_option_var.get() == "Image":
                self.wallpaper.set_canvas(canvas_type="image", path=img_path)

        self.wallpaper.draw_wallpaper(input_text=input_text, text_color=text_color)
        self.wallpaper.set_wallpaper()
        self.handle_interval_callback()

    def set_light_theme_text_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        self.light_theme_text_color_value.set(color)

    def set_light_theme_background_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        self.light_theme_background_color_value.set(color)

    def set_dark_theme_text_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        self.dark_theme_text_color_value.set(color)

    def set_dark_theme_background_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        self.dark_theme_background_color_value.set(color)
        print(self.dark_theme_background_color_value.get())

    def set_light_theme_background_image(self):
        file_path = fd.askopenfile()
        self.light_theme_background_image_path.set(file_path.name)

    def set_dark_theme_background_image(self):
        file_path = fd.askopenfile()
        self.dark_theme_background_image_path.set(file_path.name)

    def dark_mode_trace(self, callback):
        self.set_wallpaper()

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

    def handle_interval_callback(self, *args):
        if self.interval_by_string.get() == "Hour":
            time = self.interval_period.get() * 3600000
        elif self.interval_by_string.get() == "Minutes":
            time = self.interval_period.get() * 60000

        self.after(time, self.set_wallpaper)



if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.handle_interval_callback()
    app.mainloop()

