from os import path
from os import chdir
from os import listdir
from os import makedirs
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
    path_to_file = path.abspath(__file__)
    directory_name = path.dirname(path_to_file)
    chdir(directory_name)
    nbr_path = "C:\programdata\webex\webex\\500\\nbrplay.exe"
    g_input_file_dir = path.dirname(path_to_file)
    g_output_file_dir = path.dirname(path_to_file) + "\\Converted"
    g_media_setting = "MP4"
    g_showui = 0
    g_need_ui_section = True
    g_width = 1440
    g_height = 768
    m_ui_chat = 1
    m_ui_qa = 1
    m_ui_largeroutline = 1
    m_framerate = 5
    s_console_pcaudio = 0
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
    check_os()
    locate_nbr()


# Initializes the script with default values and changes to the directory where the script is located.


def clear_screen():
    if system() == "Windows":
        call("cls")
    elif system() == "Darwin" or system() == "Linux":
        call("clear")


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
    clear_screen()
    print("Please enter the path to the nbrplay.exe here")
    nbr_path = input("\n(E.G. C:\\foo\\bar\\nbrplay.exe): ")
    global nbr_path


# Sets the nbr_path variable to the user provided path.


def main_menu():
    clear_screen()
    print("Welcome to the Automatic ARF converter program. You have 5 options to chose from:")
    print("\n1. Convert file(s) to MP4")
    print("2. Convert file(s) to WMV")
    print("3. Convert file(s) to SWF")
    print("\n4. Advanced Options")
    print("5. Exit program")
    me_main_menu = input("\n enter your selection here (1-5) then press Enter/Return: ")
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
    file_type = ftype
    global file_type


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
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "arf":
            create_configs(file)
            execute_nbr_conversion(file + ".cfg")


# Converts the ARF file(s) to the previously selected format


def create_configs(fname):
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
    call(args)



def options_menu():
    clear_screen()
    print("Here you can change options for the conversion. You have 6 options to chose from:")
    print("\n1. MP4 Options")
    print("2. WMV Options")
    print("3. SWF Options")
    print("4. Global Options (applies to all formats)")
    print("\n5. Restore default settings")
    print("\n6. Go back to the main menu")
    me_options_menu = input("\nEnter your selection here (1-6)")
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
        input("\n Press Enter/Return to continue...")
        options_menu()


# Creates the options menu for the user to navigate.


def mp4_options_menu():
    clear_screen()
    print("MP4 Files have 4 configurable options (at the moment)\n\n1. Toggle Chat Window\n2. Toggle Q&A Box")
    print("3. Toggle Largeroutline\n4. Change Framerate\n\n5. Go back to the main options menu.")
    me_mp4_options_menu = input("\nPlease enter 1-5 and press Enter/Return: ")
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
    clear_screen()
    print("The current chat toggle is set to: %s\n Would you like to toggle this setting?" % m_ui_chat)
    print("Press Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_chat = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_chat.lower() == "y":
        if m_ui_chat == 1:
            m_ui_chat = 0
            global m_ui_chat
            clear_screen()
            print("The chat toggle is now set to: %s" % m_ui_chat)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
        else:
            m_ui_chat = 1
            global m_ui_chat
            clear_screen()
            print("The chat toggle is now set to: %s" % m_ui_chat)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
    else:
        mp4_options_menu()


def mp4_toggle_qa():
    clear_screen()
    print("The current Q&A toggle is set to: %s\n Would you like to toggle this setting?" % m_ui_qa)
    print("Press Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_qa = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_qa.lower() == "y":
        if m_ui_qa == 1:
            m_ui_qa = 0
            global m_ui_qa
            clear_screen()
            print("The Q&A toggle is now set to: %s" % m_ui_qa)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
        else:
            m_ui_qa = 1
            global m_ui_qa
            clear_screen()
            print("The Q&A toggle is currently set to: %s" % m_ui_qa)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
    else:
        mp4_options_menu()


def mp4_toggle_largeroutline():
    clear_screen()
    print("The current Largeroutline toggle is set to: %s\n Would you like to toggle this setting?" % m_ui_largeroutline)
    print("Press Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_largeroutline = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_largeroutline.lower() == "y":
        if m_ui_largeroutline == 1:
            m_ui_largeroutline = 0
            global m_ui_largeroutline
            clear_screen()
            print("The largeroutline toggle is now set to: %s" % m_ui_largeroutline)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
        else:
            m_ui_largeroutline = 1
            global m_ui_largeroutline
            clear_screen()
            print("The largeroutline toggle is now set to: %s" % m_ui_largeroutline)
            input("Press Enter/Return to continue...")
            mp4_options_menu()
    else:
        mp4_options_menu()


def mp4_change_framerate():
    clear_screen()
    print("The current framerate is set to: %sFPS.\nWould you like to change this setting?" % m_framerate)
    print("Enter a number above 0 (the recommended range is 1 to 10) to toggle the setting.")
    me_mp4_change_framerate = input("Leave it blank to do nothing. Press Enter/Return when you are ready to continue: ")
    if me_mp4_change_framerate > 0:
        m_framerate = me_mp4_change_framerate
        global m_framerate
        clear_screen()
        print("The framerate is now set to: %sFPS" % m_framerate)
        input("Press Enter/Return to continue...")
        mp4_options_menu()
    else:
        mp4_options_menu()


def wmv_options_menu():
    clear_screen()
    print("WMV Files have 10 configurable options (at the moment)\n\n1. Toggle PCAudio setting\n2. Toggle Chat Box")
    print("3. Toggle Webcam Video\n4. Toggle Largeroutline setting\n5. Change the video codec")
    print("6. Change the audio codec\n7. Alter the Videoformat setting\n8. Alter the Audioformat setting")
    print("9. Change the video key frames (framerate)\n10. Change the maxstream (bitrate)")
    print("\n\n11. Go back to the main options menu.")
    me_mp4_options_menu = input("\nPlease enter 1-11 and press Enter/Return: ")
    if me_mp4_options_menu == 1:
        wmv_toggle_pcaudio()
    elif me_mp4_options_menu == 2:
        wmv_toggle_chat_box()
    elif me_mp4_options_menu == 3:
        wmv_toggle_webcam_video()
    elif me_mp4_options_menu == 4:
        wmv_toggle_largeroutline()
    elif me_mp4_options_menu == 5:
        wmv_change_videocodec()
    elif me_mp4_options_menu == 6:
        wmv_change_audiocodec()
    elif me_mp4_options_menu == 7:
        wmv_alter_videoformat()
    elif me_mp4_options_menu == 8:
        wmv_alter_audioformat()
    elif me_mp4_options_menu == 9:
        wmv_change_keyframes()
    elif me_mp4_options_menu == 10:
        wmv_change_maxstream()
    elif me_mp4_options_menu == 11:
        options_menu()
    else:
        clear_screen()
        print("Please enter a valid number from 1 to 11!")
        input("\n Press Enter/Return to continue...")
        mp4_options_menu()


# Lists settings available for the WMV file format


def swf_options_menu():
    pass


# Lists settings available for the SWF file format


def global_options_menu():
    pass


# Lists settings available for all of the file formats


def restore_default_settings():
    init_script()


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
