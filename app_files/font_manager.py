from fontTools import ttLib
from os import walk

class FontManager:
    def __init__(self):
        self.system_font_path = "C:\\Windows\\Fonts"

        self.fonts_path = []
        for (dirpath, dirnames, filenames) in walk(fr'{self.system_font_path}'):
            for i in filenames:
                if any(i.endswith(ext) for ext in ['.ttf', '.otf', '.ttc', '.ttz', '.woff', '.woff2']):
                    self.fonts_path.append(dirpath.replace('\\\\', '\\') + '\\' + i)

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
