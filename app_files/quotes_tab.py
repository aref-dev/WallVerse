import customtkinter
from database import DataBase
from tkinter import filedialog as fd


TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class QuotesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.available_packs = []
        self.db = DataBase()
        self.quote_radio_value = customtkinter.StringVar(value="franklin")

        self.quote_packs = customtkinter.CTkScrollableFrame(master.tabview.tab("Quotes"), width=500)
        self.quote_packs.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.custom_radio = customtkinter.CTkRadioButton(
            master.tabview.tab("Quotes"), text="From your own notes (one quote on each line):", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="custom")
        self.custom_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkTextbox(
            master.tabview.tab("Quotes"), height=100)
        self.text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

        self.text_box.insert(index=0.1, text=self.load_textbox_file())

        self.text_box_save_btn = customtkinter.CTkButton(
            master.tabview.tab("Quotes"), text="Save", command=self.update_textbox, font=ELEMENT_FONT)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.add_pack_btn = customtkinter.CTkButton(master.tabview.tab("Quotes"), text="Add Quote Pack",
                                                    command=self.add_pack, font=ELEMENT_FONT)
        self.add_pack_btn.grid(row=5, column=0, padx=10, pady=10, sticky="W")

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

    def add_pack(self):
        file_path = fd.askopenfile()
        self.db.insert(file_path.name)

    # def load_packs(self):
    #     for pack in self.db.read
    #
    #

        # for pack in self.available_packs:
        #     print(self.available_packs[0])
            # pack_radio_btn = customtkinter.CTkRadioButton(
            #     self.quote_packs, variable=self.quote_radio_value, value=pack["Name"])
            # pack_radio_btn.pack()
            # pack_radio_label = customtkinter.CTkLabel(self.quote_packs, text=f"{name}: {description}",
            #                                           font=ELEMENT_FONT, wraplength=500)
            # pack_radio_label.pack()
