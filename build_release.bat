@ECHO OFF
REM Builds the addon for release
echo Copying source code to dist folder ...
robocopy .\anki_wiki_popup .\dist\prod_sendout /E /PURGE /XD "__pycache__" "logs" /XF *.pickle *.pyc
