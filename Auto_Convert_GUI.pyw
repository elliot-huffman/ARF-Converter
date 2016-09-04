from tkinter import *
from Auto_Convert import *


# Imports tkinter, a GUI library for python and Auto_Convert, a program for bulk converting ARF files.


def main_window():
    main_window = Tk()

    # Create main Window.

    main_window.title("ARF Auto Converter")
    main_window.minsize(250, 200)

    # set window properties.

    main_window.grid_columnconfigure(0,weight=1)
    main_window.grid_columnconfigure(1,weight=1)
    main_window.grid_rowconfigure(0,weight=1)
    main_window.grid_rowconfigure(1,weight=1)
    main_window.grid_rowconfigure(2,weight=1)
    main_window.grid_rowconfigure(3,weight=1)

    # make the interface responsive.

    mw_welcome_text = Label(main_window, text="Welcome to the ARF auto converter!")
    mw_MP4_button = Button(main_window, text="Convert to MP4", fg="green", command=button_mp4)
    mw_WMV_button = Button(main_window, text="Convert to WMV", command=button_wmv)
    mw_SWF_button = Button(main_window, text="Convert to SWF", fg="red", command=button_swf)
    mw_options_button = Button(main_window, text="Advanced Options")
    mw_exit_button = Button(main_window, text="Exit", command=exit)

    #Creates the Widgets.

    mw_welcome_text.grid(columnspan=2, sticky="NESW")
    mw_MP4_button.grid(row=1, sticky="NESW")
    mw_WMV_button.grid(row=2, sticky="NESW")
    mw_SWF_button.grid(row=3, sticky="NESW")
    mw_options_button.grid(row=1, column=1, sticky="NESW")
    mw_exit_button.grid(row=2, column=1, sticky="NESW")
    
    # Aranges the widgets on the window.

    main_window.mainloop()

    # Keep the main window on screen.


def options_window():
    options_window = Tk()
    options_window.title("Advanced Options")
    options_window.minsize(250, 200)
    options_window.grid_columnconfigure(0,weight=1)
    options_window.grid_rowconfigure(0,weight=1)
    ow_welcome_text = Label(options_window, text="Here you can change options for the conversion.\nYou have 6 options to chose from:")
    ow_welcome_text.grid(columnspan=2, sticky="NESW")
    options_window.mainloop()


# Creates options window with various widgets and runs it.


def button_mp4():
    file_type_set("mp4")
    convert_file()


# Starts file conversions for the SWF file type.


def button_wmv():
    file_type_set("wmv")
    convert_file()


# Starts file conversions for the SWF file type.


def button_swf():
    file_type_set("swf")
    convert_file()


# Starts file conversions for the SWF file type.


init_script()
main_window()

# Starts the main window.
