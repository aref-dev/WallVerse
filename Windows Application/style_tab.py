import os
import sys
from tkinter import filedialog as fd
import cowsay
import customtkinter
from CTkColorPicker import *
from font_preview_window import FontPreview


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)


class StyleTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.settings = master.settings
        self.font_preview_window = None

        self.style_tab = customtkinter.CTkScrollableFrame(master.tabview.tab("Style"), width=500, height=450)
        self.style_tab.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.font_setting_label = customtkinter.CTkLabel(self.style_tab, text="Font setting",
                                                         font=HEADING_FONT)
        self.font_setting_label.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        self.text_size_var = customtkinter.StringVar(value=self.settings.get_value("text_size"))

        self.text_size_edit_label = customtkinter.CTkLabel(
            self.style_tab, text="Text size:", font=ELEMENT_FONT)

        self.text_size_edit_label.grid(row=2, column=0, pady=10, sticky="EW")

        self.text_size_entry = customtkinter.CTkEntry(self.style_tab, textvariable=self.text_size_var)
        self.text_size_entry.configure(validate="key", validatecommand=master.v_cmd)
        self.text_size_entry.grid(row=2, column=1, padx=10, pady=10, sticky="EW")
        self.text_size_var.trace("w", callback=self.text_size_warning)

        self.font_style_edit_label = customtkinter.CTkLabel(
            self.style_tab, text="Font type:", font=ELEMENT_FONT)
        self.font_style_edit_label.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

        self.font_preview_btn = customtkinter.CTkButton(self.style_tab, text="Choose Font",
                                                        command=self.open_font_preview, font=ELEMENT_FONT)
        self.font_preview_btn.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="EW")

        # LIGHT-MODE THEME OPTIONS
        self.light_theme_label = customtkinter.CTkLabel(
            self.style_tab, text="Light mode theme settings", font=HEADING_FONT)
        self.light_theme_label.grid(row=4, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_label = customtkinter.CTkLabel(
            self.style_tab, text="Text color:", font=ELEMENT_FONT)
        self.light_theme_text_color_label.grid(row=5, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_value = customtkinter.StringVar(
            value=self.settings.get_value("light_mode_text_color"))

        self.light_theme_text_color_picker_button = customtkinter.CTkButton(self.style_tab,
                                                                            text="Choose text color",
                                                                            command=self.set_light_theme_text_color,
                                                                            font=ELEMENT_FONT)
        self.light_theme_text_color_picker_button.grid(row=5, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_label = customtkinter.CTkLabel(
            self.style_tab, text="Background:")
        self.light_theme_background_type_label.grid(row=6, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var = customtkinter.StringVar(
            value=self.settings.get_value("light_mode_bg_mode"))

        self.light_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.light_theme_background_type_option_var, font=ELEMENT_FONT))
        self.light_theme_background_type_options_combobox.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var.trace('w', self.handle_light_mode_callback)
        self.handle_light_mode_callback()

        self.light_theme_background_color_value = customtkinter.StringVar(
            value=self.settings.get_value("light_mode_bg_color"))
        self.light_theme_background_image_path = customtkinter.StringVar(
            value=resource_path(self.settings.get_value("light_mode_image_path")))

        # DARK-MODE THEME OPTIONS
        self.dark_theme_label = customtkinter.CTkLabel(
            self.style_tab, text="Dark mode theme settings", font=HEADING_FONT)
        self.dark_theme_label.grid(row=8, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_label = customtkinter.CTkLabel(
            self.style_tab, text="Text color:", font=ELEMENT_FONT)
        self.dark_theme_text_color_label.grid(row=9, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_value = customtkinter.StringVar(
            value=self.settings.get_value("dark_mode_text_color"))

        self.dark_theme_text_color_picker_button = customtkinter.CTkButton(self.style_tab,
                                                                           text="Choose text color",
                                                                           command=self.set_dark_theme_text_color,
                                                                           font=ELEMENT_FONT)
        self.dark_theme_text_color_picker_button.grid(row=9, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_label = customtkinter.CTkLabel(
            self.style_tab, text="Background:", font=ELEMENT_FONT)
        self.dark_theme_background_type_label.grid(row=10, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var = customtkinter.StringVar(
            value=self.settings.get_value("dark_mode_bg_mode"))

        self.dark_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.dark_theme_background_type_option_var, font=ELEMENT_FONT))
        self.dark_theme_background_type_options_combobox.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var.trace('w', self.handle_dark_mode_callback)
        self.handle_dark_mode_callback()

        self.dark_theme_background_color_value = customtkinter.StringVar(
            value=self.settings.get_value("dark_mode_bg_color"))
        self.dark_theme_background_image_path = customtkinter.StringVar(
            value=resource_path(self.settings.get_value("dark_mode_image_path")))

        # COWSAY
        self.cowsay_toggle_value = customtkinter.IntVar(value=self.settings.get_value("cowsay?"))
        self.cowsay_char = customtkinter.StringVar(value=self.settings.get_value("cowsay_char"))
        self.cowsay_char.trace("w", self.cowsay_char_callback)
        self.cowsay_toggle_value.trace("w", self.cowsay_toggle_callback)

        self.cowsay_setting_label = customtkinter.CTkLabel(self.style_tab, text="Cowsay setting", font=HEADING_FONT)
        self.cowsay_setting_label.grid(row=12, column=1, padx=10, pady=10, sticky="EW")

        self.cowsay_toggle_checkbox = customtkinter.CTkCheckBox(self.style_tab, offvalue=0, onvalue=1,
                                                                text="Cowsay (Works with monospaced fonts only!)",
                                                                variable=self.cowsay_toggle_value,
                                                                font=ELEMENT_FONT)

        self.cowsay_toggle_checkbox.grid(row=13, column=0, columnspan=2, padx=20, pady=10, sticky="EW")

        self.cowsay_toggle_label = customtkinter.CTkLabel(self.style_tab, text="Pick cowsay character:",
                                                          font=ELEMENT_FONT)
        self.cowsay_toggle_label.grid(row=14, column=0, padx=20, pady=10, sticky="EW")

        self.cowsay_char_combobox = customtkinter.CTkComboBox(self.style_tab, values=cowsay.main.CHARS,
                                                              variable=self.cowsay_char, font=ELEMENT_FONT)

        self.cowsay_char_combobox.grid(row=14, column=1, padx=10, pady=10, sticky="EW")

        self.refresh_wallpaper_btn2 = customtkinter.CTkButton(
            master.tabview.tab("Style"), text="Refresh Wallpaper!", command=master.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.refresh_wallpaper_btn2.grid(row=1, column=1, padx=10, pady=20, sticky="E")

    def handle_light_mode_callback(self, *args):
        self.settings.set_value("light_mode_bg_mode", self.light_theme_background_type_option_var.get())
        if self.light_theme_background_type_option_var.get() == "Solid":

            self.light_theme_background_color_label = customtkinter.CTkLabel(
                self.style_tab, text="Background color:", font=ELEMENT_FONT)
            self.light_theme_background_color_label.grid(row=7, column=0, padx=10, pady=10, sticky="EW")

            self.light_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.style_tab, text="Choose background color",
                                        command=self.set_light_theme_background_color, font=ELEMENT_FONT))
            self.light_theme_background_color_picker_button.grid(row=7, column=1, padx=10, pady=10, sticky="EW")

        elif self.light_theme_background_type_option_var.get() == "Image":

            self.light_theme_background_image_label = customtkinter.CTkLabel(
                self.style_tab, text="Background image:", font=ELEMENT_FONT)
            self.light_theme_background_image_label.grid(row=7, column=0, padx=10, pady=10, sticky="EW")
            self.light_theme_background_image_picker_button = (
                customtkinter.CTkButton(self.style_tab, text="Choose background image", font=ELEMENT_FONT,
                                        command=self.set_light_theme_background_image))

            self.light_theme_background_image_picker_button.grid(row=7, column=1, padx=10, pady=10, sticky="EW")

    def handle_dark_mode_callback(self, *args):
        self.settings.set_value("dark_mode_bg_mode", self.dark_theme_background_type_option_var.get())
        if self.dark_theme_background_type_option_var.get() == "Solid":

            self.dark_theme_background_color_label = customtkinter.CTkLabel(
                self.style_tab, text="Background color:", font=ELEMENT_FONT)
            self.dark_theme_background_color_label.grid(row=11, column=0, padx=10, pady=10, sticky="EW")

            self.dark_theme_background_color_picker_button = (
                customtkinter.CTkButton(self.style_tab, text="Choose background color",
                                        command=self.set_dark_theme_background_color, font=ELEMENT_FONT))
            self.dark_theme_background_color_picker_button.grid(row=11, column=1, padx=10, pady=10, sticky="EW")

        elif self.dark_theme_background_type_option_var.get() == "Image":

            self.dark_theme_background_image_label = customtkinter.CTkLabel(
                self.style_tab, text="Background image:", font=ELEMENT_FONT)
            self.dark_theme_background_image_label.grid(row=11, column=0, padx=10, pady=10, sticky="EW")
            self.dark_theme_background_image_picker_button = customtkinter.CTkButton(self.style_tab,
                                                                                     text="Choose background image",
                                                                                     command=self.set_dark_theme_background_image,
                                                                                     font=ELEMENT_FONT)
            self.dark_theme_background_image_picker_button.grid(row=11, column=1, padx=10, pady=10, sticky="EW")

    def text_size_warning(self, *args):
        self.settings.set_value("text_size", self.text_size_var.get())
        if self.text_size_var.get() == "":
            self.font_warning_label = customtkinter.CTkLabel(self.master.tabview.tab("Style"),
                                                             text="Font size can't be empty!",
                                                             text_color="red", font=ELEMENT_FONT)
            self.font_warning_label.grid(row=1, column=0, sticky="EW")
        else:
            try:
                self.font_warning_label.destroy()
            except AttributeError:
                pass

    def set_light_theme_text_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("light_mode_text_color"))
        color = pick_color.get()
        if color is not None:
            self.light_theme_text_color_value.set(color)
            self.settings.set_value("light_mode_text_color", color)

    def set_light_theme_background_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("light_mode_bg_color"))
        color = pick_color.get()
        if color is not None:
            self.light_theme_background_color_value.set(color)
            self.settings.set_value("light_mode_bg_color", color)

    def set_dark_theme_text_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("dark_mode_text_color"))
        color = pick_color.get()
        if color is not None:
            self.dark_theme_text_color_value.set(color)
            self.settings.set_value("dark_mode_text_color", color)

    def set_dark_theme_background_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("dark_mode_bg_color"))
        color = pick_color.get()
        if color is not None:
            self.dark_theme_background_color_value.set(color)
            self.settings.set_value("dark_mode_bg_color", color)

    def set_light_theme_background_image(self):
        file_path = fd.askopenfile()
        self.light_theme_background_image_path.set(file_path.name)
        self.settings.set_value("light_mode_image_path", file_path.name)

    def set_dark_theme_background_image(self):
        file_path = fd.askopenfile()
        self.dark_theme_background_image_path.set(file_path.name)
        self.settings.set_value("dark_mode_image_path", file_path.name)

    def dark_mode_trace(self, *args):
        self.master.set_wallpaper()

    def open_font_preview(self):
        if self.font_preview_window is None or not self.font_preview_window.winfo_exists():
            self.font_preview_window = FontPreview(self.master)
            self.font_preview_window.grab_set()
        else:
            self.font_preview_window.lift()
            self.font_preview_window.focus()

    def cowsay_char_callback(self, *args):
        self.settings.set_value("cowsay_char", self.cowsay_char.get())

    def cowsay_toggle_callback(self, *args):
        self.settings.set_value("cowsay?", self.cowsay_toggle_value.get())
