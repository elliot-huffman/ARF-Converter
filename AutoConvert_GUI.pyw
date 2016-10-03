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
        self.master_dictionary = {"radio_ctrl": StringVar(), "top_level_window": False}

    def new_top_level(self, height, width, window_title):
        self.top_level_window = Toplevel()
        w = width
        h = height
        ws = self.top_level_window.winfo_screenwidth() # width of the screen
        hs = self.top_level_window.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.top_level_window.title(window_title)
        self.top_level_window.minsize(width, height)
        self.top_level_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def new_button(self, button_text, button_command="", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        if self.master_dictionary["top_level_window"]:
            self.button = ttk.Button(self.top_level_window, text=button_text, command=button_command)
        elif not self.master_dictionary["top_level_window"]:
            self.button = ttk.Button(self.root_window, text=button_text, command=button_command)
        self.button.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_label(self, label_text, text_alignment="center", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        if self.master_dictionary["top_level_window"]:
            self.label = ttk.Label(self.top_level_window, text=label_text, anchor=text_alignment)
        elif not self.master_dictionary["top_level_window"]:
            self.label = ttk.Label(self.root_window, text=label_text, anchor=text_alignment)
        self.label.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_progress_bar(self, pg_length=250, pg_mode="determinate", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        if self.master_dictionary["top_level_window"]:
            self.progress_bar = ttk.Progressbar(self.top_level_window, length=pg_length, mode=pg_mode)
        elif not self.master_dictionary["top_level_window"]:
            self.progress_bar = ttk.Progressbar(self.root_window, length=pg_length, mode=pg_mode)
        self.progress_bar.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def responsive_grid(self, row_responsive=0, column_responsive=0, row_weight_num=1, column_weight_num=1):
        if self.master_dictionary["top_level_window"]:
            self.top_level_window.grid_columnconfigure(column_responsive, weight=column_weight_num)
            self.top_level_window.grid_rowconfigure(row_responsive, weight=row_weight_num)
        elif not self.master_dictionary["top_level_window"]:
            self.root_window.grid_columnconfigure(column_responsive, weight=column_weight_num)
            self.root_window.grid_rowconfigure(row_responsive, weight=row_weight_num)

    def new_radio_button(self, widget_text="Radio Button", radio_value="Radio Btn", radio_command="", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        if self.master_dictionary["top_level_window"]:
            self.radio_button = ttk.Radiobutton(self.top_level_window, text=widget_text, variable=self.master_dictionary["radio_ctrl"], value=radio_value, command=radio_command)
        elif not self.master_dictionary["top_level_window"]:
            self.radio_button = ttk.Radiobutton(self.root_window, text=widget_text, variable=self.master_dictionary["radio_ctrl"], value=radio_value, command=radio_command)
        self.radio_button.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)

    def new_text_box(self, grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        if self.master_dictionary["top_level_window"]:
            self.text_box = ttk.Entry(self.top_level_window)
        elif not self.master_dictionary["top_level_window"]:
            self.text_box = ttk.Entry(self.root_window)
        self.text_box.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)


# Creates a framework to easily create new windows and populate them with widgets.


class change_var_window(render_window):

    change_var_window_values = {"example_data_below": "Check it out!",
                                "var_to_change": "show_ui",
                                "toggle": False,
                                "radio": False,
                                "free_form":False,
                                "line_one": "Current value of:",
                                "line_two": "some varible name here passwed with a dicrionary",
                                "Custom_Data_Bool": False,
                                "Custom_Disable": "Enable me",
                                "Custom_Enable": "Disable me",
                                "radio_list": [("Radio Button 1", "btn_1"), ("Radio Button 2", "btn_2"), ("Radio Button 3", "btn_3")],
                                "is_number": True
                               }
    def browse_for_data(self):
        if self.change_var_window_values["browse_for_dir"]:
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = path.normpath(filedialog.askdirectory(mustexist=True))
        elif not self.change_var_window_values["browse_for_dir"]:
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = path.normpath(filedialog.askopenfile())
        self.close_window()
    def close_window(self):
        if self.master_dictionary["top_level_window"]:
            self.top_level_window.destroy()
            self.root_window.deiconify()
        elif not self.master_dictionary["top_level_window"]:
            self.root_window.destroy()
    def save_freeform_value(self):
        if self.change_var_window_values["is_number"] and vars_system.int_able_check(self.text_box.get()):
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.text_box.get()
            messagebox.showinfo("Success", "The custom value has been saved!")
            self.close_window()
        elif self.change_var_window_values["is_number"] and not vars_system.int_able_check(self.text_box.get()):
            messagebox.showerror("Error", "Entry has to be a number above zero.")
        elif not self.change_var_window_values["is_number"]:
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.text_box.get()
            messagebox.showinfo("Success", "The custom value has been saved!")
            self.close_window()

    def change_bool_data(self):
        if self.change_var_window_values["bool_value"]:
            if self.change_var_window_values["data_type"].lower() == "num":
                vars_system.init_vars[self.change_var_window_values["var_to_change"]] = 1
            elif self.change_var_window_values["data_type"].lower() == "custom":
                vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.change_var_window_values["custom_data_enable"]
        elif not self.change_var_window_values["bool_value"]:
            if self.change_var_window_values["data_type"].lower() == "num":
                vars_system.init_vars[self.change_var_window_values["var_to_change"]] = 0
            elif self.change_var_window_values["data_type"].lower() == "custom":
                vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.change_var_window_values["custom_data_disable"]
        else:
            messagebox.showerror("Error!", "An error has occured at change_data!")
        messagebox.showinfo("Success", "The toggle has been changed!")
        self.close_window()


        # seperator


    def toggle_var(self, custom_data=False, custom_data_enable="placeholder", custom_data_disable="placeholder"):
        if custom_data:
            self.change_var_window_values["data_type"] = "custom"
            self.change_var_window_values["custom_data_enable"] = custom_data_enable
            self.change_var_window_values["custom_data_disable"] = custom_data_disable
            if vars_system.init_vars[self.change_var_window_values["var_to_change"]] == custom_data_enable:
                self.change_var_window_values["bool_value"] = False
            elif vars_system.init_vars[self.change_var_window_values["var_to_change"]] == custom_data_disable:
                self.change_var_window_values["bool_value"] = True
            self.new_button("Toggle", self.change_bool_data, 2)
        elif not custom_data:
            if vars_system.init_vars[self.change_var_window_values["var_to_change"]] == 0:
                self.change_var_window_values["data_type"] = "num"
                self.change_var_window_values["bool_value"] = True
                self.new_button("Enable", self.change_bool_data, 2)
            elif vars_system.init_vars[self.change_var_window_values["var_to_change"]] == 1:
                self.change_var_window_values["data_type"] = "num"
                self.change_var_window_values["bool_value"] = False
                self.new_button("Disable", self.change_bool_data, 2)
            else:
                print("Toggle var has executed unsuccessfilly")
                print(self.change_var_window_values)
                main_window.root_window.deiconify()


    def save_radio_var(self):
        vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.master_dictionary["radio_ctrl"].get()
        messagebox.showinfo("debug", self.master_dictionary["radio_ctrl"].get())
        self.close_window()


    def create_change_var_window(self):
        self.root_window.withdraw()
        self.new_label(self.change_var_window_values["line_one"], grid_columnspan=2)
        self.new_label(self.change_var_window_values["line_two"], grid_row=1, grid_columnspan=2)
        if self.change_var_window_values["toggle"]:
            self.toggle_var(self.change_var_window_values["Custom_Data_Bool"], self.change_var_window_values["Custom_Enable"], self.change_var_window_values["Custom_Disable"])
            self.new_button("Cancel", self.close_window, grid_row=2, grid_column=1)
            # Toggle requires:
            # "var_to_change", "Custom_Data_Bool", "Custom_Enable", "Custom_Disable"
        elif self.change_var_window_values["radio"]:
            grid_placement = 2
            self.master_dictionary["radio_ctrl"] = StringVar()
            #self.master_dictionary["radio_ctrl"].set(vars_system.init_vars[self.change_var_window_values["var_to_change"]])
            for radio_name, value in self.change_var_window_values["radio_list"]:
                self.new_radio_button(widget_text=radio_name, radio_value=value, grid_row=grid_placement)
                grid_placement += 1
            grid_placement -= 1
            self.new_button("Cancle", self.close_window, grid_row=grid_placement, grid_column=1)
            grid_placement -= 1
            self.new_button("Save", self.save_radio_var, grid_row=grid_placement, grid_column=1)
            # Radio Requires:
            # "radio_list" "var_to_change"
        elif self.change_var_window_values["free_form"]:
            self.new_text_box(grid_row=2, grid_columnspan=2)
            self.new_button("Save Value", self.save_freeform_value, 3)
            self.new_button("Cancel", self.close_window, grid_row=3, grid_column=1)
            # Free_form requires:
            # "var_to_change" and "is_number"
        elif self.change_var_window_values["browse_data"]:
            self.new_button("Browse", self.browse_for_data, grid_row=2)
            self.new_button("Cancel", self.close_window, grid_row=2, grid_column=1)
            # browse_data requires:
            # "var_to_change" and "browse_for_dir""
        if self.master_dictionary["top_level_window"]:
            self.top_level_window.mainloop()
        elif not self.master_dictionary["top_level_window"]:
            self.root_window.mainloop()

# seperator

class init_system:
    def __init__(self):
        self.init_vars = {
            "path_to_file": path.abspath(__file__),
            "nbr_path": path.normpath("C:/ProgramData/WebEx/WebEx/500/nbrplay.exe"),
            "file_type": "mp4",
            "showui": 0,
            "need_ui_section": False,
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
                    self.custom_nbr_location()
                    self.locate_nbr()
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


    def int_able_check(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False


# Initializes the script with default values and changes to the directory where the script is located.


def progress_bar_window_system(file_type):
    global pg_window
    global pg_progress
    vars_system.init_vars["file_type"] = file_type.lower()
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


# Uses the render_window framework to create a window and populate it with widgets.


def options_window_create():
    main_window.root_window.withdraw()
    main_window.new_top_level(200, 250, "Converter Options")
    main_window.master_dictionary["top_level_window"] = True
    main_window.new_label("Below are the available options categories:", grid_columnspan=2)
    main_window.new_button("Global Options", global_options_window, grid_row=1)
    main_window.new_button("WMV Options", wmv_options_window,grid_row=1, grid_column=1)
    main_window.new_button("MP4 Options", mp4_options_window, grid_row=2)
    main_window.new_button("SWF Options", swf_options_window, grid_row=2, grid_column=1)
    main_window.new_button("Restore Defaults", vars_system.__init__, grid_row=3)
    main_window.new_button("Back to Main Window", main_window.close_window, grid_row=3, grid_column=1)
    main_window.top_level_window.mainloop()


# Uses the render_window framework to create a window and populate it with widgets.

def global_options_window():
    main_window.top_level_window.withdraw()
    main_window.new_top_level(200, 250, "Global options")
    main_window.new_label("Global options available:", grid_columnspan=2)
    main_window.new_button("Change Input Dir", change_input_dir, 1)
    main_window.new_button("Change Output Dir", change_output_dir, 1, 1)
    main_window.new_button("Change Width", change_width, 2)
    main_window.new_button("Change Heigth", change_height, 2, 1)
    main_window.new_button("Toggle ShowUI", toggle_showui, 3)
    main_window.new_button("Go back", main_window.close_window, 3, 1)
    main_window.top_level_window.mainloop()

def wmv_options_window():
    main_window.top_level_window.withdraw()
    main_window.new_top_level(200, 250, "WMV options")
    main_window.new_label("Global options available:", grid_columnspan=2)
    main_window.new_button("Change Input Dir", toggle_showui, 1)
    main_window.new_button("Change Output Dir", toggle_showui, 1, 1)
    main_window.new_button("Change Width", toggle_showui, 2)
    main_window.new_button("Change Heigth", toggle_showui, 2, 1)
    main_window.new_button("Toggle ShowUI", toggle_showui, 3)
    main_window.new_button("Go back", main_window.close_window, 3, 1)
    main_window.top_level_window.mainloop()

def mp4_options_window():
    main_window.top_level_window.withdraw()
    main_window.new_top_level(200, 250, "MP4 options")
    main_window.new_label("Global options available:", grid_columnspan=2)
    main_window.new_button("Change Input Dir", toggle_showui, 1)
    main_window.new_button("Change Output Dir", toggle_showui, 1, 1)
    main_window.new_button("Change Width", toggle_showui, 2)
    main_window.new_button("Change Frame Rate", toggle_showui, 2, 1)
    main_window.new_button("Go back", main_window.close_window, 3, 1)
    main_window.top_level_window.mainloop()

def swf_options_window():
    main_window.top_level_window.withdraw()
    main_window.new_top_level(200, 250, "SWF options")
    main_window.new_label("Global options available:", grid_columnspan=2)
    main_window.new_button("Change Input Dir", toggle_showui, 1)
    main_window.new_button("Change Output Dir", toggle_showui, 1, 1)
    main_window.new_button("Change Width", toggle_showui, 2)
    main_window.new_button("Change Heigth", toggle_showui, 2, 1)
    main_window.new_button("Toggle ShowUI", toggle_showui, 3)
    main_window.new_button("Go back", main_window.close_window, 3, 1)
    main_window.top_level_window.mainloop()

def toggle_showui():
    main_window.new_top_level(200, 250, "Toggle ShowUI")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"toggle": True, "var_to_change": "showui", "line_one": "Current value of ShowUI:", "line_two": vars_system.init_vars["showui"]})
    main_window.create_change_var_window()

def change_width():
    main_window.new_top_level(200, 250, "Change width")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"free_form": True, "toggle": False, "radio": False, "var_to_change": "width", "line_one": "Current value of width:", "line_two": vars_system.init_vars["width"], "is_number": True})
    main_window.create_change_var_window()

def change_height():
    main_window.new_top_level(200, 250, "Change height")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"free_form": True, "toggle": False, "radio": False, "var_to_change": "height", "line_one": "Current value of height:", "line_two": vars_system.init_vars["height"], "is_number": True})
    main_window.create_change_var_window()

def change_output_dir():
    main_window.new_top_level(200, 250, "Browse for output dir")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"browse_data": True, "browse_for_dir": True, "free_form": False, "toggle": False, "radio": False, "var_to_change": "output_file_dir", "line_one": "Current value of output_file_dir:", "line_two": vars_system.init_vars["output_file_dir"]})
    main_window.create_change_var_window()

def change_input_dir():
    main_window.new_top_level(200, 250, "Browse for output dir")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"browse_data": True, "browse_for_dir": True, "free_form": False, "toggle": False, "radio": False, "var_to_change": "input_file_dir", "line_one": "Current value of input_file_dir:", "line_two": vars_system.init_vars["input_file_dir"]})
    main_window.create_change_var_window()

def help_system():
    messagebox.showinfo("Coming Soon!", "The help system will be present in a future version.")


# Displays an info box that says "coming soon"


vars_system = init_system()

main_window = change_var_window(200, 250, "ARF Auto Converter")

main_window.new_button("Convert to MP4", lambda: progress_bar_window_system("mp4"), 1)
main_window.new_button("Convert to WMV", lambda: progress_bar_window_system("wmv"), 2)
main_window.new_button("Convert to SWF", lambda: progress_bar_window_system("swf"), 3)
main_window.new_button("Help", help_system, 2, 1)
main_window.new_button("Options", options_window_create, 1, 1)
main_window.new_button("Exit", exit, 3, 1)
main_window.new_label("Welcome to the ARF Auto Converter!", grid_columnspan=2)

main_window.root_window.mainloop()

# Starts the main window.
