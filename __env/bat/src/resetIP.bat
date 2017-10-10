echo off

PUSHD "%~dp0"
echo loading config

set iniName=resetIP.ini
set session=%~1

call read_ini.cmd %iniName% %session% addr
set addr=%retVal%

call read_ini.cmd %iniName% %session% mask
set mask=%retVal%

call read_ini.cmd %iniName% %session% gateway
set gateway=%retVal%

call read_ini.cmd %iniName% %session% dns1
set dns1=%retVal%

call read_ini.cmd %iniName% %session% dns2
set dns2=%retVal%

set name="ÒÔÌ«Íø"

echo setting DNS1=%dns1%
netsh interface ip set dns name=%name% source=static addr=%dns1% register=primary

echo setting DNS2=%dns2%
netsh interface ip add dns name=%name% addr=%dns2% index=2

echo setting addr=%addr% mask=%mask% gateway=%gateway%
netsh interface ip set address name=%name% source=static addr=%addr% mask=%mask% gateway=%gateway%

echo setting End

set iniName=
set session=

set addr=
set mark=
set gateway=
set dns1=
set dns2=

set name=

::pause