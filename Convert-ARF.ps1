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
    # Convert to an MP4 file
    [Parameter(
        Mandatory = $false,
        ParameterSetName = "MP4"
    )]
    [Switch]$MP4 = $false,
    # Convert to an WMV file
    [Parameter(
        Mandatory = $false,
        ParameterSetName = "WMV"
    )]
    [Switch]$WMV = $false,
    # Convert to an SWF file
    [Parameter(
        Mandatory = $false,
        ParameterSetName = "SWF"
    )]
    [Switch]$SWF = $false,
    # Path to the ARF source directory.
    # The default is the current working directory.
    # Validates that path specified is a directory
    [Parameter(
        Mandatory = $false,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true
    )]
    [ValidateNotNullOrEmpty()]
    [ValidateScript( { Test-Path $_ -PathType "Container" })]
    [System.String]$Path = ".\",
    # Path to the ARF destination directory
    # The default is the current working directory
    # Validates that path specified is a directory
    [Parameter(
        Mandatory = $false,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true
    )]
    [ValidateNotNullOrEmpty()]
    [ValidateScript( { Test-Path $_ -PathType "Container" })]
    [System.String]$Destination = ".\",
    # Path to the NBR Player executable
    # Validates if the path is a leaf as the executable will be a leaf
    [Parameter(
        Mandatory = $false,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true
    )]
    [ValidateNotNullOrEmpty()]
    [ValidateScript( { Test-Path $_ -PathType "Leaf" })]
    [System.String]$NBRPath
)

function Test-Prerequisite {
    <#
    .SYNOPSIS
        Checks if the pre-requisites are installed on the machine
    .DESCRIPTION
        Long description
    .EXAMPLE
        PS C:\> <example usage>
        Explanation of what the example does
    .INPUTS
        Inputs (if any)
    .OUTPUTS
        System.Boolean
    .NOTES
        General notes
    #>

    if (Test-Path -Path "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe") {
        $NBRPath = "C:\Program Files (x86)\Webex\Webex\500\nbrplay.exe"
    } elseif (Test-Path -Path "C:\Program Files\Webex\Webex\500\nbrplay.exe") {
        $NBRPath = "C:\Program Files\Webex\Webex\500\nbrplay.exe"
    } else {
        Write-Error "NBR Player not found. Please specify the location of nbrplay.exe.
        Use the -NBRPath parameter to achieve this."
        return $false
    # Check to see if the script is running on Windows
    # Throw an error if it isn't
    if ($PSVersionTable.Platform -ne "Win32NT") {
        # Write an error to the console host
        Write-Warning -Message "This is only supported on Windows, running this on other platforms is at your own risk!"
    }
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


if ($CLIMode) {
    # Execute script as CLI mode
}