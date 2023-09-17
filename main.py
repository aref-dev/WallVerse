from quote import QuoteGen
from wallpaper import WallpaperGen
from ui import UserInterface

if __name__ == "__main__":
    app = UserInterface(QuoteGen(), WallpaperGen())
    app.mainloop()


