from fontTools import ttLib
import os, sys
from os import walk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class FontManager:
    def __init__(self):
        self.app_fonts_path = resource_path(os.path.join("ui_resources", "fonts"))
        self.imported_fonts_path = os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\Windows\\Fonts"
        self.system_font_paths = [self.app_fonts_path, self.imported_fonts_path]

        self.fonts_path = []

        for path in self.system_font_paths:
            for (dirpath, dirnames, filenames) in walk(fr'{path}'):
                for i in filenames:
                    if any(i.endswith(ext) for ext in ['.ttf', '.otf', '.ttc', '.ttz', '.woff', '.woff2']):
                        font_file_path = os.path.join(dirpath, i)
                        self.fonts_path.append(font_file_path)

        def getFont(font, font_path):
            x = lambda x: font['name'].getDebugName(x)
            if x(16) is None:
                return x(1), x(2), font_path
            if x(16) is not None:
                return x(16), x(17), font_path
            else:
                pass

        self.fonts = []
        for i in range(len(self.fonts_path)):
            j = self.fonts_path[i]
            if not j.endswith('.ttc'):
                self.fonts.append(getFont(ttLib.TTFont(j), j))
            if j.endswith('.ttc'):
                try:
                    for k in range(100):
                        self.fonts.append(getFont(ttLib.TTFont(j, fontNumber=k), j))
                except:
                    pass

        self.fonts_dict = {}

        no_duplicates = []
        for i in self.fonts:
            index_0 = i[0]
            if index_0 not in no_duplicates:
                no_duplicates.append(index_0)

        for i in self.fonts:
            for k in no_duplicates:
                if i[0] == k:
                    self.fonts_dict[k] = {str(i[1]) : str(i[2]).split('\\')[-1]}
                    for j in self.fonts:
                        if i[0] == j[0]:
                            self.fonts_dict[k][j[1]] = j[2]

    def get_font_dict(self):
        return self.fonts_dict

