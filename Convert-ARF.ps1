<#
.SYNOPSIS
    Converts ARF files to the specified format.
.DESCRIPTION
    Long description
.EXAMPLE
    PS C:\> .\Convert-ARF.ps1
    Explanation of what the example does
.INPUTS
    Inputs (if any)
.OUTPUTS
    Output (if any)
.COMPONENT
    The component this cmdlet belongs to
.ROLE
    The user's company role this cmdlet is designed for
.FUNCTIONALITY
    The functionality that best describes this cmdlet
    ???
.LINK
    https://github.com/elliot-labs/PowerShell-Doodads
.NOTES
    This script only runs on Windows currently
#>

# [OutputType([System.String])]
[CmdletBinding(DefaultParameterSetName = 'MP4')]
param (
    [ValidateSet("MP4", "WMV", "SWF")]
    [System.String]$OutputType = "MP4"
)

begin {

    # Define the INI file configuration options class
    class Global_Options {
        [System.String]$InputFile
        [System.String]$OutputFile
        [System.String]$MediaType
        [System.Boolean]$ShowUI
        [System.Int64]$Width
        [System.Int64]$Height
    }
    class MP4_Options {
        [System.Boolean]$Chat
        [System.Boolean]$Video
        [System.Boolean]$QuestionAnswer
        [System.Boolean]$LargeOutLine = $True
        [System.Int64]$FrameRate
    }
    class WMV_Options {
        [System.Boolean]$PCAudio = $False
        [System.Boolean]$Chat = $False
        [System.Boolean]$Video = $False
        [System.Boolean]$LargerOutline = $True
        [System.String]$VideoCodec
        [System.String]$AudioCodec
        [System.String]$VideoFormat = "default"
        [System.String]$AudioFormat = "default"
        [System.Int64]$VideoKeyFrames
        [System.Int64]$MaxStream
    }
    class SWF_Options {
        [System.Boolean]$PCAudio = $True
        [System.Int64]$FrameRate
    }
    
    class INI_Options {
        [Global_Options]$GlobalOptions
        $FileTypeOptions

    # If there is no user input, test to see if the player is installed
    if ($null -eq $Path) {
        # Test to see if the NBR player executable is present in the 32bit program folder for 64bit Windows
        if (Test-Path -Path "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe") {
            $Path = "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe"
        }

        # Test to see if the NBR player executable is present in the program folder for 32bit Windows
        elseif (Test-Path -Path "C:\Program Files\Webex\Webex\500\nbrplay.exe") {
            $Path = "C:\Program Files\Webex\Webex\500\nbrplay.exe"
        }

        # Test to see if the NBR player executable is present legacy NBR location
        elseif (Test-Path -Path "C:\ProgramData\WebEx\WebEx\500\nbrplay.exe") {
            # Set the variable to be equal to the
            $Path = "C:\ProgramData\WebEx\WebEx\500\nbrplay.exe"
        }
    }

    function Test-NBRPrerequisite {
        <#
        .SYNOPSIS
            Checks if the pre-requisites are installed on the machine.
        .DESCRIPTION
            Tests to see if the NBR player is present on the system.
            Throws an error if it is not present stating that the user needs to specify the value themselves or install it on the system.
        .PARAMETER Path
            A path to the NBR player executable.
            Input is validated and will be returned if input is valid.
        .EXAMPLE
            PS C:\> Test-Prerequisite.
            Checks the system to see if NBR player is installed and if it is, it will return the path to the specific install location.
            If it is not installed, it will throw an error stating that the NBR player can't be found and has instruction on how to install it.
            If the system is not running windows, it will write a warning.
        .EXAMPLE
            PS C:\> Test-Prerequisite -Path "C:\Some\Path\nbrplay.exe"
            Check to see if the specified path is valid, if it is, it will return the same path specified.
            Since the parameter has validation, powershell itself will handle the error.
            If the system is not running windows, it will write a warning.
        .INPUTS
            System.String
        .OUTPUTS
            System.String
        .NOTES
            The nbr player can be installed from:
            https://www.webex.com/play-webex-recording.html
        #>
    
        # Define the parameter
        param (
            # Path to the NBR Player executable.
            # Validates if the path is a leaf as the executable will be a leaf.
            [Parameter(
                Mandatory = $false,
                ValueFromPipeline = $true,
                ValueFromPipelineByPropertyName = $true
            )]
            [ValidateNotNullOrEmpty()]
            [ValidateScript( { Test-Path $_ -PathType "Leaf" })]
            [System.String]$Path
        )
    
        # If there is no user input, test to see if the player is installed
        if ($null -eq $Path) {
            # Test to see if the NBR player executable is present in the 32bit program folder for 64bit Windows
            if (Test-Path -Path "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe") {
                $Path = "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe"
            }
    
            # Test to see if the NBR player executable is present in the program folder for 32bit Windows
            elseif (Test-Path -Path "C:\Program Files\Webex\Webex\500\nbrplay.exe") {
                $Path = "C:\Program Files\Webex\Webex\500\nbrplay.exe"
            }
    
            # Test to see if the NBR player executable is present legacy NBR location
            elseif (Test-Path -Path "C:\ProgramData\WebEx\WebEx\500\nbrplay.exe") {
                # Set the variable to be equal to the
                $Path = "C:\ProgramData\WebEx\WebEx\500\nbrplay.exe"
            }
    
            # If all check fail, notify the user that they have to specify the path themselves and halt execution
            else {
                # Terminate execution and return information on why execution was terminated
                throw "NBR Player not found. Please specify the location of nbrplay.exe.
    Use the -NBRPath parameter to achieve this.
    If it is not installed, please install it by going to www.webex.com/play-webex-recording.html"
            }
        }
    
        # Check to see if the script is running on Windows
        # Throw an error if it isn't
        if ($PSVersionTable.Platform -ne "Win32NT") {
            # Write an error to the console host
            Write-Warning -Message "This is only supported on Windows, running this on other platforms is at your own risk!"
        }
    
        # Return the path to the nbr player after validation has succeeded.
        return $Path
    }
    function Test-MP4Prerequisite {
        <#
        .SYNOPSIS
            Tests to see if the MP4 libraries are present.
        .DESCRIPTION
            Takes the specified path to the nbr install and validates if the MP4 libraries are installed or not.
            If it is not able to find the MP4 libs, it returns false, if it can find them it is successful.
        .PARAMETER NBRPath
            This parameter takes a path to the NBR player's installation directory.
            It validates that the specified path is present and is a directory.
            The correct directory has the "webex.exe" file located in it.
        .EXAMPLE
            PS C:\> Test-MP4Prerequisite -NBRPath "C:\Program Files (x86)\Webex\"
            Checks relative to the specified directory for the MP4 libs.
            If the plugin directory is not present then it creates the directory and returns false.
            If the plugin directory exists then the directory is checked for the appropriate DLLs.
            If the DLLs are indeed present then $true is returned.
        .INPUTS
            System.String
        .OUTPUTS
            System.Boolean
        .NOTES
            Returns $False if the required files could not be found.
            Returns $True if the required files could be found.
    
            Writes an error if it could not create the required folder for the MP4 DLLs.
            This is non terminating.
        #>
        
        #Requires -RunAsAdministrator
    
        param (
            [Parameter(
                Mandatory = $true,
                Position = 0,
                ValueFromPipeline = $true,
                ValueFromPipelineByPropertyName = $true,
                ValueFromRemainingArguments = $true
            )]
            [ValidateScript( { Test-Path "$_\webex.exe" -PathType "Leaf" })]
            [System.String]$NBRPath
        )
    
        process {
            # Checks to see if the Plugin directory is present before checking for the MP4 libraries.
            if (-not (Test-Path -Path "$NBRPath\Webex\500\Plugin" -PathType "Container")) {
    
                # Write warning messages to the end user if the the path doesn't exist.
                # This means that the correct directory would not exist and the user would need to set up the MP4 libs.
                Write-Warning -Message "The MP4 DLLs are not present, please download and place them into the plugin folder here: $NBRPath\Webex\500\Plugin"
                Write-Warning -Message "You can download the MP4 libraries here: https://cisco.bravais.com/s/0ovsmxyXiqUxhn0vSSUb"
                Write-Warning -Message "You can learn more here: https://help.webex.com/en-us/WBX56022/Prompted-to-Enter-URL-Account-Name-and-Password-when-Converting-an-NBR-to-MP4-Format"
    
                # Catch errors on directory creation so that errors can be handled gracefully.
                try {
                    # Create the Plugin folder for the end user to place the MP4 files into.
                    New-Item -Path "$NBRPath\Webex\500\Plugin" -ItemType "Directory"
                }
                catch {
                    # Could not create the directory for some reason, write an error.
                    Write-Error -Message "Failed to create the plugin directory."
                }
    
                # Return false indicating that the test has failed to find the required MP4 files.
                return $false
            }
            elseif (-not (Test-Path -Path "$NBRPath\Webex\500\Plugin\atgpcext.dll" -PathType "Leaf")) {
                # Write warning messages to the end user if the the path doesn't exist.
                # This means that the correct directory would not exist and the user would need to set up the MP4 libs.
                Write-Warning -Message "The Download Module DLL is not present, please download and place it into the plugin folder here: $NBRPath\Webex\500\Plugin"
                Write-Warning -Message "You can download the MP4 libraries here: https://cisco.bravais.com/s/0ovsmxyXiqUxhn0vSSUb"
                Write-Warning -Message "You can learn more here: https://help.webex.com/en-us/WBX56022/Prompted-to-Enter-URL-Account-Name-and-Password-when-Converting-an-NBR-to-MP4-Format"
                
                return $false
            }
            elseif (-not (Test-Path -Path "$NBRPath\Webex\500\Plugin\libfaac.dll" -PathType "Leaf")) {
                # Write warning messages to the end user if the the path doesn't exist.
                # This means that the correct directory would not exist and the user would need to set up the MP4 libs.
                Write-Warning -Message "The ffmpeg AAC DLL is not present, please download and place it into the plugin folder here: $NBRPath\Webex\500\Plugin"
                Write-Warning -Message "You can download the MP4 libraries here: https://cisco.bravais.com/s/0ovsmxyXiqUxhn0vSSUb"
                Write-Warning -Message "You can learn more here: https://help.webex.com/en-us/WBX56022/Prompted-to-Enter-URL-Account-Name-and-Password-when-Converting-an-NBR-to-MP4-Format"
                
                return $false
            }
            else {
                # Returns true if the required files are present.
                return $true
            }
        }    
    }
    function Export-INIConfiguration {
        <#
        .SYNOPSIS
            Creates the config files for the NBR player's conversion system
        .DESCRIPTION
            Long description
        .EXAMPLE
            PS C:\> <example usage>
            Explanation of what the example does
        .INPUTS
            Inputs (if any)
        .OUTPUTS
            Output (if any)
        .NOTES
            General notes
        #>
        param(
            [ValidateNotNullOrEmpty()]
            [ValidateScript( {
                    Test-Path -Path $_ -IsValid
                })]
            [System.String[]]$Path
        )
    
        begin { }
        process { }
        end {
            foreach ($Key in $InputObject.keys) {
                # If there is a hash table in the value section, make the key the section name and loop through the
                # sub keys and values to create the INI section's key and values.
                if ($InputObject[$Key] -Is [System.Collections.HashTable]) {
                    # Write the key value as the section name of the INI formatted
                    Add-Content -Path $Path -Value "[$Key]"
    
                    # Loop through the embedded HashTable and write the key and values to the file
                    foreach ($SubKey in ($InputObject[$Key].keys | Sort-Object)) {
                        if ($SubKey -match "^Comment[\d]+") {
                            Add-Content -Path $Path -Value "$($InputObject[$Key][$SubKey])"
                        }
                        else {
                            Add-Content -Path $Path -Value "$SubKey=$($InputObject[$Key][$SubKey])"
                        }
                    }
    
                    # Add white space to bottom of file.
                    Add-Content -Path $Path -Value ""
                    # If the key value pair does not contain a HashTable, treat it as just key and values with no section header.
                }
                else {
                    # Write the key value pairs to the specified file.
                    Add-Content -Path $Path -Value "$Key=$($InputObject[$Key])"
                }
            }
        }
    
        # Build the global config section of the config file
        #     $GlobalConfig = "
        # [Console]
        # InputFile=$InputFile
        # media=$FileType
        # ShowUI=$([int]$ShowUI)
        # PCAudio=$([int]$PCAudio)
        # [UI]
        # chat=1
        # qa=1
        # "
    }
    function ConvertFrom-CiscoARF {
        # Pass
    }
}

process {
    if ($MyInvocation.Line -NotMatch "^\.\s") {
        # run script in CLI mode, not dot sourced - standalone
    }
}

end {}