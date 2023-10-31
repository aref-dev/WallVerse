import customtkinter
import darkdetect
from CTkListbox import *
from font_manager import FontManager

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
        super().__init__(master)
        self.title("Font Preview")
        self.font_manager = FontManager()
        self.settings = master.settings
        self.resizable(height=False, width=False)

        self.ui_font_preview = customtkinter.CTkFont(family="Courier New", size=30)
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
                                                   command=master.set_wallpaper)
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

