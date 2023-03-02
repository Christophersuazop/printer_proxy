@ECHO OFF
nssm.exe stop proxyPrinter
nssm.exe remove proxyPrinter confirm
nssm.exe install proxyPrinter "%~dp0main.exe"
nssm.exe set proxyPrinter AppStdout "%~dp0logs/server.log"
nssm.exe set proxyPrinter AppStderr "%~dp0logs/server.err.log"
nssm.exe set proxyPrinter AppRotateFiles 1
nssm.exe set proxyPrinter AppRotateOnline 1
nssm.exe set proxyPrinter AppRotateBytes 1000000
nssm.exe start proxyPrinter