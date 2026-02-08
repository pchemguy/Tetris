@echo off

echo [101;93m STYLES [0m
echo ^<ESC^>[0m [0mReset[0m
echo ^<ESC^>[1m [1mBold[0m
echo ^<ESC^>[4m [4mUnderline[0m
echo ^<ESC^>[7m [7mInverse[0m
echo:
echo [101;93m NORMAL FOREGROUND COLORS [0m
echo ^<ESC^>[30m [30mBlack[0m (black)
echo ^<ESC^>[31m [31mRed[0m
echo ^<ESC^>[32m [32mGreen[0m
echo ^<ESC^>[33m [33mYellow[0m
echo ^<ESC^>[34m [34mBlue[0m
echo ^<ESC^>[35m [35mMagenta[0m
echo ^<ESC^>[36m [36mCyan[0m
echo ^<ESC^>[37m [37mWhite[0m
echo:
echo [101;93m NORMAL BACKGROUND COLORS [0m
echo ^<ESC^>[40m [40mBlack[0m
echo ^<ESC^>[41m [41mRed[0m
echo ^<ESC^>[42m [42mGreen[0m
echo ^<ESC^>[43m [43mYellow[0m
echo ^<ESC^>[44m [44mBlue[0m
echo ^<ESC^>[45m [45mMagenta[0m
echo ^<ESC^>[46m [46mCyan[0m
echo ^<ESC^>[47m [47mWhite[0m (white)
echo:
echo [101;93m STRONG FOREGROUND COLORS [0m
echo ^<ESC^>[90m [90mWhite[0m
echo ^<ESC^>[91m [91mRed[0m
echo ^<ESC^>[92m [92mGreen[0m
echo ^<ESC^>[93m [93mYellow[0m
echo ^<ESC^>[94m [94mBlue[0m
echo ^<ESC^>[95m [95mMagenta[0m
echo ^<ESC^>[96m [96mCyan[0m
echo ^<ESC^>[97m [97mWhite[0m
echo:
echo [101;93m STRONG BACKGROUND COLORS [0m
echo ^<ESC^>[100m [100mBlack[0m
echo ^<ESC^>[101m [101mRed[0m
echo ^<ESC^>[102m [102mGreen[0m
echo ^<ESC^>[103m [103mYellow[0m
echo ^<ESC^>[104m [104mBlue[0m
echo ^<ESC^>[105m [105mMagenta[0m
echo ^<ESC^>[106m [106mCyan[0m
echo ^<ESC^>[107m [107mWhite[0m
echo:
echo [101;93m COMBINATIONS [0m
echo ^<ESC^>[31m                     [31mred foreground color[0m
echo ^<ESC^>[7m                      [7minverse foreground ^<-^> background[0m
echo ^<ESC^>[7;31m                   [7;31minverse red foreground color[0m
echo ^<ESC^>[7m and nested ^<ESC^>[31m [7mbefore [31mnested[0m
echo ^<ESC^>[31m and nested ^<ESC^>[7m [31mbefore [7mnested[0m

echo:
echo ===============================================================================
echo ^<ESC^>[100;92m [100;92m [INFO] [0m
echo ^<ESC^>[103;94m [103;94m -[OK]- [0m
echo ^<ESC^>[106;35m [106;35m [WARN] [0m
echo ^<ESC^>[105;34m [105;34m [ERROR] [0m
echo:

set  "INFO=[100;92m [INFO]  [0m"
set  "OKOK=[103;94m -[OK]-  [0m"
set  "WARN=[106;35m [WARN]  [0m"
set "ERROR=[105;34m [ERROR] [0m"

echo %INFO% INFORMATION
echo %OKOK% OK
echo %WARN% WARNING
echo %ERROR% ERROR

echo:
echo ===============================================================================
echo =                                   TETRIS                                    =
echo ===============================================================================
echo:

echo:
echo ===============================================================================
echo [101;93m INVISIBLE CHARS [0m
echo ^<ESC^>[100;90m [100;90m XXXX [0m
echo ^<ESC^>[101;91m [101;91m XXXX [0m
echo ^<ESC^>[102;92m [102;92m XXXX [0m
echo ^<ESC^>[103;93m [103;93m XXXX [0m
echo ^<ESC^>[104;94m [104;94m XXXX [0m
echo ^<ESC^>[105;95m [105;95m XXXX [0m
echo ^<ESC^>[106;96m [106;96m XXXX [0m
echo ^<ESC^>[107;97m [107;97m XXXX [0m
echo -------------------------------------------------------------------------------
echo:

set "BL=."
set "CH=@"
set "CC=[103;93m%CH%[0m"

echo ========= BLANK FILL =========   ========== SOLID FILL ==========
echo:                                                                 
echo   R0      R90     R180    R270                
echo  y       y       y       y        y                                    
echo x 0123  x 0123  x 0123  x 0123   x 0123                                
echo  0::::   0::::   0::::   0::::    0%CC%%CC%%CC%%CC%              
echo  1::::   1::::   1::::   1::::    1%CC%%CC%%CC%%CC%              
echo  2::::   2::::   2::::   2::::    2%CC%%CC%%CC%%CC%              
echo  3::::   3::::   3::::   3::::    3%CC%%CC%%CC%%CC%              
echo ------------------------------   --------------------------------                                
echo:

echo ========= BLANK FILL =========
echo:
echo   R0      R90     R180    R270                
echo  y       y       y       y             
echo x 0123  x 0123  x 0123  x 0123         
echo  0%BL%%BL%%BL%%BL%   0%BL%%BL%%BL%%BL%   0%BL%%BL%%BL%%BL%   0%BL%%BL%%BL%%BL%
echo  1%BL%%BL%%BL%%BL%   1%BL%%BL%%BL%%BL%   1%BL%%BL%%BL%%BL%   1%BL%%BL%%BL%%BL%
echo  2%BL%%BL%%BL%%BL%   2%BL%%BL%%BL%%BL%   2%BL%%BL%%BL%%BL%   2%BL%%BL%%BL%%BL%
echo  3%BL%%BL%%BL%%BL%   3%BL%%BL%%BL%%BL%   3%BL%%BL%%BL%%BL%   3%BL%%BL%%BL%%BL%
echo ------------------------------
echo:

echo ============= I ==============    ============= I ==============                                                
echo:                                                                                                                
echo   R0      R90     R180    R270      R0      R90     R180    R270                                                
echo  y       y       y       y         y       y       y       y                                                    
echo x 0123  x 0123  x 0123  x 0123    x 0123  x 0123  x 0123  x 0123                                                
echo  0%BL%%BL%%BL%%BL%   0%BL%%BL%%CC%%BL%   0%BL%%BL%%BL%%BL%   0%BL%%BL%%BL%%BL%     0%BL%%BL%%BL%%BL%   0%BL%%BL%%CH%%BL%   0%BL%%BL%%BL%%BL%   0%BL%%BL%%BL%%BL%
echo  1%CC%%CC%%CC%%CC%   1%BL%%BL%%CC%%BL%   1%BL%%BL%%BL%%BL%   1%CC%%CC%%CC%%CC%     1%CH%%CH%%CH%%CH%   1%BL%%BL%%CH%%BL%   1%BL%%BL%%BL%%BL%   1%CH%%CH%%CH%%CH%
echo  2%BL%%BL%%BL%%BL%   2%BL%%BL%%CC%%BL%   2%CC%%CC%%CC%%CC%   2%BL%%BL%%BL%%BL%     2%BL%%BL%%BL%%BL%   2%BL%%BL%%CH%%BL%   2%CH%%CH%%CH%%CH%   2%BL%%BL%%BL%%BL%
echo  3%BL%%BL%%BL%%BL%   3%BL%%BL%%CC%%BL%   3%BL%%BL%%BL%%BL%   3%BL%%BL%%BL%%BL%     3%BL%%BL%%BL%%BL%   3%BL%%BL%%CH%%BL%   3%BL%%BL%%BL%%BL%   3%BL%%BL%%BL%%BL%
echo ------------------------------    ------------------------------                                                
echo:

