from os import path, chdir
from platform import system
from webbrowser import open_new_tab
from tkinter import *
from tkinter import messagebox, filedialog, ttk

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
        self.text_box_var = StringVar() 

    def is_number(self, input_item):
        if input_item.get().isdigit():
            return True
        else:
            return False

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

    def responsive_grid(self, row_responsive=0, column_responsive=0, row_weight_num=1, column_weight_num=1):
        self.root_window.grid_columnconfigure(column_responsive, weight=column_weight_num)
        self.root_window.grid_rowconfigure(row_responsive, weight=row_weight_num)
    
    def new_radio_button(self, widget_text="Radio Button", radio_value="Radio Btn", radio_command="", grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.radio_button = ttk.Radiobutton(self.root_window, text=widget_text, variable=self.radio_button_var, value=radio_value, command=radio_command)
        self.radio_button.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)
    
    def new_text_box(self, grid_row=0, grid_column=0, grid_sticky="NESW", grid_columnspan=1, grid_rowspan=1):
        self.text_box = ttk.Entry(self.root_window, textvariable=self.text_box_var)
        self.text_box.grid(row=grid_row, column=grid_column, sticky=grid_sticky, columnspan=grid_columnspan, rowspan=grid_rowspan)
        self.responsive_grid(grid_row, grid_column)
#seperator


class change_var_window(render_window):

    data_to_change = {}

    def change_data(self):
        if self.data_to_change["bool_value"]:
            if self.data_to_change["data_type"].lower() == "num":
                vars_system.init_vars[self.data_to_change["var_name"]] =  1
            elif self.data_to_change["data_type"].lower() == "bool":
                vars_system.init_vars[self.data_to_change["var_name"]] = True
            elif self.data_to_change["data_type"].lower() == "custom":
                vars_system.init_vars[self.data_to_change["var_name"]] = self.data_to_change["custom_data_enable"]
        elif not self.data_to_change["bool_value"]:
            if self.data_to_change["data_type"].lower() == "num":
                vars_system.init_vars[self.data_to_change["var_name"]] =  0
            elif self.data_to_change["data_type"].lower() == "bool":
                vars_system.init_vars[self.data_to_change["var_name"]] = False
            elif self.data_to_change["data_type"].lower() == "custom":
                vars_system.init_vars[self.data_to_change["var_name"]] = self.data_to_change["custom_data_disable"]
        else:
            messagebox.showerror("Error!","An error has occured at change_data!")
        messagebox.showinfo("Success", "The option has been changed!")
        messagebox.showinfo("debug", vars_system.init_vars[self.data_to_change["var_name"]])
        self.root_window.destroy()

    def toggle_var(self, line_one="line one here...", line_two="line two here...", var_name="some_var", custom_data=False, custom_data_enable="placeholder", custom_data_disable="placeholder"):
        self.new_label(line_one, grid_columnspan=2)
        self.new_label(line_two, grid_row=1, grid_columnspan=2)
        self.new_button("Cancel", self.root_window.destroy, grid_row=2, grid_column=1)
        self.data_to_change["var_name"] = var_name
        if custom_data:
            self.data_to_change["data_type"] = "custom"
            self.data_to_change["custom_data_enable"] = custom_data_enable
            self.data_to_change["custom_data_disable"] = custom_data_disable
            if vars_system.init_vars[self.data_to_change["var_name"]] == custom_data_enable:
                self.data_to_change["bool_value"] = False
            elif vars_system.init_vars[self.data_to_change["var_name"]] == custom_data_disable:
                self.data_to_change["bool_value"] = True
            self.new_button("Toggle", self.change_data, 2)
        elif not custom_data:
            if vars_system.init_vars[self.data_to_change["var_name"]] == 0:
                self.data_to_change["data_type"] = "num"
                self.data_to_change["bool_value"] = True
                self.new_button("Enable", self.change_data, 2)
            elif vars_system.init_vars[self.data_to_change["var_name"]] == 1:
                self.data_to_change["data_type"] = "num"
                self.data_to_change["bool_value"] = False
                self.new_button("Disable", self.change_data, 2)
            else:
                messagebox.showerror("Error!","An error has occured at toggle_var!")


    def radio_var(self):
        pass

    def type_var(self):
        pass

# seperator

class init_system:
    def __init__(self):
        self.init_vars = {"path_to_file": path.abspath(__file__),
        "nbr_path": "C:\ProgramData\WebEx\WebEx\\500\\nbrplay.exe",
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


def print_stuff():
    if radio_window.text_box_var.get().isdigit():
        print(radio_window.text_box_var.get())
    else:
        messagebox.showerror("Cannot continue!", "Non Valid input detected!\nTry again.")

#wmv_change_videocodec = change_var_window(200, 250, "Change Video Codec")
#wmv_change_videocodec.toggle_var()
vars_system = init_system()

wmv_change_videocodec = change_var_window(200, 250, "Need UI")
wmv_change_videocodec.toggle_var("Change the UI Print.\nThe current setting is:", vars_system.init_vars["need_ui_section"], "need_ui_section")
wmv_change_videocodec.root_window.mainloop()
# 



#def wmv_change_videocodec():
#    print("The WMV video codex is currently set to: %s" % vars_system.w_videocodec)
#    print("There are 2 options for this setting:\n1. Windows Media Video 9\n2. Windows Media Video 9 Screen")
#    print("\nLeave the field blank to do nothing")
#    me_wmv_videocodec = int(input("\nPlease enter 1 or 2 then press Enter/Return: "))
#    if me_wmv_videocodec == int:
#        if me_wmv_videocodec == 1:
#            vars_system.w_videocodec = "Windows Media Video"
#        elif me_wmv_videocodec == 2:
#            vars_system.w_videocodec = "Windows Media Video 9 Screen"
#        clear_screen()
#        print("The video codex is now set to: %s" % vars_system.w_videocodec)
#        input("Press Enter/Return to continue...")
#    wmv_options_menu()