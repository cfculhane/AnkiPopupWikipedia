@ECHO OFF
REM Builds the addon for release
echo Copying source code to dist folder ...
robocopy .\popup_wikipedia .\dist\popup_wikipedia /E /PURGE /XD "__pycache__" "logs" /XF *.pickle *.pyc *.sqlite
cd .\dist\popup_wikipedia
zip -r "../popup_wikipedia.zip" .
ECHO Build complete!
pause
