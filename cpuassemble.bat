@echo off
set "file=%~n1"
set "cpupath=C:\Users\Alex\Downloads\Code\Python\CPUAssembly"
set "programs=%cpupath%\Programs"

cls

python "%cpupath%\assembler.py" "%programs%\%file%.cpuasm"
python "%cpupath%\bintohex.py" "%programs%\bins\%file%.bin"

type "%cpupath%\Programs\hex\%file%.hex" | "C:\Windows\System32\clip.exe"