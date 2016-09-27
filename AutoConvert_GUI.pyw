from os import path, chdir, listdir, makedirs, remove
from subprocess import call
from platform import system
from webbrowser import open_new_tab
from tkinter import *
from tkinter import messagebox, filedialog, ttk


# Variables naming convention:
# Variables for the various windows are xw_, where "x" is the first letter of the description of the window.
# Variables for the MP4 section are prefixed with m_
# Variables for the WMV section are prefixed with w_
# Variables for the SWF section are prefixed with s_

class render_window:
    def __init__(self, height, width, window_title):
        self.root_window = Tk()
        w = width
        h = height
        ws = self.root_window.winfo_screenwidth() # width of the screen
        hs = self.root_window.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root_window.title(window_title)
        self.root_window.minsize(width, height)
        self.root_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.radio_button_var = StringVar()

    def new_button(self, button_text, button_command="", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.button = ttk.Button(self.root_window, text=button_text, command=button_command)
        self.button.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_label(self, label_text, text_alignment="center", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.label = ttk.Label(self.root_window, text=label_text, anchor=text_alignment)
        self.label.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_progress_bar(self, pg_length=250, pg_mode="determinate", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.progress_bar = ttk.Progressbar(self.root_window, length=pg_length, mode=pg_mode)
        self.progress_bar.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_radio_button(self, widget_text="Radio Button", radio_value="Radio Btn", radio_command="", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.radio_button = ttk.Radiobutton(self.root_window, text=widget_text, variable=self.radio_button_var, value=radio_value, command=radio_command)
        self.radio_button.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_text_box(self, grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.text_box = ttk.Entry(self.root_window, textvariable=self.text_box_var)
        self.text_box.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def responsive_grid(self, row_responsive=0, column_responsive=0, row_weight_num=1, column_weight_num=1):
        self.root_window.grid_columnconfigure(column_responsive, weight=column_weight_num)
        self.root_window.grid_rowconfigure(row_responsive, weight=row_weight_num)


# Creates a framework to easily create new windows and populate them with widgets.


class init_system:
    def __init__(self):
        self.init_vars = {"path_to_file": path.abspath(__file__),
        "nbr_path": os.path.normpath("C:/ProgramData/WebEx/WebEx/500/nbrplay.exe"),
        "file_type": "mp4",
        "showui": 0,
        "need_ui_section": True,
        "width": 1920,
        "height": 1080,
        "m_ui_chat": 1,
        "m_ui_qa": 1,
        "m_ui_largeroutline": 1,
        "m_framerate": 5,
        "s_console_pcaudio": 0,
        "s_framerate": 10,
        "w_console_pcaudio": 0,
        "w_ui_chat": 1,
        "w_ui_video": 1,
        "w_ui_largeroutline": 1,
        "w_videocodec": "Windows Media Video 9",
        "w_audiocodec": "Windows Media Audio 9.2 Lossless",
        "w_videoformat": "default",
        "w_audioformat": "default",
        "w_videokeyframes": 4,
        "w_maxstream": 1000}
        self.init_vars["directory_name"] = path.dirname(self.init_vars["path_to_file"])
        self.init_vars["input_file_dir"] = path.dirname(self.init_vars["path_to_file"])
        self.init_vars["output_file_dir"] = path.dirname(self.init_vars["path_to_file"]) + "\\Converted"
        chdir(self.init_vars["directory_name"])
        self.check_os()
        self.locate_nbr()
    # Sets up the initial variables and checks for system compatibility


    def check_os(self):
        if system() != "Windows":
            messagebox.showerror("Compatibility Error", "Please use Windows for file conversions.\nOther OSs are currently not supported :-(")
            exit()
    # Checks the operating system to see if it is compatible. If not, it displays an error and quits the program.


    def locate_nbr(self):
        if not self.check_file_existance(self.init_vars["nbr_path"]):
            download_nbr = messagebox.askquestion("Download dependency?", "The system could not find the NBR player.\nWould you like to download it?")
            if download_nbr == "yes":
                open_new_tab("www.webex.com/play-webex-recording.html")
                exit()
            elif download_nbr == "no":
                nbr_already_installed = messagebox.askquestion("Maybe we missed it...", "Do you have the NBR player installed already?")
                if nbr_already_installed == "yes":
                    custom_nbr_location()
                    locate_nbr()
                else:
                    messagebox.showerror("Cannot continue!", "This script requires the Network Broadcast Recording player to operate.\nPlease have it installed for the next time you run this script.")
                    exit()
        else:
            return True
        # Checks if the NBR is present. If not it prompts the user to download it. If the user declines then it prompts if it is installed in a different location.
        # If yes then it executes the custom_nbr_location function. If not, the program displays an error and quits after the error is acknowledged.


    def check_file_existance(self, file_path):
        result = path.exists(file_path)
        return result
    # Checks the given file path to see if the file exists and returns true or false.


    def custom_nbr_location(self):
        messagebox.showinfo("Find the player...", message="Please browse to the folder that houses the nbrplay.exe program.")
        self.init_vars["nbr_path"] = filedialog.askdirectory(mustexist=True)
    # Sets the nbr_path variable to the user provided path. The folder must exist to be accepted.


    def check_folder(self):
        error_num = 0
        if not path.exists(self.init_vars["input_file_dir"]):
            error_num = error_num + 5
        elif not path.exists(self.init_vars["output_file_dir"]):
            error_num = error_num + 4
        return error_num
        # Check is the source directory exists and if it does not then displays an error and goes back to the main menu.
        # Also checks if the output directory exists and if it does not it creates it.
        # 5 = input
        # 4 = output
        # 9 = input and output


# Initializes the script with default values and changes to the directory where the script is located.


def progress_bar_window_system():
    global pg_window
    global pg_progress
    pg_window = render_window(50, 250, "Conversion Progress")
    pg_window.new_progress_bar()
    pg_progress = pg_window.progress_bar
    pg_window.new_label("Converting Files", grid_row=1)
    pg_window.root_window.after(1, func=convert_file)
    main_window.root_window.withdraw()
    pg_window.root_window.mainloop()


# Creates the progress bar window, complete with the progress bar and supporting text. Centered on the screen.


def convert_file():
    global pg_window
    global pg_progress
    global main_window
    pg_window.root_window.update()
    if vars_system.check_folder() == 5:
        pg_window.root_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF input dir is invalid, please check that it exists.")
        main_window.root_window.deiconify()
        return
    elif vars_system.check_folder() == 4:
        pg_window.root_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF output dir is invalid, please check that it exists.")
        main_window.root_window.deiconify()
        return
    elif vars_system.check_folder() == 9:
        pg_window.root_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF input and output dirs are invalid, please check that they exist.")
        main_window.root_window.deiconify()
        return
    cfg_counter = 0
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            remove(file)
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "arf":
            create_configs(file)
            cfg_counter += 1
    pg_progress.config(maximum=cfg_counter)
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            execute_nbr_conversion(vars_system.init_vars["input_file_dir"] + "\\" + file)
            cfg_counter -= 1
            pg_progress.config(value=cfg_counter)
            pg_window.root_window.update()
            remove(file)
    pg_window.root_window.destroy()
    main_window.root_window.deiconify()
    messagebox.showinfo(title="Conversion complete!", message="File conversion(s) are complete!")


# The conversion process checks to make sure the dependencies are in place, if so then it creates the configs, enumerates the amount of files, sends that to the progress bar,
# executes the file conversion, updates the progress bar and repeats until there are no more config files. After there are no more config files, it removes the progress bar window,
# shows the main window and throws a completed message.


def create_configs(fname):
    with open(fname[:-3] + "cfg", "a") as config_file:
        config_file.write("[Console]")
        config_file.write("\ninputfile=%s" % vars_system.init_vars["input_file_dir"] + "\\" + fname)
        config_file.write("\nmedia=%s" % vars_system.init_vars["file_type"].upper())
        config_file.write("\nshowui=%s" % vars_system.init_vars["showui"])
        if vars_system.init_vars["file_type"].lower() == "swf":
            config_file.write("\nPCAudio=%s" % vars_system.init_vars["s_console_pcaudio"])
        elif vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nPCAudio=%s" % vars_system.init_vars["w_console_pcaudio"])
        if vars_system.init_vars["need_ui_section"]:
            config_file.write("\n[UI]")
        if vars_system.init_vars["file_type"] == "mp4":
            config_file.write("\nchat=%s" % vars_system.init_vars["m_ui_chat"])
        elif vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nchat=%s" % vars_system.init_vars["w_ui_chat"])
        if vars_system.init_vars["file_type"].lower() == "mp4":
            config_file.write("\nqa=%s" % vars_system.init_vars["m_ui_qa"])
        elif vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nvideo=%s" % vars_system.init_vars["w_ui_video"])
        if vars_system.init_vars["file_type"].lower() == "mp4":
            config_file.write("\nlargeroutline=%s" % vars_system.init_vars["m_ui_largeroutline"])
        elif vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nlargeroutline=%s" % vars_system.init_vars["w_ui_largeroutline"])
        config_file.write("\n[%s]" % vars_system.init_vars["file_type"].upper())
        config_file.write("\noutputfile=%s" % vars_system.init_vars["output_file_dir"] + "\\" + fname[:-3] + vars_system.init_vars["file_type"].lower())
        config_file.write("\nwidth=%s" % vars_system.init_vars["width"])
        config_file.write("\nheight=%s" % vars_system.init_vars["height"])
        if vars_system.init_vars["file_type"].lower() == "mp4":
            config_file.write("\nframerate=%s" % vars_system.init_vars["m_framerate"])
        elif vars_system.init_vars["file_type"] == "wmv":
            config_file.write("\nvideocodec=%s" % vars_system.init_vars["w_videocodec"])
        elif vars_system.init_vars["file_type"].lower() == "swf":
            config_file.write("\nframerate=%s" % vars_system.init_vars["s_framerate"])
        if vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\naudiocodec=%s" % vars_system.init_vars["w_audiocodec"])
        if vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nvideoformat=%s" % vars_system.init_vars["w_videoformat"])
        if vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\naudioformat=%s" % vars_system.init_vars["w_audioformat"])
        if vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nvideokeyframes=%s" % vars_system.init_vars["w_videokeyframes"])
        if vars_system.init_vars["file_type"].lower() == "wmv":
            config_file.write("\nmaxstream=%s" % vars_system.init_vars["w_maxstream"])


# Creates configuration files for the nbrplayer to use to convert the files.


def execute_nbr_conversion(cfg_name):
    call(vars_system.init_vars["nbr_path"] + " -Convert" + ' "' + cfg_name + '"')


# Executes the nbr executable with the path to the generated cfg file.


def main_window_create():
    global main_window
    main_window = render_window(200, 250, "ARF Auto Converter")

    main_window.new_button("Convert to MP4", button_mp4, 1)
    main_window.new_button("Convert to WMV", button_wmv, 2)
    main_window.new_button("Convert to SWF", button_swf, 3)
    main_window.new_button("Help", help_system, 2, 1)
    main_window.new_button("Options", options_window_create, 1, 1)
    main_window.new_button("Exit", exit, 3, 1)
    main_window.new_label("Welcome to the ARF Auto Converter!", grid_columnspan=2)

    main_window.root_window.mainloop()


# Uses the render_window framework to create a window and populate it with widgets.


def options_window_create():
    global options_window
    main_window.root_window.destroy()

    options_window = render_window(200, 500, "Converter Options")

    options_window.new_label("You can only currently restore the default settings. More to come soon!", grid_columnspan=2)
    options_window.new_button("Restore Defaults", vars_system.__init__, 1, 1)
    options_window.new_button("Back to Main Window", button_back_to_mw, 1)

    options_window.root_window.mainloop()


# Uses the render_window framework to create a window and populate it with widgets.


def help_system():
    messagebox.showinfo("Coming Soon!", "The help system will be present in a future version.")


# Displays an info box that says "coming soon"


def button_mp4():
    vars_system.init_vars["file_type"] = "mp4"
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_wmv():
    vars_system.init_vars["file_type"] = "wmv"
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_swf():
    vars_system.init_vars["file_type"] = "swf"
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_back_to_mw():
    options_window.root_window.destroy()
    main_window_create()


# Stops the options window and opens the main window.


vars_system = init_system()
main_window_create()

# Starts the main window.
