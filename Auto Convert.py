from os import path, chdir, listdir, makedirs, remove
from subprocess import call
from platform import system
from webbrowser import open_new_tab


# Variables naming convention:
# Variables for menus are prefixed with me_
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
    path_to_file = path.abspath(__file__)
    directory_name = path.dirname(path_to_file)
    chdir(directory_name)
    nbr_path = "C:\programdata\webex\webex\\500\\nbrplay.exe"
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
    check_os()
    locate_nbr()


# Initializes the script with default values and changes to the directory where the script is located.


def clear_screen():
    if system() == "Windows":
        call("cls", shell=True)
    elif system() == "Darwin" or system() == "Linux":
        call("clear", shell=True)


# Sets up a multi platform clear screen function for Windows, OS X and Linux


def check_os():
    if system() != "Windows":
        clear_screen()
        print("This script is currently only compatible with Windows.")
        input("\nPress Enter/Return to continue...")
        exit_program(False)


# Check if the operating system is supported.


def check_for_nbr(path_to_nbr):
    result = path.exists(path_to_nbr)
    return result


# Checks for the nbr.exe at the provided location.


def locate_nbr():
    if not check_for_nbr(nbr_path):
        clear_screen()
        print("The system could not find the NBR player.\nWould you like to download it?")
        me_locate_nbr = str(input("\nY or N: "))
        if me_locate_nbr.lower() == "y":
            open_new_tab("www.webex.com/play-webex-recording.html")
            exit()
        elif me_locate_nbr.lower() == "n":
            clear_screen()
            print("Do you have it installed already?")
            me_nbr_already_installed = str(input("Y or N: "))
            if me_nbr_already_installed.lower() == "y":
                custom_nbr_location()
            else:
                clear_screen()
                print("This script requires the Network Broadcast Recording player to operate.")
                print("Please have it installed for the next time you run this script.")
                input("\nPress Enter/Return to continue...")
                exit_program(False)
        else:
            clear_screen()
            print("Please enter either Y or N!")
            input("\nPress Enter/Return to continue...")
            locate_nbr()
    else:
        return True


# If the nbr.exe is not at the default location, asks user where it is. If not installed asks user if the user wishes to
# download the program. If the user does not want to then it stops the script and tells the user that it is required.


def custom_nbr_location():
    global nbr_path
    clear_screen()
    print("Please enter the path to the nbrplay.exe here")
    nbr_path = input("\n(E.G. C:\\foo\\bar\\nbrplay.exe): ")


# Sets the nbr_path variable to the user provided path.


def main_menu():
    clear_screen()
    print("Welcome to the Automatic ARF converter program. You have 5 options to chose from:")
    print("\n1. Convert file(s) to MP4")
    print("2. Convert file(s) to WMV")
    print("3. Convert file(s) to SWF")
    print("\n4. Advanced Options")
    print("5. Exit program")
    me_main_menu = int(input("\nEnter your selection here (1-5) then press Enter/Return: "))
    if me_main_menu == 1:
        file_type("mp4")
        convert_file()
    elif me_main_menu == 2:
        file_type("wmv")
        convert_file()
    elif me_main_menu == 3:
        file_type("swf")
        convert_file()
    elif me_main_menu == 4:
        options_menu()
    elif me_main_menu == 5:
        exit_program(True)
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 5!")
        input("\n Press Enter/Return to continue...")
        main_menu()


# Creates the main menu for the user to navigate.


def file_type(ftype):
    global file_type
    file_type = ftype


# Sets the file type to be converted to.


def check_folder():
    if not path.exists(g_input_file_dir):
        print("The source directory does not exist. Please check your settings and try again.")
        input("\nPress Enter/Return to continue...")
        main_menu()
    elif not path.exists(g_output_file_dir):
        makedirs(g_output_file_dir)
        return "Created Destination Directory"


# Check is the source directory exists and if it does not then displays an error and goes back to the main menu.
# Also checks if the output directory exists and if it does not it creates it.


def convert_file():
    cfg_counter = 0
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            remove(file)
        if path.isfile(file) and file[-3:].lower() == "arf":
            create_configs(file)
            cfg_counter += 1
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            clear_screen()
            print("%s Files left to convert. This may take a while..." % str(cfg_counter))
            execute_nbr_conversion(file)
            cfg_counter -= 1


# Deletes CFG files already present in the selected/default folder then creates new config files. After the cfg creation
# is complete, the NBR player is executed with the new cfg files for reference while the remaining files are counted
# down.


def create_configs(fname):
    global file_type
    with open(fname + ".cfg", "a") as config_file:
        config_file.write("[Console]")
        config_file.write("inputfile=%s" % g_input_file_dir + fname)
        config_file.write("media=%s" % file_type.upper())
        config_file.write("showui=%s\n" % g_showui)
        if file_type.lower() == "swf":
            config_file.write("PCAudio=%s" % s_console_pcaudio)
        elif file_type.lower() == "wmv":
            config_file.write("PCAudio=%s" % w_console_pcaudio)
        if g_need_ui_section:
            config_file.write("[UI]")
        if file_type.lower() == "mp4":
            config_file.write("chat=%s" % m_ui_chat)
        elif file_type.lower() == "wmv":
            config_file.write("chat=%s" % w_ui_chat)
        if file_type.lower() == "mp4":
            config_file.write("qa=%s" % m_ui_qa)
        elif file_type.lower() == "wmv":
            config_file.write("video=%s" % w_ui_video)
        if file_type.lower() == "mp4":
            config_file.write("largeroutline=%s" % m_ui_largeroutline)
        elif file_type.lower() == "wmv":
            config_file.write("largeroutline=%s" % w_ui_largeroutline)
        config_file.write("[%s]" % file_type.upper())
        config_file.write("outputfile=%s" % g_input_file_dir + fname[:-3] + "mp4")
        config_file.write("width=%s" % g_width)
        config_file.write("height=%s" % g_height)
        if file_type.lower() == "mp4":
            config_file.write("framerate=%s" % m_framerate)
        elif file_type.lower() == "wmv":
            config_file.write("videocodec=%s" % w_videocodec)
        elif file_type.lower() == "swf":
            config_file.write("framerate=%s" % s_framerate)
        if file_type.lower() == "wmv":
            config_file.write("audiocodec=%s" % w_audiocodec)
        if file_type.lower() == "wmv":
            config_file.write("videoformat=%s" % w_videoformat)
        if file_type.lower() == "wmv":
            config_file.write("audioformat=%s" % w_audioformat)
        if file_type.lower() == "wmv":
            config_file.write("videokeyframes=%s" % w_videokeyframes)
        if file_type.lower() == "wmv":
            config_file.write("maxstream=%s" % w_maxstream)


# Creates configuration files for the nbrplayer to use to convert the files.


def execute_nbr_conversion(cfg_name):
    args = ["nbr_path", "-Convert"]
    args.append(cfg_name)
    call(args, shell=True)


# Executes the nbr executable with the path to the generated cfg file.


def options_menu():
    clear_screen()
    print("Here you can change options for the conversion. You have 6 options to chose from:")
    print("\n1. MP4 Options")
    print("2. WMV Options")
    print("3. SWF Options")
    print("4. Global Options (applies to all formats)")
    print("\n5. Restore default settings")
    print("\n6. Go back to the main menu")
    me_options_menu = int(input("\nEnter your selection here (1-6)"))
    if me_options_menu == 1:
        mp4_options_menu()
    elif me_options_menu == 2:
        wmv_options_menu()
    elif me_options_menu == 3:
        swf_options_menu()
    elif me_options_menu == 4:
        global_options_menu()
    elif me_options_menu == 5:
        restore_default_settings()
    elif me_options_menu == 6:
        main_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 6!")
        input("\nPress Enter/Return to continue...")
        options_menu()


# Creates the options menu for the user to navigate.


def mp4_options_menu():
    clear_screen()
    print("MP4 Files have 4 configurable options (at the moment)\n\n1. Toggle Chat Window\n2. Toggle Q&A Box")
    print("3. Toggle Largeroutline\n4. Change Framerate\n\n5. Go back to the main options menu.")
    me_mp4_options_menu = int(input("\nPlease enter 1-5 and press Enter/Return: "))
    if me_mp4_options_menu == 1:
        mp4_toggle_chat()
    elif me_mp4_options_menu == 2:
        mp4_toggle_qa()
    elif me_mp4_options_menu == 3:
        mp4_toggle_largeroutline()
    elif me_mp4_options_menu == 4:
        mp4_change_framerate()
    elif me_mp4_options_menu == 5:
        options_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 5!")
        input("\n Press Enter/Return to continue...")
        mp4_options_menu()


# Lists settings available for the MP4 file format


def mp4_toggle_chat():
    global m_ui_chat
    clear_screen()
    print("The Q&A box toggle is set to: %s" % m_ui_chat)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_chat = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_chat.lower() == "y":
        if m_ui_chat == 1:
            m_ui_chat = 0
        else:
            m_ui_chat = 1
        clear_screen()
        print("The Q&A box toggle is now set to: %s" % m_ui_chat)
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the chat box setting for MP4 files.


def mp4_toggle_qa():
    global m_ui_qa
    clear_screen()
    print("The Q&A box toggle is set to: %s" % m_ui_qa)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_qa = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_qa.lower() == "y":
        if m_ui_qa == 1:
            m_ui_qa = 0
        else:
            m_ui_qa = 1
        clear_screen()
        print("The Q&A box toggle is now set to: %s" % m_ui_qa)
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the Q&A box setting for MP4 files.


def mp4_toggle_largeroutline():
    global m_ui_largeroutline
    clear_screen()
    print("The LargerOutline toggle is set to: %s" % m_ui_largeroutline)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_largeroutline = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_largeroutline.lower() == "y":
        if m_ui_largeroutline == 1:
            m_ui_largeroutline = 0
        else:
            m_ui_largeroutline = 1
        clear_screen()
        print("The LargerOutline toggle is now set to: %s" % m_ui_largeroutline)
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the LargerOutline setting for MP4 files.


def mp4_change_framerate():
    global m_framerate
    clear_screen()
    print("The current frame rate is set to: %sFPS.\nLeave it blank to do nothing." % m_framerate)
    print("Enter a number above 0 (the recommended range is 1 to 10) to change the setting.")
    me_mp4_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_mp4_change_framerate > 0:
        m_framerate = me_mp4_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % m_framerate)
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Changes the frame rate for MP4 files.


def wmv_options_menu():
    clear_screen()
    print("WMV Files have 10 configurable options (at the moment)\n\n1. Toggle PCAudio setting\n2. Toggle Chat Box")
    print("3. Toggle Webcam Video\n4. Toggle Largeroutline setting\n5. Change the video codec")
    print("6. Change the audio codec\n7. Alter the Videoformat setting\n8. Alter the Audioformat setting")
    print("9. Change the video key frames (frame rate)\n10. Change the maxstream (bitrate)")
    print("\n\n11. Go back to the main options menu.")
    me_wmv_options_menu = int(input("\nPlease enter 1-11 and press Enter/Return: "))
    if me_wmv_options_menu == 1:
        wmv_toggle_pcaudio()
    elif me_wmv_options_menu == 2:
        wmv_toggle_chat_box()
    elif me_wmv_options_menu == 3:
        wmv_toggle_webcam_video()
    elif me_wmv_options_menu == 4:
        wmv_toggle_largeroutline()
    elif me_wmv_options_menu == 5:
        wmv_change_videocodec()
    elif me_wmv_options_menu == 6:
        wmv_change_audiocodec()
    elif me_wmv_options_menu == 7:
        wmv_alter_videoformat()
    elif me_wmv_options_menu == 8:
        wmv_alter_audioformat()
    elif me_wmv_options_menu == 9:
        wmv_change_keyframes()
    elif me_wmv_options_menu == 10:
        wmv_change_maxstream()
    elif me_wmv_options_menu == 11:
        options_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 11!")
        input("\nPress Enter/Return to continue...")
        wmv_options_menu()


# Lists settings available for the WMV file format


def wmv_toggle_pcaudio():
    global w_console_pcaudio
    clear_screen()
    print("The PCAudio toggle is set to: %s\n Would you like to toggle this setting?" % w_console_pcaudio)
    print("This is an experimental and untested setting!!!")
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_pcaudio = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_pcaudio.lower() == "y":
        if w_console_pcaudio == 1:
            w_console_pcaudio = 0
        else:
            w_console_pcaudio = 1
        clear_screen()
        print("The PCAudio toggle is now set to: %s" % w_console_pcaudio)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Enables or Disables the PCAudio setting for the WMV file


def wmv_toggle_chat_box():
    global w_ui_chat
    clear_screen()
    print("The chat box toggle is set to: %s\n Would you like to toggle this setting?" % w_ui_chat)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_chat_box = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_chat_box.lower() == "y":
        if w_ui_chat == 1:
            w_ui_chat = 0
        else:
            w_ui_chat = 1
        clear_screen()
        print("The chat box toggle is now set to: %s" % w_ui_chat)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the chat box setting for WMV files.


def wmv_toggle_webcam_video():
    global w_ui_video
    clear_screen()
    print("The web cam box toggle is set to: %s\n Would you like to toggle this setting?" % w_ui_video)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_video_box = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_video_box.lower() == "y":
        if w_ui_video == 1:
            w_ui_video = 0
        else:
            w_ui_video = 1
        clear_screen()
        print("The web cam toggle is now set to: %s" % w_ui_video)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the web cam box setting for WMV files.


def wmv_toggle_largeroutline():
    global w_ui_largeroutline
    clear_screen()
    print("The LargerOutline toggle is set to: %s\n Would you like to toggle this setting?" % w_ui_largeroutline)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_largeroutline = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_largeroutline.lower() == "y":
        if w_ui_largeroutline == 1:
            w_ui_largeroutline = 0
        else:
            w_ui_largeroutline = 1
        clear_screen()
        print("The LargerOutline toggle is now set to: %s" % w_ui_largeroutline)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the LargerOutline setting for WMV files.


def wmv_change_videocodec():
    global w_videocodec
    clear_screen()
    print("The WMV video codec is currently set to: %s" % w_videocodec)
    print("There are 2 options for this setting:\n1. Windows Media Video 9\n2. Windows Media Video 9 Screen")
    print("\nLeave the field blank to do nothing")
    me_wmv_videocodec = int(input("\nPlease enter 1 or 2 then press Enter/Return: "))
    if me_wmv_videocodec == int:
        if me_wmv_videocodec == 1:
            w_videocodec = "Windows Media Video"
        elif me_wmv_videocodec == 2:
            w_videocodec = "Windows Media Video 9 Screen"
        clear_screen()
        print("The video codec is now set to: %s" % w_videocodec)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the Video Codec for WMV files.


def wmv_change_audiocodec():
    global w_audiocodec
    clear_screen()
    print("The WMV audio codec is currently set to: %s" % w_audiocodec)
    print("There are 3 options for this setting:\n1. Windows Media Audio 9.2 9\n2. Windows Media Audio 9.2 Lossless")
    print("3. Windows Media Audio 10 Professional\nLeave the field blank to do nothing")
    me_wmv_audiocodec = int(input("\nPlease enter 1-3 then press Enter/Return: "))
    if me_wmv_audiocodec == 1:
        w_audiocodec = "Windows Media Video"
    elif me_wmv_audiocodec == 2:
        w_audiocodec = "Windows Media Video 9 Screen"
    elif me_wmv_audiocodec == 3:
        w_audiocodec = "Windows Media Audio 10 Professional"
    clear_screen()
    print("The audio codec is now set to: %s" % w_audiocodec)
    input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the Audio Codec for WMV files.


def wmv_alter_videoformat():
    global w_videoformat
    clear_screen()
    print("I have no idea what this setting does so I do not recommend changing this.")
    print("Leave the field blank to do nothing.\n The current setting is: %s" % w_videoformat)
    me_wmv_videoformat = input("Enter some value here: ")
    if len(me_wmv_videoformat) > 0:
        w_videoformat = me_wmv_videoformat
        clear_screen()
        print("The VideoFormat setting is now set to: %s" % w_videoformat)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the VideoFormat for WMV files.


def wmv_alter_audioformat():
    global w_audioformat
    clear_screen()
    print("I have no idea what this setting does so I do not recommend changing this.")
    print("Leave the field blank to do nothing.\n The current setting is: %s" % w_audioformat)
    me_wmv_audioformat = input("Enter some value here: ")
    if len(me_wmv_audioformat) > 0:
        w_audioformat = me_wmv_audioformat
        clear_screen()
        print("The AudioFormat setting is now set to: %s" % w_audioformat)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the AudioFormat for WMV files.


def wmv_change_keyframes():
    global w_videokeyframes
    clear_screen()
    print("The current frame rate is set to: %sFPS.\nLeave it blank to do nothing." % w_videokeyframes)
    print("Enter a number above 0 (the recommended range is 4 to 10) to change the setting.")
    me_wmv_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_wmv_change_framerate > 0:
        w_videokeyframes = me_wmv_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % w_videokeyframes)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the KeyFrames for WMV files.


def wmv_change_maxstream():
    global w_maxstream
    clear_screen()
    print("The current MaxStream is set to: %sBPS.\nLeave it blank to do nothing." % w_maxstream)
    print("Enter a number above 0 (the recommended range is 500 to 1000) to change the setting.")
    me_wmv_change_maxstream = int(input("Press Enter/Return when you are ready to continue: "))
    if me_wmv_change_maxstream > 0:
        w_maxstream = me_wmv_change_maxstream
        clear_screen()
        print("MaxStream is now set to: %s" % w_maxstream)
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the MaxStream for WMV files.


def swf_options_menu():
    clear_screen()
    print("SWF Files have 2 configurable options (at the moment):\n\n1. Toggle PCAudio setting\n2. Change frame rate")
    print("\n3. Go back to the main options menu.")
    me_swf_options_menu = int(input("\nPlease enter 1-3 and press Enter/Return: "))
    if me_swf_options_menu == 1:
        swf_toggle_pcaudio()
    elif me_swf_options_menu == 2:
        swf_change_framerate()
    elif me_swf_options_menu == 3:
        options_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 3!")
        input("\n Press Enter/Return to continue...")
        swf_options_menu()


# Lists settings available for the SWF file format


def swf_toggle_pcaudio():
    global s_console_pcaudio
    clear_screen()
    print("The PCAudio toggle is set to: %s\n Would you like to toggle this setting?" % s_console_pcaudio)
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_swf_toggle_pcaudio = input("Press Enter/Return when you are ready to continue: ")
    if me_swf_toggle_pcaudio.lower() == "y":
        if s_console_pcaudio == 1:
            s_console_pcaudio = 0
        else:
            s_console_pcaudio = 1
        clear_screen()
        print("The PCAudio toggle is now set to: %s" % s_console_pcaudio)
        input("Press Enter/Return to continue...")
    swf_options_menu()


# Enables or Disables the PCAudio setting for the SWF file


def swf_change_framerate():
    global s_framerate
    clear_screen()
    print("The current frame rate is set to: %sFPS. Leave below blank to do nothing." % s_framerate)
    print("Enter a number above 0 to change the frame rate (the recommended range is from 1 to 10).")
    me_swf_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_swf_change_framerate > 0:
        s_framerate = me_swf_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % s_framerate)
        input("Press Enter/Return to continue...")
    swf_options_menu()


# Changes the frame rate for SWF files.


def global_options_menu():
    clear_screen()
    print("There are 5 global options (at the moment):4\n\n1. Set the ARF input folder\n2. Toggle ShowUI")
    print("3. Set the converted output folder\n4. Set the resolution Width\n5. Set the resolution Height")
    print("\n6. Go back to the main options menu.")
    me_global_options_menu = int(input("\nPlease enter 1-6 and press Enter/Return: "))
    if me_global_options_menu == 1:
        global_input_dir()
    elif me_global_options_menu == 2:
        global_toggle_showui()
    elif me_global_options_menu == 3:
        global_input_dir()
    elif me_global_options_menu == 4:
        global_set_res_width()
    elif me_global_options_menu == 5:
        global_set_res_height()
    elif me_global_options_menu == 6:
        options_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 6!")
        input("\nPress Enter/Return to continue...")
        global_options_menu()


# Lists settings available that are compatible with all of the file formats


def global_input_dir():
    global g_input_file_dir
    clear_screen()
    print("This sets the directory that contains all of the ARFs to be converted. By default this setting is the same")
    print("as the directory that this script file is in.")
    print("The current input dir is: %s" % g_input_file_dir)
    print("\nEnter the full path to the directory that contains the ARF files to be converted or blank to do nothing.")
    me_global_input_dir = input("Press Enter/Return when you are ready to continue: ")
    if len(me_global_input_dir) > 0:
        g_input_file_dir = me_global_input_dir
        clear_screen()
        print("The input directory is now set to: %s" % g_input_file_dir)
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Sets the directory that contains all of the ARF files to be converted.


def global_toggle_showui():
    global g_showui
    clear_screen()
    print("The ShowUI toggle is set to: %s\n Would you like to toggle this setting?" % g_showui)
    print("This option is experimental, I would not recommend changing this until tested.")
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_global_toggle_showui = input("Press Enter/Return when you are ready to continue: ")
    if me_global_toggle_showui.lower() == "y":
        if g_showui == 1:
            g_showui = 0
        else:
            g_showui = 1
        clear_screen()
        print("The ShowUI toggle is now set to: %s" % g_showui)
        input("Press Enter/Return to continue...")
    global_options_menu()


# Toggles the ShowUI setting for all file types.


def global_output_dir():
    global g_output_file_dir
    clear_screen()
    print("This sets the directory that will contain all of the converted ARFs. By default this setting is .\Converted")
    print("The current output dir is: %s" % g_output_file_dir)
    print("\nEnter the full path to the directory that will contain the converted ARF files or blank to do nothing.")
    me_global_output_dir = input("Press Enter/Return when you are ready to continue: ")
    if len(me_global_output_dir) > 0:
        g_output_file_dir = me_global_output_dir
        clear_screen()
        print("The output directory is now set to: %s" % g_output_file_dir)
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Sets the directory that will contain all of the converted ARF files after conversion.


def global_set_res_width():
    global g_width
    clear_screen()
    print("This sets the resolution width for the converted file.")
    print("The resolution width is currently set to: %spx" % g_width)
    print("\nEnter a number(recommended values are 1024 and above). Leave blank to change nothing.")
    me_global_res_width = len(input("Press Enter/Return when you are ready to continue: "))
    if me_global_res_width > 0:
        g_width = me_global_res_width
        clear_screen()
        print("The resolution width is now set to: %s" % g_width)
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Changes the output file's resolution width (the 1024 in 1024x768)


def global_set_res_height():
    global g_height
    clear_screen()
    print("This sets the resolution height for the converted file.")
    print("The resolution height is currently set to: %spx" % g_height)
    print("\nEnter a number(recommended values are 768 and above). Leave blank to change nothing.")
    me_global_res_height = len(input("Press Enter/Return when you are ready to continue: "))
    if me_global_res_height > 0:
        g_height = me_global_res_height
        clear_screen()
        print("The resolution height is now set to: %s" % g_height)
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Changes the output file's resolution height (the 768 in 1024x768)


def restore_default_settings():
    init_script()
    options_menu()


# Restores all settings to default values


def exit_program(friendly):
    clear_screen()
    if friendly:
        print("Thank you for using this script, I hope you enjoyed it!")
    elif not friendly:
        print("Thank you for considering this product! If you have any issues please email thelich2@gmail.com or")
        print("file an issue on https://github.com/elliot-labs/ARF-Converter\n\nThanks!")
    else:
        print("You have triggered an exit that the programmer has not foreseen.")
        print("Please report this to thelich2@gmail.com or https://github.com/elliot-labs/ARF-Converter")
    exit()


# This is a simple program closer that thanks the user for using the program.


init_script()
main_menu()


# Let the madness begin!
