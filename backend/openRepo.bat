set var=0
FOR /F "delims=" %%i IN ('cd Z:') DO SET var=%%i
IF %var% == Z:\ ( echo 'Already Opened' )
IF %var% == 0 (start pushd \\192.168.0.185\c)
