from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors  # For getting screen-size
import tempfile
import ctypes

"""
Windows SystemParametersInfo for changing wallpaper:
0x14 is for setting the desktop wallpaper
0x2 is for writing it to user's INI/ Initialization File to prevent change after reboot
"""
SPI_SETDESKWALLPAPER = 0x14
SPIF_UPDATEINIFILE   = 0x2

class WallpaperGen:
    def __init__(self):
        self.text_over_wallpaper = None
        self.text_font = None
        self.font_size = None
        self.text_color = None
        self.text_width = None
        self.text_height = None

        self.canvas = None
        self.screen_size = None
        self.background_color = None

        self.background_img_file_path = None

        self.draw = None  # PIL draw object for image manipulation

        self.temp_wallpaper = None
        self.temp_wallpaper_path = None

    def set_font(self, font, font_size):
        self.font_size = font_size
        self.text_font = ImageFont.truetype(font=font, size=self.font_size)

    def set_canvas(self, canvas_type, bg_color="black", path=None):
        if canvas_type == "solid":
            self.background_color = bg_color
            self.canvas = Image.new(mode="RGB", size=self.screen_size, color=self.background_color)

        elif canvas_type == "image":
            self.background_img_file_path = path
            self.canvas = Image.open(fp=self.background_img_file_path).resize(size=self.screen_size)

    def set_screen_size(self, method="auto", monitor_order=0, screen_width=1920, screen_height=1080):
        if method == "manual":
            self.screen_size = (screen_width, screen_height)
        elif method == "auto":
            screen_width = get_monitors()[monitor_order].width
            screen_height = get_monitors()[monitor_order].height
            self.screen_size = (screen_width, screen_height)


    def draw_wallpaper(self, input_text, text_color="grey"):
        self.text_over_wallpaper = input_text
        self.text_color = text_color
        self.draw = ImageDraw.Draw(self.canvas)
        _, _, self.text_width, self.text_height = (
            ImageDraw.Draw(self.canvas).textbbox((0, 0), text=self.text_over_wallpaper, font=self.text_font))

        self.draw.text(((self.canvas.width - self.text_width) / 2, (self.canvas.height - self.text_height) / 2),
                       text=self.text_over_wallpaper, fill=self.text_color, font=self.text_font)

    def set_wallpaper(self):
        self.temp_wallpaper = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        self.canvas.save(self.temp_wallpaper.name, "PNG")
        self.temp_wallpaper_path = self.temp_wallpaper.name
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, self.temp_wallpaper_path, SPIF_UPDATEINIFILE)
        self.temp_wallpaper.close()

