import customtkinter
import cowsay
from tkinter import filedialog as fd
import darkdetect
from CTkColorPicker import *
from CTkListbox import *
from font_manager import FontManager
from settings_manager import SettingsManager

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)


def new_select(self, index):
    """ select the option """
    for options in self.buttons.values():
        options.configure(fg_color="transparent")

    if self.multiple:
        if self.buttons[index] in self.selections:
            self.selections.remove(self.buttons[index])
            self.buttons[index].configure(fg_color="transparent", hover=False)
            self.after(100, lambda: self.buttons[index].configure(hover=self.hover))
        else:
            self.selections.append(self.buttons[index])
        for i in self.selections:
            i.configure(fg_color=self.select_color, hover=False)
            self.after(100, lambda button=i: button.configure(hover=self.hover))
    else:
        self.selected = self.buttons[index]
        self.buttons[index].configure(fg_color=self.select_color, hover=False)
        # self.after(100, lambda: self.buttons[index].configure(hover=self.hover))

    if self.command:
        self.command(self.get())


CTkListbox.select = new_select


class FontPreview(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.title("Font Preview")
        self.font_manager = FontManager()
        self.settings = SettingsManager()

        self.ui_font_preview = customtkinter.CTkFont(family="Courier New", size=35)
        self.font_family = customtkinter.StringVar()

        self.font_test_text = customtkinter.CTkTextbox(self, font=self.ui_font_preview, width=400)
        self.font_test_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.font_test_text.insert("end", text="Font Preview")

        self.font_info_dict = self.font_manager.get_font_dict()

        self.font_listbox = CTkListbox(self)
        self.font_style_listbox = CTkListbox(self)

        self.font_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="EW")
        self.font_style_listbox.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        if darkdetect.isLight():
            self.font_listbox.configure(text_color="black")
            self.font_style_listbox.configure(text_color="black")
        elif darkdetect.isDark():
            self.font_listbox.configure(text_color="white")
            self.font_style_listbox.configure(text_color="white")

        for font in self.font_info_dict:
            self.font_listbox.insert("end", font)

        self.refresh_btn = customtkinter.CTkButton(self, text="Refresh Wallpaper!", fg_color="purple",
                                                   command=master.master.set_wallpaper)
        self.refresh_btn.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.close_btn = customtkinter.CTkButton(self, text="Done", command=self.exit_font_preview)
        self.close_btn.grid(row=2, column=1, padx=10, pady=10, sticky="EW")

        self.font_listbox.bind("<ButtonRelease-1>", self.font_chooser)
        self.font_style_listbox.bind("<ButtonRelease-1>", self.style_chooser)

        self.font_style_path = customtkinter.StringVar(value=self.settings.get_value("font_path"))

        self.font_family.trace("w", self.get_style)

    def font_chooser(self, *args):
        self.font_family.set(self.font_listbox.get(self.font_listbox.curselection()))
        self.ui_font_preview.configure(family=self.font_family.get())
        try:
            self.font_style_path.set(list(self.font_info_dict[self.font_family.get()].values())[0])
        except KeyError:
            pass

    def style_chooser(self, *args):
        selected_style = self.font_style_listbox.get(self.font_style_listbox.curselection())
        try:
            self.font_style_path.set(self.font_info_dict[self.font_family.get()][selected_style])
        except KeyError:
            pass

    def get_style(self, *args):
        # self.settings.set_value("font_path", self.font_style_path.get())
        try:
            self.font_style_listbox.delete(0, "end")
        except IndexError:
            pass
        try:
            for style in self.font_info_dict[self.font_family.get()].keys():
                self.font_style_listbox.insert("end", style)
        except:
            pass

    def exit_font_preview(self):
        self.settings.set_value("font_path", self.font_style_path.get())
        self.destroy()



class StyleTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.font_preview_window = FontPreview(self)
        self.settings = SettingsManager()
        self.font_preview_window.destroy()

        self.style_tab = customtkinter.CTkScrollableFrame(master.tabview.tab("Style"), width=600, height=400)
        self.style_tab.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.font_setting_label = customtkinter.CTkLabel(self.style_tab, text="Font setting",
                                                         font=HEADING_FONT)
        self.font_setting_label.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        self.text_size_var = customtkinter.StringVar(value=self.settings.get_value("text_size"))

        self.text_size_edit_label = customtkinter.CTkLabel(
            self.style_tab, text="Text size:", font=ELEMENT_FONT)

        self.text_size_edit_label.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

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

        self.light_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.light_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.light_theme_background_type_option_var, font=ELEMENT_FONT))
        self.light_theme_background_type_options_combobox.grid(row=6, column=1, padx=10, pady=10, sticky="EW")

        self.light_theme_background_type_option_var.trace('w', self.handle_light_mode_callback)
        self.handle_light_mode_callback()

        self.light_theme_background_color_value = customtkinter.StringVar(
            value=self.settings.get_value("light_mode_bg_color"))
        self.light_theme_background_image_path = customtkinter.StringVar(
            value=self.settings.get_value("light_mode_image_path"))

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

        self.dark_theme_background_type_option_var = customtkinter.StringVar(value="Solid")

        self.dark_theme_background_type_options_combobox = (
            customtkinter.CTkComboBox(self.style_tab, values=["Solid", "Image"],
                                      variable=self.dark_theme_background_type_option_var, font=ELEMENT_FONT))
        self.dark_theme_background_type_options_combobox.grid(row=10, column=1, padx=10, pady=10, sticky="EW")

        self.dark_theme_background_type_option_var.trace('w', self.handle_dark_mode_callback)
        self.handle_dark_mode_callback()

        self.dark_theme_background_color_value = customtkinter.StringVar(
            value=self.settings.get_value("dark_mode_bg_color"))
        self.dark_theme_background_image_path = customtkinter.StringVar(
            value=self.settings.get_value("dark_mode_image_path"))

        # COWSAY
        self.cowsay_toggle_value = customtkinter.IntVar(value=0)
        self.cowsay_char = customtkinter.StringVar(value=self.settings.get_value("cowsay_char"))
        self.cowsay_char.trace("w", self.cowsay_callback)

        self.cowsay_setting_label = customtkinter.CTkLabel(self.style_tab, text="Cowsay setting", font=HEADING_FONT)
        self.cowsay_setting_label.grid(row=12, column=1, padx=10, pady=10, sticky="EW")

        self.cowsay_toggle_checkbox = customtkinter.CTkCheckBox(self.style_tab, offvalue=0, onvalue=1,
                                                                text="Cowsay (Works with monospaced fonts only!)",
                                                                variable=self.cowsay_toggle_value,
                                                                font=ELEMENT_FONT)

        self.cowsay_toggle_checkbox.grid(row=13, column=0, columnspan=2, padx=50, pady=10, sticky="EW")

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
        self.light_theme_text_color_value.set(color)
        self.settings.set_value("light_mode_text_color", color)

    def set_light_theme_background_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("light_mode_bg_color"))
        color = pick_color.get()
        self.light_theme_background_color_value.set(color)
        self.settings.set_value("light_mode_bg_color", color)

    def set_dark_theme_text_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("dark_mode_text_color"))
        color = pick_color.get()
        self.dark_theme_text_color_value.set(color)
        self.settings.set_value("dark_mode_text_color", color)

    def set_dark_theme_background_color(self):
        pick_color = AskColor(initial_color=self.settings.get_value("dark_mode_bg_color"))
        color = pick_color.get()
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
            self.font_preview_window = FontPreview(self)  # create window if its None or destroyed
        else:
            self.font_preview_window.attributes("-topmost", True)
            self.font_preview_window.lift()

    def cowsay_callback(self, *args):
        self.settings.set_value("cowsay_char", self.cowsay_char.get())
