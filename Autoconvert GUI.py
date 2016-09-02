from tkinter import *

main_window = Tk()

main_window.title("ARF Auto Converter")
main_window.minsize(250, 200)


mw_top_frame = Frame(main_window)
mw_left_frame = Frame(main_window)
mw_right_frame = Frame(main_window)
mw_top_frame.pack(side=TOP)
mw_left_frame.pack(side=LEFT)
mw_right_frame.pack(side=RIGHT)


# Creates a responsive framework to place widgets on


mw_welcome_text = Label(mw_top_frame, text="Welcome to the ARF auto converter!")
mw_MP4_button = Button(mw_left_frame, text="Convert to MP4", fg="green")
mw_WMV_button = Button(mw_left_frame, text="Convert to WMV")
mw_SWF_button = Button(mw_left_frame, text="Convert to SWF", fg="red")
mw_options_button = Button(mw_right_frame, text="Advanced Options")
mw_exit_button = Button(mw_right_frame, text="Exit")


mw_welcome_text.grid(columnspan=2, pady=25)
mw_MP4_button.grid()
mw_WMV_button.grid(row=1)
mw_SWF_button.grid(row=2)
mw_options_button.grid()
mw_exit_button.grid(row=1)


main_window.mainloop()


# Create the main window and populate it iwth various buttons and labels.


# options_window = Tk()


# Creates the window that will contain all of the widgets


options_window.title("Advanced Options")
options_window.minsize(200, 200)


# Sets the window manager options


ow_welcome_text = Label(options_window, text="Here you can change options for the conversion.\nYou have 6 options to chose from:")


# Creates the widgets


ow_welcome_text.grid(columnspan=2, sticky=N)


# Places the widgets


# options_window.mainloop()


# Executes the window and keeps it untill the interupted.