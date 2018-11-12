from os import path, chdir, listdir, makedirs, remove
from subprocess import call
from platform import system
from webbrowser import open_new_tab


# Variables naming convention:
# Variables for menus are prefixed with me_
# Variables for the MP4 section are prefixed with m_
# Variables for the WMV section are prefixed with w_
# Variables for the SWF section are prefixed with s_

class init_system:
    def __init__(self):
        self.init_vars = {"path_to_file": path.abspath(__file__),
        "nbr_path": path.normpath("C:/ProgramData/WebEx/WebEx/500/nbrplay.exe"),
        "file_type": "mp4",
        "showui": 0,
        "need_ui_section": 1,
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
        self.check_os()
        self.locate_nbr()

    def check_os(self):
        if system() != "Windows":
            clear_screen()
            print("Please use Windows for file conversions.\nOther OSs are currently not supported :-(")
            exit_program(False)
    # Checks the operating system to see if it is compatible. If not, it displays an error and quits the program.


    def locate_nbr(self):
        if not self.check_file_existance(self.init_vars["nbr_path"]):
            print("The system could not find the NBR player.\nWould you like to download it?")
            me_locate_nbr = str(input("\nY or N: "))
            if me_locate_nbr.lower() == "y":
                open_new_tab("www.webex.com/play-webex-recording.html")
                exit()
            elif me_locate_nbr.lower() == "n":
                clear_screen()
                print("Maybe we missed it...\nDo you have the NBR player installed already?")
                me_nbr_already_installed = str(input("Y or N: "))
                if me_nbr_already_installed == "y":
                    self.custom_nbr_location()
                    self.locate_nbr()
                else:
                    clear_screen()
                    print("This script requires the Network Broadcast Recording player to operate.")
                    print("Please have it installed for the next time you run this script.")
                    input("\nPress Enter/Return to continue...")
                    exit_program(False)
        else:
            return True

    # If the nbr.exe is not at the default location, asks user where it is. If not installed asks user if the user wishes to
    # download the program. If the user does not want to then it stops the script and tells the user that it is required.


    def check_file_existance(self, file_path):
        result = path.exists(file_path)
        return result
    # Checks the given file path to see if the file exists and returns true or false.


    def custom_nbr_location(self):
        clear_screen()
        print("Please enter the path to the nbrplay.exe here")
        self.init_vars["nbr_path"] = input("\n(E.G. C:\\foo\\bar\\nbrplay.exe): ")
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
        # 0 = a, ok!
        # 5 = input
        # 4 = output
        # 9 = input and output


# Sets up the initial variables and checks for system compatibility. Also houses generic core functions.


def clear_screen():
    if system() == "Windows":
        call("cls", shell=True)
    elif system() == "Darwin" or system() == "Linux":
        call("clear", shell=True)


# Sets up a multi platform clear screen function for Windows, OS X and Linux


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
        vars_system.init_vars["file_type"] = "mp4"
        convert_file()
    elif me_main_menu == 2:
        vars_system.init_vars["file_type"] = "wmv"
        convert_file()
    elif me_main_menu == 3:
        vars_system.init_vars["file_type"] = "swf"
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


def convert_file():
    if vars_system.check_folder() == 5:
        print("The ARF input dir is invalid, please check that it exists.")
        input("\n Press Enter/Return to return to the main menu...")
        main_menu()
    if vars_system.check_folder() == 4:
        print("The ARF output dir is invalid, please check that it exists.")
        input("\n Press Enter/Return to return to the main menu...")
        main_menu()
    if vars_system.check_folder() == 9:
        print("The ARF input and output dir is invalid, please check that they exist.")
        input("\n Press Enter/Return to return to the main menu...")
        main_menu()
    cfg_counter = 0
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            remove(file)
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "arf":
            create_configs(file)
            cfg_counter += 1
    for file in listdir("."):
        if path.isfile(file) and file[-3:].lower() == "cfg":
            clear_screen()
            print("%s Files left to convert. This may take a while..." % str(cfg_counter))
            execute_nbr_conversion(vars_system.init_vars["input_file_dir"] + "\\" + file)
            cfg_counter -= 1
            remove(file)
    convert_again()


# Deletes CFG files already present in the selected/default folder then creates new config files. After the cfg creation
# is complete, the NBR player is executed with the new cfg files for reference while the remaining files are counted
# down.


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
        if vars_system.init_vars["need_ui_section"] == 1:
            config_file.write("\n[UI]")
        if vars_system.init_vars["file_type"].lower() == "mp4":
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
        elif vars_system.init_vars["file_type"].lower() == "wmv":
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


def convert_again():
    clear_screen()
    print("The conversion is finished.")
    print("Would you like to run another bulk conversion?")
    me_convert_again = input("\nType Y for yes and N for no then press Enter/Return to continue: ")
    if me_convert_again.lower() == "y":
        main_menu()
    else:
        exit_program(True)


# Asks the user if they would like to convert another batch of files.


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
    print("3. Toggle Largeroutline\n4. Change frame rate\n\n5. Go back to the main options menu.")
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
    clear_screen()
    print("The Q&A box toggle is set to: %s" % vars_system.init_vars["m_ui_chat"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_chat = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_chat.lower() == "y":
        if vars_system.init_vars["m_ui_chat"] == 1:
            vars_system.init_vars["m_ui_chat"] = 0
        else:
            vars_system.init_vars["m_ui_chat"] = 1
        clear_screen()
        print("The Q&A box toggle is now set to: %s" % vars_system.init_vars["m_ui_chat"])
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the chat box setting for MP4 files.


def mp4_toggle_qa():
    clear_screen()
    print("The Q&A box toggle is set to: %s" % vars_system.init_vars["m_ui_qa"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_qa = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_qa.lower() == "y":
        if vars_system.init_vars["m_ui_qa"] == 1:
            vars_system.init_vars["m_ui_qa"] = 0
        else:
            vars_system.init_vars["m_ui_qa"] = 1
        clear_screen()
        print("The Q&A box toggle is now set to: %s" % vars_system.init_vars["m_ui_qa"])
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the Q&A box setting for MP4 files.


def mp4_toggle_largeroutline():
    clear_screen()
    print("The LargerOutline toggle is set to: %s" % vars_system.init_vars["m_ui_largeroutline"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_mp4_toggle_largeroutline = input("Press Enter/Return when you are ready to continue: ")
    if me_mp4_toggle_largeroutline.lower() == "y":
        if vars_system.init_vars["m_ui_largeroutline"] == 1:
            vars_system.init_vars["m_ui_largeroutline"] = 0
        else:
            vars_system.init_vars["m_ui_largeroutline"] = 1
        clear_screen()
        print("The LargerOutline toggle is now set to: %s" % vars_system.init_vars["m_ui_largeroutline"])
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Toggles the LargerOutline setting for MP4 files.


def mp4_change_framerate():
    clear_screen()
    print("The current frame rate is set to: %sFPS.\nLeave it blank to do nothing." % vars_system.init_vars["m_framerate"])
    print("Enter a number above 0 (the recommended range is 1 to 10) to change the setting.")
    me_mp4_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_mp4_change_framerate > 0:
        vars_system.init_vars["m_framerate"] = me_mp4_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % vars_system.init_vars["m_framerate"])
        input("Press Enter/Return to continue...")
    mp4_options_menu()


# Changes the frame rate for MP4 files.


def wmv_options_menu():
    clear_screen()
    print("WMV Files have 10 configurable options (at the moment)\n\n1. Toggle PCAudio setting\n2. Toggle Chat Box")
    print("3. Toggle Webcam Video\n4. Toggle Largeroutline setting\n5. Change the video codex")
    print("6. Change the audio codex\n7. Alter the Videoformat setting\n8. Alter the Audioformat setting")
    print("9. Change the video key frames (frame rate)\n10. Change the maxstream (bit rate)")
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
    clear_screen()
    print("The PCAudio toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["w_console_pcaudio"])
    print("This is an experimental and untested setting!!!")
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_pcaudio = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_pcaudio.lower() == "y":
        if vars_system.init_vars["w_console_pcaudio"] == 1:
            vars_system.init_vars["w_console_pcaudio"] = 0
        else:
            vars_system.init_vars["w_console_pcaudio"] = 1
        clear_screen()
        print("The PCAudio toggle is now set to: %s" % vars_system.init_vars["w_console_pcaudio"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Enables or Disables the PCAudio setting for the WMV file


def wmv_toggle_chat_box():
    clear_screen()
    print("The chat box toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["w_ui_chat"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_chat_box = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_chat_box.lower() == "y":
        if vars_system.init_vars["w_ui_chat"] == 1:
            vars_system.init_vars["w_ui_chat"] = 0
        else:
            vars_system.init_vars["w_ui_chat"] = 1
        clear_screen()
        print("The chat box toggle is now set to: %s" % vars_system.init_vars["w_ui_chat"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the chat box setting for WMV files.


def wmv_toggle_webcam_video():
    clear_screen()
    print("The web cam box toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["w_ui_video"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_video_box = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_video_box.lower() == "y":
        if vars_system.init_vars["w_ui_video"] == 1:
            vars_system.init_vars["w_ui_video"] = 0
        else:
            vars_system.init_vars["w_ui_video"] = 1
        clear_screen()
        print("The web cam toggle is now set to: %s" % vars_system.init_vars["w_ui_video"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the web cam box setting for WMV files.


def wmv_toggle_largeroutline():
    clear_screen()
    print("The LargerOutline toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["w_ui_largeroutline"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_wmv_toggle_largeroutline = input("Press Enter/Return when you are ready to continue: ")
    if me_wmv_toggle_largeroutline.lower() == "y":
        if vars_system.init_vars["w_ui_largeroutline"] == 1:
            vars_system.init_vars["w_ui_largeroutline"] = 0
        else:
            vars_system.init_vars["w_ui_largeroutline"] = 1
        clear_screen()
        print("The LargerOutline toggle is now set to: %s" % vars_system.init_vars["w_ui_largeroutline"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Toggles the LargerOutline setting for WMV files.


def wmv_change_videocodec():
    clear_screen()
    print("The WMV video codex is currently set to: %s" % vars_system.init_vars["w_videocodec"])
    print("There are 2 options for this setting:\n1. Windows Media Video 9\n2. Windows Media Video 9 Screen")
    print("\nLeave the field blank to do nothing")
    me_wmv_videocodec = int(input("\nPlease enter 1 or 2 then press Enter/Return: "))
    if me_wmv_videocodec == int:
        if me_wmv_videocodec == 1:
            vars_system.init_vars["w_videocodec"] = "Windows Media Video"
        elif me_wmv_videocodec == 2:
            vars_system.init_vars["w_videocodec"] = "Windows Media Video 9 Screen"
        clear_screen()
        print("The video codex is now set to: %s" % vars_system.init_vars["w_videocodec"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the Video Codex for WMV files.


def wmv_change_audiocodec():
    clear_screen()
    print("The WMV audio codex is currently set to: %s" % vars_system.init_vars["w_audiocodec"])
    print("There are 3 options for this setting:\n1. Windows Media Audio 9.2 9\n2. Windows Media Audio 9.2 Lossless")
    print("3. Windows Media Audio 10 Professional\nLeave the field blank to do nothing")
    me_wmv_audiocodec = int(input("\nPlease enter 1-3 then press Enter/Return: "))
    if me_wmv_audiocodec == 1:
        vars_system.init_vars["w_audiocodec"] = "Windows Media Video"
    elif me_wmv_audiocodec == 2:
        vars_system.init_vars["w_audiocodec"] = "Windows Media Video 9 Screen"
    elif me_wmv_audiocodec == 3:
        vars_system.init_vars["w_audiocodec"] = "Windows Media Audio 10 Professional"
    clear_screen()
    print("The audio codex is now set to: %s" % vars_system.init_vars["w_audiocodec"])
    input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the Audio Codex for WMV files.


def wmv_alter_videoformat():
    clear_screen()
    print("I have no idea what this setting does so I do not recommend changing this.")
    print("Leave the field blank to do nothing.\n The current setting is: %s" % vars_system.init_vars["w_videoformat"])
    me_wmv_videoformat = input("Enter some value here: ")
    if len(me_wmv_videoformat) > 0:
        vars_system.init_vars["w_videoformat"] = me_wmv_videoformat
        clear_screen()
        print("The VideoFormat setting is now set to: %s" % vars_system.init_vars["w_videoformat"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the VideoFormat for WMV files.


def wmv_alter_audioformat():
    clear_screen()
    print("I have no idea what this setting does so I do not recommend changing this.")
    print("Leave the field blank to do nothing.\n The current setting is: %s" % vars_system.init_vars["w_audioformat"])
    me_wmv_audioformat = input("Enter some value here: ")
    if len(me_wmv_audioformat) > 0:
        vars_system.init_vars["w_audioformat"] = me_wmv_audioformat
        clear_screen()
        print("The AudioFormat setting is now set to: %s" % vars_system.init_vars["w_audioformat"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the AudioFormat for WMV files.


def wmv_change_keyframes():
    clear_screen()
    print("The current frame rate is set to: %sFPS.\nLeave it blank to do nothing." % vars_system.init_vars["w_videokeyframes"])
    print("Enter a number above 0 (the recommended range is 4 to 10) to change the setting.")
    me_wmv_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_wmv_change_framerate > 0:
        vars_system.init_vars["w_videokeyframes"] = me_wmv_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % vars_system.init_vars["w_videokeyframes"])
        input("Press Enter/Return to continue...")
    wmv_options_menu()


# Changes the KeyFrames for WMV files.


def wmv_change_maxstream():
    clear_screen()
    print("The current MaxStream is set to: %sBPS.\nLeave it blank to do nothing." % vars_system.init_vars["w_maxstream"])
    print("Enter a number above 0 (the recommended range is 500 to 1000) to change the setting.")
    me_wmv_change_maxstream = int(input("Press Enter/Return when you are ready to continue: "))
    if me_wmv_change_maxstream > 0:
        vars_system.init_vars["w_maxstream"] = me_wmv_change_maxstream
        clear_screen()
        print("MaxStream is now set to: %s" % vars_system.init_vars["w_maxstream"])
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
    clear_screen()
    print("The PCAudio toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["s_console_pcaudio"])
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_swf_toggle_pcaudio = input("Press Enter/Return when you are ready to continue: ")
    if me_swf_toggle_pcaudio.lower() == "y":
        if vars_system.init_vars["s_console_pcaudio"] == 1:
            vars_system.init_vars["s_console_pcaudio"] = 0
        else:
            vars_system.init_vars["s_console_pcaudio"] = 1
        clear_screen()
        print("The PCAudio toggle is now set to: %s" % vars_system.init_vars["s_console_pcaudio"])
        input("Press Enter/Return to continue...")
    swf_options_menu()


# Enables or Disables the PCAudio setting for the SWF file


def swf_change_framerate():
    clear_screen()
    print("The current frame rate is set to: %sFPS. Leave below blank to do nothing." % vars_system.init_vars["s_framerate"])
    print("Enter a number above 0 to change the frame rate (the recommended range is from 1 to 10).")
    me_swf_change_framerate = int(input("Press Enter/Return when you are ready to continue: "))
    if me_swf_change_framerate > 0:
        vars_system.init_vars["s_framerate"] = me_swf_change_framerate
        clear_screen()
        print("The frame rate is now set to: %sFPS" % vars_system.init_vars["s_framerate"])
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
        global_output_dir()
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
    clear_screen()
    print("This sets the directory that contains all of the ARFs to be converted. By default this setting is the same")
    print("as the directory that this script file is in.")
    print("The current input dir is: %s" % vars_system.init_vars["input_file_dir"])
    print("\nEnter the full path to the directory that contains the ARF files to be converted or blank to do nothing.")
    me_global_input_dir = input("Press Enter/Return when you are ready to continue: ")
    if len(me_global_input_dir) > 0:
        vars_system.init_vars["input_file_dir"] = me_global_input_dir
        clear_screen()
        print("The input directory is now set to: %s" % vars_system.init_vars["input_file_dir"])
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Sets the directory that contains all of the ARF files to be converted.


def global_toggle_showui():
    clear_screen()
    print("The ShowUI toggle is set to: %s\n Would you like to toggle this setting?" % vars_system.init_vars["showui"])
    print("This option is experimental, I would not recommend changing this until tested.")
    print("\nPress Y to toggle the setting. Leave it blank to do nothing.")
    me_global_toggle_showui = input("Press Enter/Return when you are ready to continue: ")
    if me_global_toggle_showui.lower() == "y":
        if vars_system.init_vars["showui"] == 1:
            vars_system.init_vars["showui"] = 0
        else:
            vars_system.init_vars["showui"] = 1
        clear_screen()
        print("The ShowUI toggle is now set to: %s" % vars_system.init_vars["showui"])
        input("Press Enter/Return to continue...")
    global_options_menu()


# Toggles the ShowUI setting for all file types.


def global_output_dir():
    clear_screen()
    print("This sets the directory that will contain all of the converted ARFs. By default this setting is .\\Converted")
    print("The current output dir is: %s" % vars_system.init_vars["output_file_dir"])
    print("\nEnter the full path to the directory that will contain the converted ARF files or blank to do nothing.")
    me_global_output_dir = input("Press Enter/Return when you are ready to continue: ")
    if len(me_global_output_dir) > 0:
        vars_system.init_vars["output_file_dir"] = me_global_output_dir
        clear_screen()
        print("The output directory is now set to: %s" % vars_system.init_vars["output_file_dir"])
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Sets the directory that will contain all of the converted ARF files after conversion.


def global_set_res_width():
    clear_screen()
    print("This sets the resolution width for the converted file.")
    print("The resolution width is currently set to: %spx" % vars_system.init_vars["width"])
    print("\nEnter a number(recommended values are 1024 and above). Leave blank to change nothing.")
    me_global_res_width = len(input("Press Enter/Return when you are ready to continue: "))
    if me_global_res_width > 0:
        vars_system.init_vars["width"] = me_global_res_width
        clear_screen()
        print("The resolution width is now set to: %s" % vars_system.init_vars["width"])
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Changes the output file's resolution width (the 1024 in 1024x768)


def global_set_res_height():
    clear_screen()
    print("This sets the resolution height for the converted file.")
    print("The resolution height is currently set to: %spx" % vars_system.init_vars["height"])
    print("\nEnter a number(recommended values are 768 and above). Leave blank to change nothing.")
    me_global_res_height = len(input("Press Enter/Return when you are ready to continue: "))
    if me_global_res_height > 0:
        vars_system.init_vars["height"] = me_global_res_height
        clear_screen()
        print("The resolution height is now set to: %s" % vars_system.init_vars["height"])
        input("\nPress Enter/Return to continue...")
    global_options_menu()


# Changes the output file's resolution height (the 768 in 1024x768)


def restore_default_settings():
    vars_system.__init__()
    options_menu()


# Restores all settings to default values


def exit_program(friendly):
    clear_screen()
    if friendly:
        print("Thank you for using this script, I hope you enjoyed it!")
    elif not friendly:
        print("Thank you for considering this product! If you have any issues please email ehuffman@elliot-labs.com or")
        print("file an issue on https://github.com/elliot-labs/ARF-Converter\n\nThanks!")
    else:
        print("You have triggered an exit that the programmer has not foreseen.")
        print("Please report this to ehuffman@elliot-labs.com or https://github.com/elliot-labs/ARF-Converter")
    exit()


# This is a simple program closer that thanks the user for using the program.


if __name__ == '__main__':
    vars_system = init_system()
    main_menu()


# Checks to see if it is the main program (not an import) and then starts madness!