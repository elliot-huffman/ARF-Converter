from os import path, chdir, listdir, makedirs, remove
from subprocess import call
from platform import system
from webbrowser import open_new_tab
from tkinter import *
from tkinter import messagebox, filedialog, ttk


# Variables naming convention:
# Varibles for the various windows are xw_, where "x" is the first letter of the discription of the window.
# Variables for the MP4 section are prefixed with m_
# Variables for the WMV section are prefixed with w_
# Variables for the SWF section are prefixed with s_
# Variables for the global conversion settings are prefixed with g_


def init_script():
    global g_input_file_dir
    global g_output_file_dir
    global g_media_setting
    global g_showui
    global g_need_ui_section
    global g_width
    global g_height
    global m_ui_chat
    global m_ui_qa
    global m_ui_largeroutline
    global m_framerate
    global s_console_pcaudio
    global s_framerate
    global w_console_pcaudio
    global w_ui_chat
    global w_ui_video
    global w_ui_largeroutline
    global w_videocodec
    global w_audiocodec
    global w_videoformat
    global w_audioformat
    global w_videokeyframes
    global w_maxstream
    global nbr_path
    global ow_display_screen
    path_to_file = path.abspath(__file__)
    directory_name = path.dirname(path_to_file)
    chdir(directory_name)
    nbr_path = "C:\ProgramData\WebEx\WebEx\\500\\nbrplay.exe"
    g_input_file_dir = path.dirname(path_to_file)
    g_output_file_dir = path.dirname(path_to_file) + "\\Converted"
    g_media_setting = "MP4"
    g_showui = 0
    g_need_ui_section = True
    g_width = 1920
    g_height = 1080
    m_ui_chat = 1
    m_ui_qa = 1
    m_ui_largeroutline = 1
    m_framerate = 5
    s_console_pcaudio = 0
    s_framerate = 10
    w_console_pcaudio = 0
    w_ui_chat = 1
    w_ui_video = 1
    w_ui_largeroutline = 1
    w_videocodec = "Windows Media Video 9"
    w_audiocodec = "Windows Media Audio 9.2 Lossless"
    w_videoformat = "default"
    w_audioformat = "default"
    w_videokeyframes = 4
    w_maxstream = 1000
    ow_display_screen = "main"
    check_os()
    locate_nbr()


# Initializes the script with default values and changes to the directory where the script is located.

def check_os():
    if system() != "Windows":
        messagebox.showerror("Compatibility Error", "Please use Windows for file conversions.\nOther OSs are currently not supported :-(")
        exit()


def check_for_nbr(path_to_nbr):
    result = path.exists(path_to_nbr)
    return result


def locate_nbr():
    if not check_for_nbr(nbr_path):
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


def file_type_set(ftype):
    global file_type
    file_type = ftype.lower()


# Sets the file type to be converted to.


def custom_nbr_location():
    global nbr_path
    nbrplay.exe
    messagebox.showinfo("Find the player...", message="Please browse to the path to the nbrplay.exe")
    nbr_path = filedialog.askdirectory(mustexist=True)


# Sets the nbr_path variable to the user provided path.


def check_folder():
    global g_input_file_dir
    global g_output_file_dir
    error_num = 0
    if not path.exists(g_input_file_dir):
        error_num = error_num + 5
    elif not path.exists(g_output_file_dir):
        error_num = error_num + 4
    return error_num


# Check is the source directory exists and if it does not then displays an error and goes back to the main menu.
# Also checks if the output directory exists and if it does not it creates it.
# 5 = input
# 4 = output
# 9 = input and output


def progress_bar_window_system():
    global progress_bar
    global pg_window
    main_window.withdraw()
    pg_window = Tk()
    w = 250 # width for the Tk root
    h = 200 # height for the Tk root
    ws = pg_window.winfo_screenwidth() # width of the screen
    hs = pg_window.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    

    pg_window.title("Converstion Progress")
    pg_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    progress_bar = ttk.Progressbar(pg_window, length=250, mode="determinate")
    progress_bar.pack()

    conversion_text = ttk.Label(pg_window, anchor=CENTER, text="Converting Files")
    conversion_text.pack(fill=X)

    pg_window.after(1, func=convert_file)
    pg_window.mainloop()


def convert_file():
    global g_input_file_dir
    global progress_bar
    global pg_window
    pg_window.update()
    if check_folder() == 5:
        pg_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF input dir is invalid, please check that it exisits.")
        main_window.deiconify()
        return
    elif check_folder() == 4:
        pg_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF output dir is invalid, please check that it exisits.")
        main_window.deiconify()
        return
    elif check_folder() == 9:
        pg_window.destroy()
        messagebox.showerror("Cannot continue!", "The ARF input and output dirs are invalid, please check that they exist.")
        main_window.deiconify()
        return
    cfg_counter = 0
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            remove(file)
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "arf":
            create_configs(file)
            cfg_counter += 1
    progress_bar.config(maximum=cfg_counter)
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            execute_nbr_conversion(g_input_file_dir + "\\" + file)
            cfg_counter -= 1
            progress_bar.config(value=cfg_counter)
            pg_window.update()
            remove(file)
    pg_window.destroy()
    main_window.deiconify()
    messagebox.showinfo(title="Conversion complete!", message="File conversion(s) are complete!")


def create_configs(fname):
    global file_type
    with open(fname[:-3] + "cfg", "a") as config_file:
        config_file.write("[Console]")
        config_file.write("\ninputfile=%s" % g_input_file_dir + "\\" + fname)
        config_file.write("\nmedia=%s" % file_type.upper())
        config_file.write("\nshowui=%s" % g_showui)
        if file_type == "swf":
            config_file.write("\nPCAudio=%s" % s_console_pcaudio)
        elif file_type == "wmv":
            config_file.write("\nPCAudio=%s" % w_console_pcaudio)
        if g_need_ui_section:
            config_file.write("\n[UI]")
        if file_type == "mp4":
            config_file.write("\nchat=%s" % m_ui_chat)
        elif file_type == "wmv":
            config_file.write("\nchat=%s" % w_ui_chat)
        if file_type == "mp4":
            config_file.write("\nqa=%s" % m_ui_qa)
        elif file_type == "wmv":
            config_file.write("\nvideo=%s" % w_ui_video)
        if file_type == "mp4":
            config_file.write("\nlargeroutline=%s" % m_ui_largeroutline)
        elif file_type == "wmv":
            config_file.write("\nlargeroutline=%s" % w_ui_largeroutline)
        config_file.write("\n[%s]" % file_type.upper())
        config_file.write("\noutputfile=%s" % g_output_file_dir + "\\" + fname[:-3] + file_type)
        config_file.write("\nwidth=%s" % g_width)
        config_file.write("\nheight=%s" % g_height)
        if file_type == "mp4":
            config_file.write("\nframerate=%s" % m_framerate)
        elif file_type == "wmv":
            config_file.write("\nvideocodec=%s" % w_videocodec)
        elif file_type == "swf":
            config_file.write("\nframerate=%s" % s_framerate)
        if file_type == "wmv":
            config_file.write("\naudiocodec=%s" % w_audiocodec)
        if file_type == "wmv":
            config_file.write("\nvideoformat=%s" % w_videoformat)
        if file_type == "wmv":
            config_file.write("\naudioformat=%s" % w_audioformat)
        if file_type == "wmv":
            config_file.write("\nvideokeyframes=%s" % w_videokeyframes)
        if file_type == "wmv":
            config_file.write("\nmaxstream=%s" % w_maxstream)


# Creates configuration files for the nbrplayer to use to convert the files.


def execute_nbr_conversion(cfg_name):
    global nbr_path
    call(nbr_path + " -Convert" + ' "' + cfg_name + '"')


# Executes the nbr executable with the path to the generated cfg file.


def main_window_create():
    global main_window
    main_window = Tk()
    w = 250 # width for the Tk root
    h = 200 # height for the Tk root
    ws = main_window.winfo_screenwidth() # width of the screen
    hs = main_window.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # Create main Window and gather information.

    main_window.title("ARF Auto Converter")
    main_window.minsize(250, 200)
    main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # set window properties.

    main_window.grid_columnconfigure(0,weight=1)
    main_window.grid_columnconfigure(1,weight=1)
    main_window.grid_rowconfigure(0,weight=1)
    main_window.grid_rowconfigure(1,weight=1)
    main_window.grid_rowconfigure(2,weight=1)
    main_window.grid_rowconfigure(3,weight=1)

    # make the interface responsive.

    mw_welcome_text = ttk.Label(main_window, anchor=CENTER, text="Welcome to the ARF auto converter!")
    mw_MP4_button = ttk.Button(main_window, text="Convert to MP4", command=button_mp4)
    mw_WMV_button = ttk.Button(main_window, text="Convert to WMV", command=button_wmv)
    mw_SWF_button = ttk.Button(main_window, text="Convert to SWF", command=button_swf)
    mw_options_button = ttk.Button(main_window, text="Advanced Options", command=options_window_create)
    mw_exit_button = ttk.Button(main_window, text="Exit", command=exit)

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


def options_window_create():
    global options_window
    main_window.destroy()
    options_window = Tk()
    w = 500 # width for the Tk root
    h = 200 # height for the Tk root
    ws = options_window.winfo_screenwidth() # width of the screen
    hs = options_window.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # Create main window and gathers various info
    
    if ow_display_screen == "main":
        
        options_window.title("Advanced Options")
        options_window.minsize(500, 200)
        options_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        # Set window properties
        
        options_window.grid_columnconfigure(0,weight=1)
        options_window.grid_rowconfigure(0,weight=1)
        
        # Make the interface responsive
        
        ow_welcome_text = ttk.Label(options_window, anchor=CENTER, justify=CENTER, text="You can only currently restore the default setting. More to come soon!")
        ow_restore_defaults = ttk.Button(options_window, text="Restore Defaults", command=init_script)
        ow_back_to_mw = ttk.Button(options_window, text="Back to Main Window", command=button_back_to_mw)
        
        # Create the widgets on the window
        
        ow_welcome_text.grid(columnspan=2, sticky="NESW")
        ow_restore_defaults.grid(row=1, column=1, sticky="NSEW")
        ow_back_to_mw.grid(row=1, sticky="NSEW")
        
        # Arrange the widgets
        
        options_window.mainloop()
        
        # Keep the options window onscreen.
    elif ow_display_screen == "global":
        pass


def button_mp4():
    file_type_set("mp4")
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_wmv():
    file_type_set("wmv")
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_swf():
    file_type_set("swf")
    progress_bar_window_system()


# Starts file conversions for the SWF file type.


def button_back_to_mw():
    options_window.destroy()
    main_window_create()


# Stops the options window and opens the main window.


init_script()
main_window_create()

# Starts the main window.
