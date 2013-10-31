Option Explicit

Main

Sub Main 
Dim Path 
Dim a: a = ListDir("c:\Webex\*.arf") 
Dim FileName 
Dim FileName1 
Dim FileName2 
Dim mp4 
Dim wmv 
Dim objFSO 
Dim objFile 
Dim objTextFile 
Dim WSHShell 
Dim StrCMDLine 
Dim d: d = ListDir("c:\Webex\*.cfg") 
Set WSHShell = CreateObject("WScript.Shell") 
For Each FileName In d 
Set objFSO = CreateObject("Scripting.FileSystemObject") 
objFSO.DeleteFile(Filename) 
Next 
For Each FileName In a 
mp4 = 0 
wmv = 0 
'WScript.Echo FileName 
'WScript.Echo Left(Filename,(Len(Filename)-4)) 
Dim b: b = ListDir(Left(Filename,(Len(Filename)-4))+".mp4") 
For Each FileName1 In b 
'WScript.Echo FileName1 
mp4 = 1 
Next 
Dim c: c = ListDir(Left(Filename,(Len(Filename)-4))+".wmv") 
For Each FileName2 In c 
'WScript.Echo FileName2 
wmv = 1 
Next 
If mp4 = 0 then 
Set objFSO = CreateObject("Scripting.FileSystemObject") 
Set objTextFile = objFSO.CreateTextFile(Left(Filename,(Len(Filename)-4))+"-mp4.cfg") 
objTextFile.WriteLine("") 
objTextFile.WriteLine("[Console]") 
objTextFile.WriteLine("inputfile="+Filename) 
objTextFile.WriteLine("media=MP4") 
objTextFile.WriteLine("showui=0") 
objTextFile.WriteLine("[UI]") 
objTextFile.WriteLine("chat=0") 
objTextFile.WriteLine("qa=0") 
objTextFile.WriteLine("largeroutline=1") 
objTextFile.WriteLine("[MP4]") 
objTextFile.WriteLine("outputfile="+Left(Filename,(Len(Filename)-4))+".mp4") 
objTextFile.WriteLine("width=1024") 
objTextFile.WriteLine("height=768") 
objTextFile.WriteLine("framerate=8") 
objTextFile.Close 
End If 
If wmv = 0 then 
Set objFSO = CreateObject("Scripting.FileSystemObject") 
Set objTextFile = objFSO.CreateTextFile(Left(Filename,(Len(Filename)-4))+"-wmv.cfg") 
objTextFile.WriteLine("[Console]") 
objTextFile.WriteLine("inputfile="+Filename) 
objTextFile.WriteLine("media=WMV") 
objTextFile.WriteLine("showui=0") 
objTextFile.WriteLine("PCAudio=0") 
objTextFile.WriteLine("[UI]") 
objTextFile.WriteLine("largeroutline=0") 
objTextFile.WriteLine("[WMV]") 
objTextFile.WriteLine("outputfile="+Left(Filename,(Len(Filename)-4))+".wmv") 
objTextFile.WriteLine("width=1024") 
objTextFile.WriteLine("height=768") 
objTextFile.WriteLine("videocodec=Windows Media Video 9") 
objTextFile.WriteLine("audiocodec=Windows Media Audio 9.2 Lossless") 
objTextFile.WriteLine("videoformat=default") 
objTextFile.WriteLine("audioformat=default") 
objTextFile.WriteLine("videokeyframes=4") 
objTextFile.WriteLine("maxstream=1000") 
objTextFile.Close 
End If 
Next 
Dim e: e = ListDir("c:\Webex\*.cfg") 
For Each FileName In e 
Set objFSO = CreateObject("Scripting.FileSystemObject") 
StrCMDLine = "cmd /c C: & CD %windir% & C:\ProgramData\WebEx\WebEx\500\nbrplay.exe -Convert " + """" + FileName + """" + " & exit" 
'WScript.Echo StrCMDLine 
wshShell.run StrCMDLine ,0,True 
objFSO.DeleteFile(Filename) 
Next

End Sub

Public Function ListDir (ByVal Path) 
Dim fso: Set fso = CreateObject("Scripting.FileSystemObject") 
If Path = "" then Path = "*.*" 
Dim Parent, Filter 
if fso.FolderExists(Path) then ' Path is a directory 
Parent = Path 
Filter = "*" 
Else 
Parent = fso.GetParentFolderName(Path) 
If Parent = "" Then If Right(Path,1) = ":" Then Parent = Path: Else Parent = "." 
Filter = fso.GetFileName(Path) 
If Filter = "" Then Filter = "*" 
End If 
ReDim a(10) 
Dim n: n = 0 
Dim Folder: Set Folder = fso.GetFolder(Parent) 
Dim Files: Set Files = Folder.Files 
Dim File 
For Each File In Files 
If CompareFileName(File.Name,Filter) Then 
If n > UBound(a) Then ReDim Preserve a(n*2) 
a(n) = File.Path 
n = n + 1 
End If 
Next 
ReDim Preserve a(n-1) 
ListDir = a 
End Function

Private Function CompareFileName (ByVal Name, ByVal Filter) ' (recursive) 
CompareFileName = False 
Dim np, fp: np = 1: fp = 1 
Do 
If fp > Len(Filter) Then CompareFileName = np > len(name): Exit Function 
If Mid(Filter,fp) = ".*" Then ' special case: ".*" at end of filter 
If np > Len(Name) Then CompareFileName = True: Exit Function 
End If 
If Mid(Filter,fp) = "." Then ' special case: "." at end of filter 
CompareFileName = np > Len(Name): Exit Function 
End If 
Dim fc: fc = Mid(Filter,fp,1): fp = fp + 1 
Select Case fc 
Case "*" 
CompareFileName = CompareFileName2(name,np,filter,fp) 
Exit Function 
Case "?" 
If np <= Len(Name) And Mid(Name,np,1) <> "." Then np = np + 1 
Case Else 
If np > Len(Name) Then Exit Function 
Dim nc: nc = Mid(Name,np,1): np = np + 1 
If Strcomp(fc,nc,vbTextCompare)<>0 Then Exit Function 
End Select 
Loop 
End Function

Private Function CompareFileName2 (ByVal Name, ByVal np0, ByVal Filter, ByVal fp0) 
Dim fp: fp = fp0 
Dim fc2 
Do ' skip over "*" and "?" characters in filter 
If fp > Len(Filter) Then CompareFileName2 = True: Exit Function 
fc2 = Mid(Filter,fp,1): fp = fp + 1 
If fc2 <> "*" And fc2 <> "?" Then Exit Do 
Loop 
If fc2 = "." Then 
If Mid(Filter,fp) = "*" Then ' special case: ".*" at end of filter 
CompareFileName2 = True: Exit Function 
End If 
If fp > Len(Filter) Then ' special case: "." at end of filter 
CompareFileName2 = InStr(np0,Name,".") = 0: Exit Function 
End If 
End If 
Dim np 
For np = np0 To Len(Name) 
Dim nc: nc = Mid(Name,np,1) 
If StrComp(fc2,nc,vbTextCompare)=0 Then 
If CompareFileName(Mid(Name,np+1),Mid(Filter,fp)) Then 
CompareFileName2 = True: Exit Function 
End If 
End If 
Next 
CompareFileName2 = False 
End Function
