import customtkinter
import cowsay
import darkdetect
import threading
from tkinter import filedialog as fd
from CTkColorPicker import *
from CTkListbox import *
import matplotlib.font_manager as font_manager

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)


class FontPreview(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.font_path = None
        self.title("Font Preview")

        self.chosen_font = customtkinter.CTkFont(family="Courier New", size=35)

        self.font_test_text = customtkinter.CTkTextbox(self, font=self.chosen_font, width=400)
        self.font_test_text.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.font_test_text.insert("end", text="Font Preview")

        self.font_listbox = CTkListbox(self)
        self.font_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        self.system_fonts = font_manager.findSystemFonts()
        self.font_info_dict = {}

        for name in self.system_fonts:
            self.font_info_dict[name] = font_manager.FontProperties(fname=name).get_name()

        for font in self.font_info_dict.values():
            self.font_listbox.insert("end", font)

        self.font_select_btn = customtkinter.CTkButton(self, text="Select Font", command=self.destroy)
        self.font_select_btn.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.font_listbox.bind("<ButtonRelease-1>", self.font_chooser)

        self.font_style_var = customtkinter.StringVar(value='C:\\Windows\\Fonts\\seguiemj.ttf')
        self.font_style_var.trace("w", self.return_font)

    def font_chooser(self, *args):
        self.chosen_font.configure(family=self.font_listbox.get(self.font_listbox.curselection()))
        self.font_style_var.set([k for k, v in self.font_info_dict.items()
                                 if v == self.font_listbox.get(self.font_listbox.curselection())][0])
        print(self.font_style_var.get())

    def return_font(self):
        new_path = self.font_path.replace("\\", "\\\\")
        return new_path


class StyleTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.font_preview_window = FontPreview(self)
        self.font_preview_window.destroy()

        self.t = threading.Thread(target=darkdetect.listener, args=(self.dark_mode_trace,))
        self.t.daemon = True
        self.t.start()

        self.style_tab = customtkinter.CTkScrollableFrame(master.tabview.tab("Style"), width=600, height=400)
        self.style_tab.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.font_setting_label = customtkinter.CTkLabel(self.style_tab, text="Font setting",
                                                         font=HEADING_FONT)
        self.font_setting_label.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        self.text_size_var = customtkinter.StringVar(value="18")

        self.text_size_edit_label = customtkinter.CTkLabel(
            self.style_tab, text="Text size:", font=ELEMENT_FONT)

        self.text_size_edit_label.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.text_size_entry = customtkinter.CTkEntry(self.style_tab, textvariable=self.text_size_var)
        self.text_size_entry.configure(validate="key", validatecommand=master.v_cmd)
        self.text_size_entry.grid(row=2, column=1, padx=10, pady=10, sticky="EW")
        self.text_size_var.trace("w", callback=self.text_size_warning)

        # font_path = Path("fonts")
        #
        # available_fonts = [font.name for font in font_path.iterdir()]

        self.font_style_edit_label = customtkinter.CTkLabel(
            self.style_tab, text="Font type:", font=ELEMENT_FONT)
        self.font_style_edit_label.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

        self.font_preview_btn = customtkinter.CTkButton(self.style_tab, text="Choose Font",
                                                        command=self.open_font_preview, font=ELEMENT_FONT)
        self.font_preview_btn.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="EW")
        # self.font_combobox = customtkinter.CTkComboBox(
        #     self.style_tab, values=available_fonts, variable=self.font_style_var)
        #
        # self.font_combobox.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="EW")

        # LIGHT-MODE THEME OPTIONS
        self.light_theme_label = customtkinter.CTkLabel(
            self.style_tab, text="Light mode theme settings", font=HEADING_FONT)
        self.light_theme_label.grid(row=4, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_label = customtkinter.CTkLabel(
            self.style_tab, text="Text color:", font=ELEMENT_FONT)
        self.light_theme_text_color_label.grid(row=5, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_text_color_value = customtkinter.StringVar(value="#F1F0E8")

        self.light_theme_text_color_picker_button = customtkinter.CTkButton(self.style_tab,
                                                                            text="Choose text color",
                                                                            command=self.set_light_theme_text_color,
                                                                            font=ELEMENT_FONT)
        self.light_theme_text_color_picker_button.grid(row=5, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_label = customtkinter.CTkLabel(
            self.style_tab, text="Background:")
        self.light_theme_background_type_label.grid(row=6, column=0, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.light_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.light_theme_background_type_option_var, font=ELEMENT_FONT))
        self.light_theme_background_type_options_combobox.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var.trace('w', self.handle_light_mode_callback)
        self.handle_light_mode_callback()

        self.light_theme_background_color_value = customtkinter.StringVar(value="#96B6C5")
        self.light_theme_background_image_path = customtkinter.StringVar()

        # DARK-MODE THEME OPTIONS
        self.dark_theme_label = customtkinter.CTkLabel(
            self.style_tab, text="Dark mode theme settings", font=HEADING_FONT)
        self.dark_theme_label.grid(row=8, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_label = customtkinter.CTkLabel(
            self.style_tab, text="Text color:", font=ELEMENT_FONT)
        self.dark_theme_text_color_label.grid(row=9, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_text_color_value = customtkinter.StringVar(value="#005B41")

        self.dark_theme_text_color_picker_button = customtkinter.CTkButton(self.style_tab,
                                                                           text="Choose text color",
                                                                           command=self.set_dark_theme_text_color,
                                                                           font=ELEMENT_FONT)
        self.dark_theme_text_color_picker_button.grid(row=9, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_label = customtkinter.CTkLabel(
            self.style_tab, text="Background:", font=ELEMENT_FONT)
        self.dark_theme_background_type_label.grid(row=10, column=0, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.dark_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.dark_theme_background_type_option_var, font=ELEMENT_FONT))
        self.dark_theme_background_type_options_combobox.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var.trace('w', self.handle_dark_mode_callback)
        self.handle_dark_mode_callback()

        self.dark_theme_background_color_value = customtkinter.StringVar(value="#0F0F0F")
        self.dark_theme_background_image_path = customtkinter.StringVar()

        # COWSAY
        self.cowsay_toggle_value = customtkinter.IntVar(value=0)
        self.cowsay_char = customtkinter.StringVar(value="tux")

        self.cowsay_setting_label = customtkinter.CTkLabel(self.style_tab, text="Cowsay setting", font=HEADING_FONT)
        self.cowsay_setting_label.grid(row=12, column=1, padx=10, pady=10, sticky="EW")

        self.cowsay_toggle_checkbox = customtkinter.CTkCheckBox(self.style_tab, offvalue=0, onvalue=1,
                                                                text="Cowsay",
                                                                variable=self.cowsay_toggle_value,
                                                                font=ELEMENT_FONT)

        self.cowsay_toggle_checkbox.grid(row=13, column=0, padx=50, pady=10, sticky="EW")

        self.cowsay_toggle_label = customtkinter.CTkLabel(self.style_tab, text="Pick cowsay character:",
                                                          font=ELEMENT_FONT)
        self.cowsay_toggle_label.grid(row=14, column=0, padx=50, pady=10, sticky="EW")

        self.cowsay_char_combobox = customtkinter.CTkComboBox(self.style_tab, values=cowsay.main.CHARS,
                                                              variable=self.cowsay_char, font=ELEMENT_FONT)

        self.cowsay_char_combobox.grid(row=14, column=1, padx=10, pady=10, sticky="EW")

        self.refresh_wallpaper_btn2 = customtkinter.CTkButton(
            master.tabview.tab("Style"), text="Refresh Wallpaper!", command=master.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.refresh_wallpaper_btn2.grid(row=1, column=1, padx=10, pady=10, sticky="E")

    def handle_light_mode_callback(self, *args):
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
        if self.text_size_var.get() == "":
            self.font_warning_label = customtkinter.CTkLabel(self.master.tabview.tab("Style"),
                                                             text="Font size can't be empty!",
                                                             text_color="red", font=ELEMENT_FONT)
            self.font_warning_label.grid(row=1, column=0, sticky="EW")
        else:
            self.font_warning_label.destroy()

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
        self.master.set_wallpaper()

    def open_font_preview(self):
        if self.font_preview_window is None or not self.font_preview_window.winfo_exists():
            self.font_preview_window = FontPreview(self)  # create window if its None or destroyed
        else:
            self.font_preview_window.focus()
