FOR /F "tokens=* USEBACKQ" %%F IN (`cd Z:`) DO (
SET var=%%F
)
IF %var% == Z:\ (echo "opened") else start pushd \\192.168.0.185\c
