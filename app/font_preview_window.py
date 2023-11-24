import os
import platform
import sys

import customtkinter

from font_manager import FontManager


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FontPreview(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Font Preview")
        if platform.system() == "Windows":
            self.after(200, lambda: self.iconbitmap(resource_path(os.path.join("ui_resources", "transparent.ico"))))
        elif platform.system() == "Darwin":
            pass
        elif platform.system() == "Linux":
            pass
        self.font_manager = FontManager()
        self.settings = master.settings
        self.resizable(height=False, width=False)

        self.ui_font_preview = customtkinter.CTkFont(family="Courier New", size=30)
        self.font_family = customtkinter.StringVar()
        self.font_style_path = customtkinter.StringVar(value=resource_path(self.settings.get_value("font_path")))
        self.selected_font = customtkinter.StringVar()
        self.selected_style = customtkinter.StringVar()

        self.font_test_text = customtkinter.CTkTextbox(self, font=self.ui_font_preview, width=400)
        self.font_test_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.font_test_text.insert("end", text="Basic font preview")

        self.font_info_dict = self.font_manager.get_font_dict()
        self.font_list = [font for font in self.font_info_dict]

        self.font_frame = customtkinter.CTkScrollableFrame(self, label_text="Fonts")
        self.font_frame.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        for font in self.font_list:
            self.font_radio = customtkinter.CTkRadioButton(self.font_frame, text=font,
                                                           variable=self.selected_font, value=font)
            self.font_radio.pack(padx=10, pady=10, anchor="w")

        self.font_style_frame = customtkinter.CTkFrame(self)
        self.font_style_frame.grid(row=1, column=1, padx=10, pady=10, sticky="EW")
        self.font_style_label = customtkinter.CTkLabel(self.font_style_frame, text="Styles")
        self.font_style_label.pack(padx=10, pady=10)
        self.font_style_combobox = customtkinter.CTkOptionMenu(self.font_style_frame, state="disabled",
                                                               variable=self.selected_style)
        self.font_style_combobox.pack(padx=10, pady=10)

        self.refresh_btn = customtkinter.CTkButton(self, text="Refresh Wallpaper!", fg_color="purple",
                                                   command=master.set_wallpaper)
        self.refresh_btn.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.close_btn = customtkinter.CTkButton(self, text="Done", command=self.exit_font_preview)
        self.close_btn.grid(row=2, column=1, padx=10, pady=10, sticky="EW")

        self.font_family.trace("w", self.get_style)
        self.selected_font.trace("w", self.font_chooser)
        self.selected_style.trace("w", self.style_chooser)
        self.font_style_path.trace("w", self.save_settings)

    def font_chooser(self, *args):
        self.font_family.set(self.selected_font.get())
        self.ui_font_preview.configure(family=self.font_family.get())
        try:
            self.font_style_path.set(list(self.font_info_dict[self.font_family.get()].values())[0])
        except KeyError:
            pass

    def style_chooser(self, *args):
        selected_style = self.selected_style.get()
        try:
            self.font_style_path.set(self.font_info_dict[self.font_family.get()][selected_style])
        except KeyError:
            pass

    def get_style(self, *args):
        font_styles = []
        try:
            for style in self.font_info_dict[self.font_family.get()].keys():
                font_styles.append(style)
        except KeyError:
            pass
        try:
            self.font_style_combobox.configure(values=font_styles, state="readonly")
        except AttributeError:
            pass
        try:
            self.font_style_combobox.set(font_styles[0])
        except IndexError:
            pass

    def save_settings(self, *args):
        self.settings.set_value("font_path", self.font_style_path.get())

    def exit_font_preview(self):
        self.destroy()
