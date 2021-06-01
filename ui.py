#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import font
from ttkthemes import ThemedStyle
from tkinter import messagebox

import os
import sys

import configurator
import controller
import driver

CURRENT_VERSION = "0.1.5"

# Modes
MODE_AUTO = 0
MODE_BASIC = 1
MODE_ADVANCED = 2
MODE_COOLERBOOST = 3

# For a list of themes: https://ttkthemes.readthedocs.io/en/latest/themes.html
DARK_THEME = "black"
LIGHT_THEME = "scidgrey"


class AppUI:
    def __init__(self, root):
        # Get config
        self.config = configurator.get_config()

        # setting title
        root.title("OpenFreezeCenter")

        # setting window size
        self.width = 370 * 2
        self.height = 270 * 2
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            self.width,
            self.height,
            (screenwidth - self.width) / 2,
            (screenheight - self.height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Asign theme
        self.style = ThemedStyle(root)
        self.ft = font.Font(family="Helvetica", size=12)

        # Tabbed ui
        self.tab_parent = ttk.Notebook(root)

        self.tab_overview = ttk.Frame(self.tab_parent)
        self.tab_monitor = ttk.Frame(self.tab_parent)
        self.tab_settings = ttk.Frame(self.tab_parent)
        self.tab_about = ttk.Frame(self.tab_parent)

        self.tab_parent.add(self.tab_overview, text="Overview")
        self.tab_parent.add(self.tab_monitor, text="Monitor")
        self.tab_parent.add(self.tab_settings, text="Settings")
        self.tab_parent.add(self.tab_about, text="About")

        self.tab_parent.pack(expand=1, fill="both")

        # Add ui elements
        self.setup_about()
        self.setup_settings()
        self.setup_overview()
        self.setup_monitor()

        self.update_ui()

    def update_ui(self):

        # Light/Dark theme
        if self.config["ui"]["dark_mode_enabled"] == True:
            self.button_dark_mode["text"] = "Dark Mode"
            self.style.set_theme(DARK_THEME)
        else:
            self.button_dark_mode["text"] = "Light Mode"
            self.style.set_theme(LIGHT_THEME)

        # Installed
        if not driver.is_installed():
            self.button_install["text"] = "Install Driver"
        else:
            self.button_install["text"] = "Uninstall Driver"

        # Mode
        self.button_auto["fg"] = "black"
        self.button_basic["fg"] = "black"
        self.button_advanced["fg"] = "black"
        self.button_boost["fg"] = "black"

        if self.config["settings"]["mode"] == MODE_AUTO:
            self.button_auto["fg"] = "red"
        elif self.config["settings"]["mode"] == MODE_BASIC:
            self.button_basic["fg"] = "red"
        elif self.config["settings"]["mode"] == MODE_ADVANCED:
            self.button_advanced["fg"] = "red"
        elif self.config["settings"]["mode"] == MODE_COOLERBOOST:
            self.button_boost["fg"] = "red"

    #######################################
    ### UI Setup Design                ####
    #######################################

    def setup_monitor(self):

        self.label_min = tk.Label(self.tab_monitor)
        self.label_min["font"] = self.ft
        self.label_min["text"] = "Min."

        self.label_max = tk.Label(self.tab_monitor)
        self.label_max["font"] = self.ft
        self.label_max["text"] = "Max."

        self.label_cur = tk.Label(self.tab_monitor)
        self.label_cur["font"] = self.ft
        self.label_cur["text"] = "Current"

        self.label_cpu_temp = tk.Label(self.tab_monitor)
        self.label_cpu_temp["font"] = self.ft
        self.label_cpu_temp["text"] = "CPU Temp."

        self.label_gpu_temp = tk.Label(self.tab_monitor)
        self.label_gpu_temp["font"] = self.ft
        self.label_gpu_temp["text"] = "GPU Temp."

        self.label_cpu_rpm = tk.Label(self.tab_monitor)
        self.label_cpu_rpm["font"] = self.ft
        self.label_cpu_rpm["text"] = "CPU Fan RPM"

        self.label_gpu_rpm = tk.Label(self.tab_monitor)
        self.label_gpu_rpm["font"] = self.ft
        self.label_gpu_rpm["text"] = "GPU Fan RPM"

        # Position elements
        self.label_cpu_temp.place(y=30, x=0, width=120, height=30)
        self.label_gpu_temp.place(y=60, x=0, width=120, height=30)
        self.label_cpu_rpm.place(y=90, x=0, width=120, height=30)
        self.label_gpu_rpm.place(y=120, x=0, width=120, height=30)

        self.label_cur.place(y=0, x=120, width=60, height=30)
        self.label_min.place(y=0, x=180, width=60, height=30)
        self.label_max.place(y=0, x=240, width=60, height=30)

        # TODO: Add monitoring values

    def setup_overview(self):

        self.button_auto = tk.Button(self.tab_overview)
        self.button_auto["command"] = self.button_auto_command
        self.button_auto["font"] = self.ft
        self.button_auto["text"] = "Auto"

        self.button_basic = tk.Button(self.tab_overview)
        self.button_basic["command"] = self.button_basic_command
        self.button_basic["font"] = self.ft
        self.button_basic["text"] = "Basic"

        self.button_advanced = tk.Button(self.tab_overview)
        self.button_advanced["command"] = self.button_advanced_command
        self.button_advanced["font"] = self.ft
        self.button_advanced["text"] = "Advanced"

        self.button_boost = tk.Button(self.tab_overview)
        self.button_boost["command"] = self.button_boost_command
        self.button_boost["font"] = self.ft
        self.button_boost["text"] = "Cooler Booster"

        # Placement
        self.button_auto.place(
            y=25, x=self.width / 3, width=self.width / 3, height=self.height / 8
        )
        self.button_basic.place(
            y=25 + 1 * self.height / 8,
            x=self.width / 3,
            width=self.width / 3,
            height=self.height / 8,
        )
        self.button_advanced.place(
            y=25 + 2 * self.height / 8,
            x=self.width / 3,
            width=self.width / 3,
            height=self.height / 8,
        )
        self.button_boost.place(
            y=25 + 3 * self.height / 8,
            x=self.width / 3,
            width=self.width / 3,
            height=self.height / 8,
        )

    def setup_about(self):
        self.label1 = tk.Label(self.tab_about)
        self.label1["font"] = self.ft
        self.label1["justify"] = "center"
        self.label1[
            "text"
        ] = "Creator(s) :-> Aditya Kumar Bajpai\nRob Oudendijk\nLiam Lalonde"

        self.label2 = tk.Label(self.tab_about)
        self.label2["font"] = self.ft
        self.label2["justify"] = "center"
        self.label2["text"] = "Version %s" % CURRENT_VERSION

        # Placement
        self.label1.place(x=0, y=60, width=self.width, height=120)
        self.label2.place(x=0, y=25, width=self.width, height=30)

    def setup_settings(self):

        self.button_install = tk.Button(self.tab_settings)
        self.button_install["command"] = self.button_install_command
        self.button_install["font"] = self.ft

        self.button_dark_mode = tk.Button(self.tab_settings)
        self.button_dark_mode["command"] = self.button_dark_mode_command
        self.button_dark_mode["font"] = self.ft

        # Placement
        self.button_install.place(
            y=25, x=self.width / 3, width=self.width / 3, height=self.height / 8
        )
        self.button_dark_mode.place(
            y=25 + 1 * self.height / 8,
            x=self.width / 3,
            width=self.width / 3,
            height=self.height / 8,
        )

    #######################################
    ### Command Button On Click Events ####
    #######################################

    def button_auto_command(self):
        self.config["settings"]["mode"] = MODE_AUTO
        self.set_mode()
        self.update_ui()

    def button_basic_command(self):
        self.config["settings"]["mode"] = MODE_BASIC
        self.set_mode()
        self.update_ui()

    def button_advanced_command(self):
        self.config["settings"]["mode"] = MODE_ADVANCED
        self.set_mode()
        self.update_ui()

    def button_boost_command(self):
        self.config["settings"]["mode"] = MODE_COOLERBOOST
        self.set_mode()
        self.update_ui()

    def button_install_command(self):

        if driver.is_installed():
            res = driver.install()
            if res == True:
                messagebox.showinfo(
                    "Installation Complete!",
                    "Please Reboot your system to enable EC module write capablities of script",
                )
            else:
                messagebox.showinfo(
                    "Installation Failure!",
                    "Please check the logs for more information",
                )
        else:
            res = driver.uninstall()
            if res == True:
                messagebox.showinfo(
                    "Uninstallation Complete!",
                    "Please Reboot your system to disable EC module write capablities of script",
                )
            else:
                messagebox.showinfo(
                    "Uninstallation Failure!",
                    "Please check the logs for more information",
                )

        self.update_ui()

    def button_dark_mode_command(self):
        # Switch
        if self.config["ui"]["dark_mode_enabled"] == True:
            self.config["ui"]["dark_mode_enabled"] = False
        else:
            self.config["ui"]["dark_mode_enabled"] = True

        # Update file
        configurator.write_config(self.config)

        self.update_ui()

    def set_mode(self):
        mode = self.config["settings"]["mode"]
        vr = self.config["settings"]["vr_custom"]
        offset = self.config["settings"]["offset"]

        print("setting mode %s %s %s" % (mode, vr, offset))

        # Ask for root permissions here
        # controller.enable_mode(mode, vr, offset)


def open_ui():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    open_ui()
