import customtkinter
from database import DataBase
from tkinter import filedialog as fd

TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)
ELEMENT_FONT_BOLD = ('Helvetica', 14, 'bold')


class QuotesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DataBase()
        self.settings = master.settings
        self.quote_radio_value = customtkinter.StringVar(value=self.settings.get_value("selected_pack"))
        self.quote_radio_value.trace("w", self.delete_pack_btn_show)

        self.quote_packs = customtkinter.CTkScrollableFrame(master.tabview.tab("Quotes"), width=500,
                                                            label_text="Available Packs", label_font=ELEMENT_FONT)
        self.quote_packs.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="EW")
        self.load_packs()

        self.custom_radio = customtkinter.CTkRadioButton(
            master.tabview.tab("Quotes"), text="From your own notes (one on each line):", font=ELEMENT_FONT,
            variable=self.quote_radio_value, value="custom")
        self.custom_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkTextbox(
            master.tabview.tab("Quotes"), height=120)
        self.text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

        self.text_box.insert(index=0.1, text=self.load_textbox_file())

        self.text_box_save_btn = customtkinter.CTkButton(
            master.tabview.tab("Quotes"), text="Save", command=self.update_textbox, font=ELEMENT_FONT)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.add_pack_btn = customtkinter.CTkButton(master.tabview.tab("Quotes"), text="Add Quote Pack",
                                                    command=self.add_pack, font=ELEMENT_FONT)
        self.add_pack_btn.grid(row=5, column=0, padx=10, pady=10, sticky="W")

        self.delete_pack_btn = customtkinter.CTkButton(master.tabview.tab("Quotes"), text="Remove Pack",
                                                       command=self.delete_pack, font=ELEMENT_FONT, fg_color="red")

        self.refresh_wallpaper_btn1 = customtkinter.CTkButton(
            master.tabview.tab("Quotes"), text="Refresh Wallpaper!", command=master.set_wallpaper, fg_color="purple",
            font=ELEMENT_FONT)
        self.refresh_wallpaper_btn1.grid(row=5, column=2, padx=10, pady=10, sticky="EW")

        self.delete_pack_btn_show()

    def load_textbox_file(self):
        with open(file="quote_packs\\custom.txt", mode="r") as file:
            return file.read()

    def update_textbox(self):
        with open(file="quote_packs\\custom.txt", mode="w") as file:
            file.write(self.text_box.get(0.1, customtkinter.END))

    def add_pack(self):
        file_path = fd.askopenfile()
        self.db.add_pack(file_path.name)
        self.load_packs()

    def load_packs(self):
        packs = self.quote_packs.pack_slaves()
        for pack in packs:
            pack.pack_forget()
        all_packs = self.db.get_info()
        for pack in all_packs:
            pack_name, pack_description = pack
            pack_radio_btn = customtkinter.CTkRadioButton(
                self.quote_packs, variable=self.quote_radio_value, text=pack_name,
                value=pack_name, font=ELEMENT_FONT_BOLD)

            pack_radio_label = customtkinter.CTkLabel(self.quote_packs, text=pack_description,
                                                      font=ELEMENT_FONT, wraplength=450)
            pack_radio_btn.pack(anchor="w", pady=(10, 0))
            pack_radio_label.pack(anchor="center", pady=5)

    def delete_pack_btn_show(self, *args):
        self.settings.set_value("selected_pack", self.quote_radio_value.get())
        if self.quote_radio_value.get() != "custom":
            self.delete_pack_btn.grid(row=5, column=1, padx=10, pady=10)
        else:
            self.delete_pack_btn.grid_remove()

    def delete_pack(self):
        self.db.remove_pack(self.quote_radio_value.get())
        self.load_packs()
        self.quote_radio_value.set("custom")
