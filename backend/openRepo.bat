set var=0
echo %var%
FOR /F "delims=" %%i IN ('cd Z:') DO SET var=%%i
echo %var%
IF %var% == Z:\ ( echo 'Already Opened' )
IF %var% == 0 (start pushd \\192.168.0.185\c)
