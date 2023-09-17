from quote import QuoteGen
from wallpaper import WallpaperGen
import customtkinter

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
            self.tabview.tab("Home"), text="Set as Wallpaper", command=self.set_wallpaper)
        self.auto_set_btn.grid(row=3, column=0, columnspan=2, padx=100, pady=10, sticky="EW")

        # Quotes Tab
        self.quote_radio_value = customtkinter.StringVar()

        self.fortune_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="The original fortune from OpenBSD", font=FONT2,
            variable=self.quote_radio_value, value="fortune")
        self.fortune_radio.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.franklin_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Quotes form Poor Richard's Almanack by Benjamin Franklin", font=FONT2,
            variable=self.quote_radio_value, value="franklin")
        self.franklin_radio.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        self.franklin_radio = customtkinter.CTkRadioButton(
            self.tabview.tab("Quotes"), text="Your own collection (separate with %):", font=FONT2,
            variable=self.quote_radio_value, value="custom")
        self.franklin_radio.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        self.text_box = customtkinter.CTkEntry(self.tabview.tab("Quotes"), height=100)
        self.text_box.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

    def set_wallpaper(self):
        selected_pack = self.quote.set_quote_pack(self.quote_radio_value.get())
        random_quote = self.quote.get_random_quote()
        self.wallpaper.set_font(font="resources/fonts/RobotoMono-Bold.ttf", font_size=20)  # FONT HAS TO BE MONOSPACED
        self.wallpaper.set_screen_size(method="manual")
        self.wallpaper.set_canvas(canvas_type="solid", bg_color="darkblue")
        self.wallpaper.draw_wallpaper(input_text=random_quote, text_color="white")


if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()
