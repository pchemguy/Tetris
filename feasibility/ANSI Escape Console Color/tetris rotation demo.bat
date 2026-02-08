@echo off

set "BL=."
set "CH=@"
set "CC=[103;93m%CH%[0m"


cls
echo Tetris Rotation:
echo == I ==
echo:
echo   R0
echo  y
echo x 0123
echo  0%BL%%BL%%BL%%BL%
echo  1%CC%%CC%%CC%%CC%
echo  2%BL%%BL%%BL%%BL%
echo  3%BL%%BL%%BL%%BL%
echo -------
echo:
timeout.exe /T 2 >nul

cls
echo Tetris Rotation:
echo == I ==
echo:
echo   R90
echo  y
echo x 0123
echo  0%BL%%BL%%CC%%BL%
echo  1%BL%%BL%%CC%%BL%
echo  2%BL%%BL%%CC%%BL%
echo  3%BL%%BL%%CC%%BL%
echo -------
echo:
timeout.exe /T 2 >nul

cls
echo Tetris Rotation:
echo == I ==
echo:
echo   R180
echo  y
echo x 0123
echo  0%BL%%BL%%BL%%BL%
echo  1%BL%%BL%%BL%%BL%
echo  2%CC%%CC%%CC%%CC%
echo  3%BL%%BL%%BL%%BL%
echo -------
echo:
timeout.exe /T 2 >nul

cls
echo Tetris Rotation:
echo == I ==
echo:
echo   R270
echo  y
echo x 0123
echo  0%BL%%CC%%BL%%BL%
echo  1%BL%%CC%%BL%%BL%
echo  2%BL%%CC%%BL%%BL%
echo  3%BL%%CC%%BL%%BL%
echo -------
echo:
timeout.exe /T 2 >nul

pause
