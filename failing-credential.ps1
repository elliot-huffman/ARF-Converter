[System.String]$Username = "Elliot"
[System.String]$Password = "QwertY123!@#"

ConvertTo-SecureString -String $Password -AsPlainText -Force
New-Object -TypeName "System.Management.Automation.PSCredential" -ArgumentList $Username,$Password
