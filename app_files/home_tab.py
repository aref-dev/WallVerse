import customtkinter

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class HomeTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.home_title = customtkinter.CTkLabel(
            master.tabview.tab("Home"), text="Welcome to Fortune's Window", font=TITLE_FONT)
        self.home_title.grid(row=0, column=0, columnspan=2, padx=100, pady=(30, 0), sticky="EW")

        self.home_info = customtkinter.CTkLabel(
            master.tabview.tab("Home"), text="Revisit your favorite quotes, or be surprised!", font=ELEMENT_FONT)
        self.home_info.grid(row=1, column=0, columnspan=2, padx=100, pady=20, sticky="EW")

        self.auto_set_btn = customtkinter.CTkButton(
            master.tabview.tab("Home"), text="Set as Wallpaper", command=master.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.auto_set_btn.grid(row=3, column=0, columnspan=2, padx=100, pady=10, sticky="EW")
