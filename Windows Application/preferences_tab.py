import os.path
import customtkinter
import winshell
from settings_manager import SettingsManager


TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class PreferencesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.settings = SettingsManager()
        self.interval_period = customtkinter.StringVar(value=self.settings.get_value("refresh_int"))
        self.interval_by_string = customtkinter.StringVar(value=self.settings.get_value("refresh_unit"))
        self.timer = None
        self.handle_interval_callback()

        self.refresh_interval_label = customtkinter.CTkLabel(
            master.tabview.tab("Preferences"), text="Refresh every:", font=ELEMENT_FONT)
        self.refresh_interval_label.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.interval_entry = customtkinter.CTkEntry(
            master.tabview.tab("Preferences"), font=ELEMENT_FONT, textvariable=self.interval_period)
        self.interval_entry.configure(validate="key", validatecommand=master.v_cmd)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)
        self.interval_period.trace("w", callback=self.time_interval_warning)
        self.interval_period.trace("w", self.handle_interval_callback)

        self.interval_hours = customtkinter.CTkRadioButton(
            master.tabview.tab("Preferences"), text="hours", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="hours")
        self.interval_hours.grid(row=0, column=2, padx=(20, 0), pady=10, sticky="EW")

        self.interval_minutes = customtkinter.CTkRadioButton(
            master.tabview.tab("Preferences"), text="minutes", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="minutes")
        self.interval_minutes.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="EW")

        self.interval_by_string.trace('w', self.handle_interval_callback)

        self.startup_var = customtkinter.IntVar(value=self.settings.get_value("start_with_os?"))

        self.startup_checkbox = customtkinter.CTkCheckBox(
            master.tabview.tab("Preferences"), text="Start with Windows?",
            variable=self.startup_var, onvalue=1, offvalue=0)
        self.startup_checkbox.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="EW")

        self.startup_var.trace("w", self.check_startup)

    def time_interval_warning(self, *args):
        if self.interval_period.get() == "":
            self.interval_warning_label = customtkinter.CTkLabel(self.master.tabview.tab("Preferences"),
                                                                 text="Interval can't be empty!",
                                                                 text_color="red", font=ELEMENT_FONT)
            self.interval_warning_label.grid(row=2, column=0, sticky="EW")
        else:
            try:
                self.interval_warning_label.destroy()
            except AttributeError:
                pass

    def handle_interval_callback(self, *args):
        self.settings.set_value("refresh_int", self.interval_period.get())
        self.settings.set_value("refresh_unit",self.interval_by_string.get())
        if self.timer:
            self.after_cancel(self.timer)
        time = None
        try:
            if self.interval_by_string.get() == "hours":
                time = int(self.interval_period.get()) * 3600000
            elif self.interval_by_string.get() == "minutes":
                time = int(self.interval_period.get()) * 60000
            self.timer = self.after(time, self.master.set_wallpaper)
        except ValueError:
            pass

    def check_startup(self, *args):
        self.settings.set_value("start_with_os?", self.startup_var.get())
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        shortcut_path = os.path.join(startup_folder, "Fortune's Window.lnk")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(current_folder, "Fortune's Window.exe")
        if self.startup_var.get() == 0:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
        elif self.startup_var.get() == 1:
            if not os.path.exists(shortcut_path):
                with winshell.shortcut(shortcut_path) as shortcut:
                    shortcut.path = exe_path
                    shortcut.write()


