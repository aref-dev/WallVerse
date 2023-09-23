from quote import QuoteGen
from wallpaper import WallpaperGen
import customtkinter
import random

FONT = ('Arial', 18, 'italic')
FONT2 = ('Arial', 14, 'bold')

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class UserInterface(customtkinter.CTk):
    def __init__(self, quote_obj: QuoteGen, wallpaper_obj: WallpaperGen):
        super().__init__()
        self.quote = quote_obj
        self.wallpaper = wallpaper_obj

        self.app = customtkinter.CTk()
        self.app.title("WallVerse")
        self.app.geometry("600x600")

        self.tabview = customtkinter.CTkTabview(self, width=500)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))

        self.tabview.add("Home")
        self.tabview.add("Quotes")
        self.tabview.add("Style")
        self.tabview.add("Preferences")

        self.home_title = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Welcome to Fortune's Window", font=FONT)
        self.home_title.grid(row=0, column=0, columnspan=2, padx=100, pady=20, sticky="EW")

        self.home_info = customtkinter.CTkLabel(
            self.tabview.tab("Home"), text="Revisit your favorite quotes, or be surprised!", font=FONT2)
        self.home_info.grid(row=1, column=0, columnspan=2, padx=100, pady=20, sticky="EW")

        self.auto_set_btn = customtkinter.CTkButton(
            self.tabview.tab("Home"), text="Set as Wallpaper", command=self.set_wallpaper_auto)
        self.auto_set_btn.grid(row=3, column=0, columnspan=2, padx=100, pady=10, sticky="EW")

        # Quotes Tab
        self.quote_radio_value = customtkinter.StringVar(value="fortune")

        self.fortune_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="The original fortune from OpenBSD", font=FONT2,
            variable=self.quote_radio_value, value="fortune")
        self.fortune_radio.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.franklin_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Quotes form Poor Richard's Almanack by Benjamin Franklin", font=FONT2,
            variable=self.quote_radio_value, value="franklin")
        self.franklin_radio.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.custom_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Your own collection (one quote on each line):", font=FONT2,
            variable=self.quote_radio_value, value="custom")
        self.custom_radio.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkTextbox(
            self.tabview.tab("Quotes"), height=100)
        self.text_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="EW")

        self.text_box.insert(index=0.1, text=self.load_textbox_file())

        self.text_box_save_btn = customtkinter.CTkButton(
            self.tabview.tab("Quotes"), text="Save", command=self.update_textbox)
        self.text_box_save_btn.grid(row=4, column=2, padx=10, pady=10, sticky="EW")

        self.custom_set_btn = customtkinter.CTkButton(
            self.tabview.tab("Quotes"), text="Set as Wallpaper", command=self.set_wallpaper_custom)
        self.custom_set_btn.grid(row=5, column=2, padx=10, pady=10, sticky="EW")

    def load_textbox_file(self):
        with open(file="resources/quote_packs/custom.txt", mode="r") as file:
            return file.read()

    def update_textbox(self):
        with open(file="resources/quote_packs/custom.txt", mode="w") as file:
            file.write(self.text_box.get(0.1, customtkinter.END))

    def set_wallpaper_custom(self):
        self.quote.set_quote_pack(self.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        self.wallpaper.set_font(font="resources/fonts/RobotoMono-Bold.ttf", font_size=20)  # FONT HAS TO BE MONOSPACED
        self.wallpaper.set_screen_size(method="auto")
        self.wallpaper.set_canvas(canvas_type="solid", bg_color="black")
        self.wallpaper.draw_wallpaper(input_text=random_quote, text_color="white")

    def set_wallpaper_auto(self):
        self.quote.set_quote_pack("fortune")
        random_quote = self.quote.get_random_quote()
        cowsay_quote = self.quote.pass_to_cowsay(random_quote)
        self.wallpaper.set_font(font="resources/fonts/RobotoMono-Bold.ttf", font_size=20)  # FONT HAS TO BE MONOSPACED
        self.wallpaper.set_screen_size(method="auto")
        self.wallpaper.set_canvas(canvas_type="solid", bg_color="black")
        self.wallpaper.draw_wallpaper(input_text=cowsay_quote, text_color="white")
        self.wallpaper.set_wallpaper()

if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()
