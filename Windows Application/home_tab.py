import customtkinter

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class HomeTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.home_title = customtkinter.CTkLabel(
            master.tabview.tab("Home"), text="Welcome to Fortune's Window", font=TITLE_FONT, width=540)
        self.home_title.grid(row=0, column=0, columnspan=2, pady=(150, 0), sticky="EW")

        self.home_info = customtkinter.CTkLabel(
            master.tabview.tab("Home"), text="Revisit your favorite quotes, or be surprised!", font=ELEMENT_FONT)
        self.home_info.grid(row=1, column=0, columnspan=2, pady=20, sticky="EW")

        self.auto_set_btn = customtkinter.CTkButton(
            master.tabview.tab("Home"), text="Set as Wallpaper", command=self.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.auto_set_btn.grid(row=3, column=0, columnspan=2, padx=75, pady=(10,350), sticky="EW")

    def set_wallpaper(self):
        self.master.set_wallpaper()
        self.master.settings.set_value("set_as_wallpaper?", 1)