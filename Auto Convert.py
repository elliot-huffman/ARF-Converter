from os import path
from os import chdir
from os import listdir
from subprocess import call
from platform import system
from webbrowser import open_new_tab


# Variables naming convention:
# Variables for menus are prefixed with me_
# Variables for the MP4 section are prefixed with m_
# Variables for the WMV section are prefixed with w_
# Variables for the SWF section are prefixed with s_


def init_script():
    path_to_file = path.abspath(__file__)
    directory_name = path.dirname(path_to_file)
    chdir(directory_name)
    nbr_path = "C:\programdata\webex\webex\\500\\nbrplay.exe"
    global nbr_path


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
    if check_for_nbr(nbr_path) == False:
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
                print("This script requires the Network Broadcast Recording player to operate.\nPlease have it installed for the next time you run this script.")
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
        convert_to_mp4()
    elif me_main_menu == 2:
        file_type("wmv")
        convert_to_wmv()
    elif me_main_menu == 3:
        file_type("swf")
        convert_to_swf()
    elif me_main_menu == 4:
        options_menu()
    elif me_main_menu == 5:
        exit_program(True)


# Creates the main menu for the user to navigate.


def file_type(ftype):
    file_type = ftype
    global file_type


# Sets the file type to be converted to.


def convert_to_mp4():
    pass
    # for file in listdir("."):
    #     if path.isfile(file) and file[-3:].lower() == "arf":
    #         print("file")


# Converts the ARF file(s) to MP4


def convert_to_wmv():
    pass


# Converts the ARF file(s) to WMV


def convert_to_swf():
    pass


# Converts the ARF file(s) to SWF


def options_menu():
    clear_screen()
    print("Here you can change options for the conversion. You have 6 options to chose from:")
    print("\n1. MP4 Options")
    print("2. WMV Options")
    print("3. SWF Options")
    print("4. Global Options (applies to all formats)")
    print("\n5. Restore default settings")
    print("\n6. Go back to the main menu")
    me_options_menu = input("\nEnter your selection here (1-5)")
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


# Creates the options menu for the user to navigate.


def mp4_options_menu():
    pass


# Lists settings available for the MP4 file format


def wmv_options_menu():
    pass


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
    if friendly == True:
        print("Thank you for using this script, I hope you enjoyed it!")
    else:
        print("Thank you for considering this product! If you have any issues please email thelich2@gmail.com or\n file an issue on Github\n\nThanks!")
    exit()


# This is a simple program closer that thanks the user for using the program.
