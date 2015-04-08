from os import path
from subprocess import call
from platform import system
from webbrowser import open_new_tab


# Variables naming convention:
# Variables for menus are prefixed with me_
# Variables for the MP4 section are prefixed with m_
# Variables for the WMV section are prefixed with w_
# Variables for the SWF section are prefixed with s_


def init_script():
    nbr_path = "C:\programdata\webex\webex\\500\\nbrplay.exe"
    global nbr_path

# initializes the script with default values.

def clear_screen():
    if system() == "Windows":
        call("cls")
    elif system() == "Darwin" or system() == "Linux":
        call("clear")

# Sets up a multi platform clear screen function for Windows, OS X and Linux

def check_for_nbr(path_to_nbr):
    result = path.exists(path_to_nbr)
    return result

# Checks for the nbr.exe at the provided location.

def locate_nbr():
    if check_for_nbr(nbr_path) == False:
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
                exit_program()
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
    print("Please enter the path here")
    nbr_path = input("(E.G. C:\\foo\\bar\\nbr.exe): ")
    global nbr_path

# Sets the nbr_path variable to the user provided path.

def exit_program():
    clear_screen()
    print("Thank you for using this script, I hope you enjoyed it!")
    exit()

# this is a simple program closer that thanks the user for using the program.
