from quote import QuoteGen
from wallpaper import WallpaperGen
import customtkinter
from tkinter import filedialog as fd
from pathlib import Path
import pyglet
from CTkColorPicker import *
import threading
import darkdetect
import random

# Adding custom font for title:

pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file("./resources/ui_fonts/Fuggles-Regular.ttf")

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
        self.app.title("WallVerse")
        self.app.geometry("600x600")

        self.tabview = customtkinter.CTkTabview(self, width=600)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

        self.tabview.add("Home")
        self.tabview.add("Quotes")
        self.tabview.add("Style")
        self.tabview.add("Preferences")

        # Home tab

        self.home_title = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Welcome to Fortune's Window", font=TITLE_FONT)
        self.home_title.grid(row=0, column=0, columnspan=2, padx=100, pady=(30, 0), sticky="EW")

        self.home_info = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Revisit your favorite quotes, or be surprised!", font=ELEMENT_FONT)
        self.home_info.grid(row=1, column=0, columnspan=2, padx=100, pady=20, sticky="EW")

        self.auto_set_btn = customtkinter.CTkButton(
            self.tabview.tab("Home"), text="Set as Wallpaper", command=self.set_wallpaper)
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
            self.tabview.tab("Quotes"), text="Save", command=self.update_textbox)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.custom_set_btn = customtkinter.CTkButton(
            self.tabview.tab("Quotes"), text="Set as Wallpaper", command=self.set_wallpaper)
        self.custom_set_btn.grid(row=5, column=2, padx=10, pady=10, sticky="EW")

        # Style tab

        self.text_size_var = customtkinter.IntVar(value=18)

        self.text_size_edit_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text size:")

        self.text_size_edit_label.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        self.text_size_edit_options = customtkinter.CTkEntry(
            self.tabview.tab("Style"), textvariable=self.text_size_var)

        self.text_size_edit_options.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        font_path = Path("./resources/fonts")

        available_fonts = [font.name for font in font_path.iterdir()]

        self.font_style_var = customtkinter.StringVar(value=available_fonts[0])

        self.font_style_edit_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Font size:")
        self.font_style_edit_label.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.font_combobox = customtkinter.CTkComboBox(
            self.tabview.tab("Style"), values=available_fonts, variable=self.font_style_var)

        self.font_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="EW")

        # LIGHT-MODE THEME OPTIONS

        self.light_theme_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Light mode theme", font=HEADING_FONT)
        self.light_theme_label.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text color:")
        self.light_theme_text_color_label.grid(row=4, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_value = customtkinter.StringVar()

        self.light_theme_text_color_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                            text="Choose text color",
                                                                            command=self.set_light_theme_text_color)
        self.light_theme_text_color_picker_button.grid(row=4, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Background:")
        self.light_theme_background_type_label.grid(row=5, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.light_theme_background_type_options_combobox = customtkinter.CTkComboBox(self.tabview.tab("Style"),
                                                                                      values=["Solid", "Image"],
                                                                                      variable=self.light_theme_background_type_option_var)
        self.light_theme_background_type_options_combobox.grid(row=5, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var.trace('w', self.handle_light_mode_callback)
        self.handle_light_mode_callback()

        self.light_theme_background_color_value = customtkinter.StringVar()
        self.light_theme_background_image_path = customtkinter.StringVar()

    def handle_light_mode_callback(self, *args):
        if self.light_theme_background_type_option_var.get() == "Solid":

            self.light_theme_background_color_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background color:")
            self.light_theme_background_color_label.grid(row=6, column=0, padx=10, pady=10, sticky="EW")

            self.light_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.tabview.tab("Style"), text="Choose background color",
                                        command=self.set_light_theme_background_color))
            self.light_theme_background_color_picker_button.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        elif self.light_theme_background_type_option_var.get() == "Image":

            self.light_theme_background_image_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background image:")
            self.light_theme_background_image_label.grid(row=6, column=0, padx=10, pady=10, sticky="EW")
            self.light_theme_background_image_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                                      text="Choose background image",
                                                                                      command=self.set_light_theme_background_image)

            self.light_theme_background_image_picker_button.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        # DARK-MODE THEME OPTIONS

        self.dark_theme_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Dark mode theme", font=HEADING_FONT)
        self.dark_theme_label.grid(row=7, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Text color:")
        self.dark_theme_text_color_label.grid(row=8, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_value = customtkinter.StringVar()

        self.dark_theme_text_color_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                           text="Choose text color",
                                                                           command=self.set_dark_theme_text_color)
        self.dark_theme_text_color_picker_button.grid(row=8, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_label = customtkinter.CTkLabel(
            self.tabview.tab("Style"), text="Background:")
        self.dark_theme_background_type_label.grid(row=9, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.dark_theme_background_type_options_combobox = customtkinter.CTkComboBox(self.tabview.tab("Style"),
                                                                                     values=["Solid", "Image"],
                                                                                     variable=self.dark_theme_background_type_option_var)
        self.dark_theme_background_type_options_combobox.grid(row=9, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var.trace('w', self.handle_dark_mode_callback)
        self.handle_dark_mode_callback()

        self.dark_theme_background_color_value = customtkinter.StringVar()
        self.dark_theme_background_image_path = customtkinter.StringVar()

    def handle_dark_mode_callback(self, *args):
        if self.dark_theme_background_type_option_var.get() == "Solid":

            self.dark_theme_background_color_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background color:")
            self.dark_theme_background_color_label.grid(row=10, column=0, padx=10, pady=10, sticky="EW")

            self.dark_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.tabview.tab("Style"), text="Choose background color",
                                        command=self.set_dark_theme_background_color))
            self.dark_theme_background_color_picker_button.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

        elif self.dark_theme_background_type_option_var.get() == "Image":

            self.dark_theme_background_image_label = customtkinter.CTkLabel(
                self.tabview.tab("Style"), text="Background image:")
            self.dark_theme_background_image_label.grid(row=10, column=0, padx=10, pady=10, sticky="EW")
            self.dark_theme_background_image_picker_button = customtkinter.CTkButton(self.tabview.tab("Style"),
                                                                                     text="Choose background image",
                                                                                     command=self.set_dark_theme_background_image)
            self.dark_theme_background_image_picker_button.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

    def load_textbox_file(self):
        with open(file="resources/quote_packs/custom.txt", mode="r") as file:
            return file.read()

    def update_textbox(self):
        with open(file="resources/quote_packs/custom.txt", mode="w") as file:
            file.write(self.text_box.get(0.1, customtkinter.END))

    def set_wallpaper(self):
        self.quote.set_quote_pack(self.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        self.wallpaper.set_font(font=f"resources/fonts/{self.font_style_var.get()}",
                                font_size=self.text_size_var.get())
        self.wallpaper.set_screen_size(method="auto")
        self.wallpaper.set_canvas(canvas_type="solid", bg_color=self.dark_theme_background_color_value.get())
        self.wallpaper.draw_wallpaper(input_text=random_quote, text_color=self.dark_theme_text_color_value.get())
        self.wallpaper.set_wallpaper()

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

    def set_light_theme_background_image(self):
        file_path = fd.askopenfile()
        self.light_theme_background_image_path.set(file_path.name)

    def set_dark_theme_background_image(self):
        file_path = fd.askopenfile()
        self.dark_theme_background_image_path.set(file_path.name)


if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()
