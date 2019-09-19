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
.NOTES
    This script only runs on Windows currently
#>

# [OutputType([System.String])]
[CmdletBinding(DefaultParameterSetName = 'MP4')]
param (
    $MP4,
    $WMV,
    $SWF
)

function Test-Prerequisite {
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

function New-Config {
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
}

function ConvertFrom-ARF {
    <#
    .SYNOPSIS
        Convert the ARF file to the specified type
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
}

if ($MyInvocation.Line -NotMatch "^\.\s") {
    # run script in CLI mode, not dot sourced - standalone
}