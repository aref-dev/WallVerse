import customtkinter

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class QuotesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.quote_radio_value = customtkinter.StringVar(value="fortune")

        self.fortune_radio = customtkinter.CTkRadioButton(
            master.tabview.tab("Quotes"), text="The original fortune from OpenBSD", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="fortune")
        self.fortune_radio.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.franklin_radio = customtkinter.CTkRadioButton(
            master.tabview.tab("Quotes"), text="Quotes form Poor Richard's Almanack by Benjamin Franklin",
            font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="franklin")
        self.franklin_radio.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.custom_radio = customtkinter.CTkRadioButton(
            master.tabview.tab("Quotes"), text="Your own collection (one quote on each line):", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="custom")
        self.custom_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkTextbox(
            master.tabview.tab("Quotes"), height=100)
        self.text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

        self.text_box.insert(index=0.1, text=self.load_textbox_file())

        self.text_box_save_btn = customtkinter.CTkButton(
            master.tabview.tab("Quotes"), text="Save", command=self.update_textbox, font=ELEMENT_FONT)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.refresh_wallpaper_btn1 = customtkinter.CTkButton(
            master.tabview.tab("Quotes"), text="Refresh wallpaper!", command=master.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.refresh_wallpaper_btn1.grid(row=5, column=2, padx=10, pady=10, sticky="EW")

    def load_textbox_file(self):
        with open(file="quote_packs/custom.txt", mode="r") as file:
            return file.read()

    def update_textbox(self):
        with open(file="quote_packs/custom.txt", mode="w") as file:
            file.write(self.text_box.get(0.1, customtkinter.END))
