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
    $MP4,
    $WMV,
    $SWF
)

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
        [Parameter(
            Mandatory=$true,
            Position=0,
            ValueFromPipeline=$true,
            ValueFromPipelineByPropertyName=$true
        )]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({
            foreach ($Key in $_.Keys) {
                if (($key -Is [System.String]) -and ($_[$key] -Is [System.String])) {
                    continue
                } elseif (($key -Is [System.String]) -and ($_[$key] -Is [System.Collections.HashTable])) {
                    foreach ($SubKey in $_[$key].Keys) {
                        if (($SubKey -Is [System.String]) -and ($_[$key][$SubKey] -Is [System.String])) {
                            continue
                        } else {
                            return $false
                        }
                    }
                } else {
                    return $false
                }
            }
            return $true
        })]
        [System.Collections.HashTable]$InputObject,
        [Parameter(
            Mandatory=$true,
            Position=1,
            ValueFromPipeline=$true,
            ValueFromPipelineByPropertyName=$true
        )]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({})]
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
                    } else {
                        Add-Content -Path $Path -Value "$SubKey=$($InputObject[$Key][$SubKey])"
                    }
                }

                # Add white space to bottom of file.
                Add-Content -Path $Path -Value ""
            # If the key value pair does not contain a HashTable, treat it as just key and values with no section header.
            } else {
                # Write the key value pairs to the specified file.
                Add-Content -Path $Path -Value "$Key=$($InputObject[$Key])"
            }
        }
    }

    # Build the global config section of the config file
    #     $GlobalConfig = "
    # [Console]
    # inputfile=$InputFile
    # media=$FileType
    # showui=$([int]$ShowUI)
    # PCAudio=$([int]$PCAudio)
    # [UI]
    # chat=1
    # qa=1
    # "
}

function ConvertFrom-CiscoARF {
    <#
    .SYNOPSIS
        Short description
    .DESCRIPTION
        Long description
    .EXAMPLE
        Example of how to use this cmdlet
    .EXAMPLE
        Another example of how to use this cmdlet
    .INPUTS
        Inputs to this cmdlet (if any)
    .OUTPUTS
        Output from this cmdlet (if any)
    .NOTES
        General notes
    .COMPONENT
        The component this cmdlet belongs to
    .ROLE
        The role this cmdlet belongs to
    .FUNCTIONALITY
        The functionality that best describes this cmdlet
#>
    [CmdletBinding(DefaultParameterSetName = 'Parameter Set 1',
        SupportsShouldProcess = $true,
        PositionalBinding = $false,
        HelpUri = 'http://www.microsoft.com/',
        ConfirmImpact = 'Medium')]
    [Alias()]
    [OutputType([String])]
    Param (
        # Param1 help description
        [Parameter(Mandatory = $true,
            Position = 0,
            ValueFromPipeline = $true,
            ValueFromPipelineByPropertyName = $true,
            ValueFromRemainingArguments = $false,
            ParameterSetName = 'Parameter Set 1')]
        [ValidateNotNull()]
        [ValidateNotNullOrEmpty()]
        [ValidateCount(0, 5)]
        [ValidateSet("sun", "moon", "earth")]
        [Alias("p1")]
        $Param1,

        # Param2 help description
        [Parameter(ParameterSetName = 'Parameter Set 1')]
        [AllowNull()]
        [AllowEmptyCollection()]
        [AllowEmptyString()]
        [ValidateScript( { $true })]
        [ValidateRange(0, 5)]
        [int]
        $Param2,

        # Param3 help description
        [Parameter(ParameterSetName = 'Another Parameter Set')]
        [ValidatePattern("[a-z]*")]
        [ValidateLength(0, 15)]
        [String]
        $Param3
    )

    begin {
    }

    process {
        if ($pscmdlet.ShouldProcess("Target", "Operation")) {

        }
    }

    end {
    }
}

if ($MyInvocation.Line -NotMatch "^\.\s") {
    # run script in CLI mode, not dot sourced - standalone
}