@echo off

%extd% /browseforfile "Select a file" "" "All Files (*.*)|*.*"

if "%result%"=="" (exit) else (set file="%result%")

%extd% /savefiledialog "Save file as" "" "All Files (*.*)|*.*"

if "%result%"=="" (exit) else (set save="%result%")

%extd% /inputbox "" "Enter the key" "mykey"

if "%result%"=="" (exit) else (set key="%result%")

%extd% /aesdecode %file% %save% %key%