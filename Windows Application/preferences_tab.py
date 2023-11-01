import os.path
import customtkinter
import winshell
import sys


HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class PreferencesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.settings = master.settings
        self.interval_period = customtkinter.StringVar(value=self.settings.get_value("refresh_int"))
        self.interval_by_string = customtkinter.StringVar(value=self.settings.get_value("refresh_unit"))
        self.timer = None
        self.handle_interval_callback()

        self.preferences_frame = customtkinter.CTkFrame(master.tabview.tab("Preferences"))
        self.preferences_frame.grid(row=0, column=0)

        self.refresh_interval_label = customtkinter.CTkLabel(
            self.preferences_frame, text="Refresh every:", font=ELEMENT_FONT)
        self.refresh_interval_label.grid(row=0, column=0, padx=10, pady=(40, 10), sticky="EW")

        self.interval_entry = customtkinter.CTkEntry(
            self.preferences_frame, font=ELEMENT_FONT, textvariable=self.interval_period)
        self.interval_entry.configure(validate="key", validatecommand=master.v_cmd)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=(40, 10))
        self.interval_period.trace("w", callback=self.time_interval_warning)
        self.interval_period.trace("w", self.handle_interval_callback)

        self.interval_hours = customtkinter.CTkRadioButton(
            self.preferences_frame, text="hours", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="hours")
        self.interval_hours.grid(row=0, column=2, padx=(20, 0), pady=(40, 10), sticky="EW")

        self.interval_minutes = customtkinter.CTkRadioButton(
            self.preferences_frame, text="minutes", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="minutes")
        self.interval_minutes.grid(row=0, column=3, padx=(0, 10), pady=(40, 10), sticky="EW")

        self.interval_by_string.trace('w', self.handle_interval_callback)

        self.startup_var = customtkinter.IntVar(value=self.settings.get_value("start_with_os?"))

        self.startup_checkbox = customtkinter.CTkSwitch(
            self.preferences_frame, text="Start with Windows?",
            variable=self.startup_var, onvalue=1, offvalue=0, width=390)
        self.startup_checkbox.grid(row=2, column=0, columnspan=3, padx=20, pady=(20,410), sticky="EW")

        self.startup_var.trace("w", self.check_startup)
        self.time_interval_warning()

    def time_interval_warning(self, *args):
        if self.interval_period.get() == "":
            self.interval_warning_label = customtkinter.CTkLabel(self.master.tabview.tab("Preferences"),
                                                                 text="Interval can't be empty!",
                                                                 text_color="red", font=ELEMENT_FONT)
            self.interval_warning_label.grid(row=1, column=0, sticky="EW")
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
        shortcut_path = os.path.join(startup_folder, "WallVerse.lnk")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.realpath(sys.executable)
        if self.startup_var.get() == 0:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
        elif self.startup_var.get() == 1:
            self.settings.set_value("set_as_wallpaper?", 1)
            if not os.path.exists(shortcut_path):
                with winshell.shortcut(shortcut_path) as shortcut:
                    shortcut.path = exe_path
                    shortcut.write()


