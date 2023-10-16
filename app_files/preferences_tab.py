import customtkinter


TITLE_FONT = ('Fuggles', 46, 'bold')
HEADING_FONT = ('Georgia', 18, 'bold')
ELEMENT_FONT = ('Helvetica', 14)

class PreferencesTab(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.interval_period = customtkinter.StringVar(value="20")
        self.interval_by_string = customtkinter.StringVar(value="Hour")
        self.timer = None

        self.refresh_interval_label = customtkinter.CTkLabel(
            master.tabview.tab("Preferences"), text="Refresh every:", font=ELEMENT_FONT)
        self.refresh_interval_label.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        self.interval_entry = customtkinter.CTkEntry(
            master.tabview.tab("Preferences"), font=ELEMENT_FONT, textvariable=self.interval_period)
        self.interval_entry.configure(validate="key", validatecommand=master.v_cmd)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)
        self.interval_period.trace("w", callback=self.time_interval_warning)

        self.interval_hour = customtkinter.CTkRadioButton(
            master.tabview.tab("Preferences"), text="Hour", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="Hour")
        self.interval_hour.grid(row=0, column=2, padx=(20, 0), pady=10, sticky="EW")

        self.interval_minute = customtkinter.CTkRadioButton(
            master.tabview.tab("Preferences"), text="Minutes", font=ELEMENT_FONT,
            variable=self.interval_by_string, value="Minutes")
        self.interval_minute.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="EW")

        self.interval_by_string.trace('w', self.handle_interval_callback)

    def time_interval_warning(self, *args):
        if self.interval_period.get() == "":
            self.interval_warning_label = customtkinter.CTkLabel(self.master.tabview.tab("Preferences"),
                                                                 text="Interval can't be empty!",
                                                                 text_color="red", font=ELEMENT_FONT)
            self.interval_warning_label.grid(row=1, column=0, sticky="EW")
        else:
            self.interval_warning_label.destroy()

    def handle_interval_callback(self, *args):
        if self.timer:
            self.after_cancel(self.timer)
        time = None
        if self.interval_by_string.get() == "Hour":
            time = int(self.interval_period.get()) * 3600000
        elif self.interval_by_string.get() == "Minutes":
            time = int(self.interval_period.get()) * 60000

        self.timer = self.after(time, self.master.set_wallpaper)