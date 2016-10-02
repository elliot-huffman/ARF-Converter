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
#seperator


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
    def save_freeform_value(self):
        if self.change_var_window_values["is_number"] and vars_system.int_able_check(self.text_box.get()):
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.text_box.get()
            messagebox.showinfo("Success", "The custom value has been saved!")
            main_window.root_window.deiconify()
            self.root_window.destroy()
        elif self.change_var_window_values["is_number"] and not vars_system.int_able_check(self.text_box.get()):
            messagebox.showerror("Error", "Entry has to be a number above zero.")
        elif not self.change_var_window_values["is_number"]:
            vars_system.init_vars[self.change_var_window_values["var_to_change"]] = self.text_box.get()
            messagebox.showinfo("Success", "The custom value has been saved!")
            main_window.root_window.deiconify()
            self.root_window.destroy()

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
        main_window.root_window.deiconify()
        self.root_window.destroy()


        # seperator


    def toggle_var(self, var_name="some_var", custom_data=False, custom_data_enable="placeholder", custom_data_disable="placeholder"):
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
        self.top_level_window.destroy()
        main_window.root_window.deiconify()


    def create_change_var_window(self):
        self.new_label(self.change_var_window_values["line_one"], grid_columnspan=2)
        self.new_label(self.change_var_window_values["line_two"], grid_row=1, grid_columnspan=2)
        if self.change_var_window_values["toggle"]:
            self.toggle_var(self.change_var_window_values["var_to_change"], self.change_var_window_values["Custom_Data_Bool"], self.change_var_window_values["Custom_Enable"], self.change_var_window_values["Custom_Disable"])
            self.new_button("Cancel", self.root_window.destroy, grid_row=2, grid_column=1)
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
            self.new_button("Cancle", self.top_level_window.destroy, grid_row=grid_placement, grid_column=1)
            grid_placement -= 1
            self.new_button("Save", self.save_radio_var, grid_row=grid_placement, grid_column=1)
            # Radio Requires:
            # "radio_list" "var_to_change"
        elif self.change_var_window_values["free_form"]:
            self.new_text_box(grid_row=2, grid_columnspan=2)
            self.new_button("Save Value", self.save_freeform_value, 3)
            self.new_button("Cancel", self.root_window.destroy, grid_row=3, grid_column=1)
            # Free_form requires:
            # "var_to_change" and "is_number"
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


def freeform_example():
    freeform = change_var_window(200, 250, "Change width")
    freeform.change_var_window_values.update({"free_form": True, "toggle": False, "radio": False, "var_to_change": "width", "line_one": "Current value of width:", "line_two": vars_system.init_vars["width"], "is_number": True})
    main_window.root_window.withdraw()
    freeform.create_change_var_window()
    #remember to include Line_One and Line_Two!!!

def example_toggle():
    toggle = change_var_window(200, 250, "Toggle ShowUI")
    toggle.change_var_window_values.update({"toggle": True, "var_to_change": "showui", "line_one": "Current value of ShowUI:", "line_two": vars_system.init_vars["showui"]})
    main_window.root_window.withdraw()
    toggle.create_change_var_window()

def radio_example():
    main_window.new_top_level(200, 250, "Radio")
    main_window.master_dictionary["top_level_window"] = True
    main_window.change_var_window_values.update({"free_form": False, "toggle": False, "radio": True, "var_to_change": "w_audiocodec", "line_one": "Current value of w_audiocodec:", "line_two": vars_system.init_vars["w_audiocodec"]})
    main_window.change_var_window_values.update({"radio_list": [("Windows Media Audio 9.2", "Windows Media Audio 9.2"), ("Windows Media Audio 9.2 Lossless", "Windows Media Audio 9.2 Lossless"), ("Windows Media Audio 10 Professional", "Windows Media Audio 10 Professional")]})
    main_window.create_change_var_window()


#seperator

vars_system = init_system()

main_window = change_var_window(200, 250, "Main Window")
main_window.new_button("Freeform Edit", freeform_example, 1, grid_columnspan=2)
main_window.new_button("Toggle Var", example_toggle)
main_window.new_button("Radio Var", radio_example, grid_column=1)

main_window.root_window.mainloop()
