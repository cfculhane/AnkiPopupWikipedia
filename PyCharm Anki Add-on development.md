PyCharm Anki Add-on development

This is a quick and dirty guide to getting Anki running in a dev environment.
My setup : Windows 10 x64, Python 3.7.4


### Setting up Anki from source
- Pull down source from https://github.com/dae/anki
- In Pycharm, create a project in this folder
- Create your venv
- Install requirements using pip
	- on my system, pip wouldn't pull down pyaudio, so I downloaded the wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
	- For whatever reason, pywin32 isn't listed in the requirements either, so install with `pip install pywin32`
	- Also need to install the QT dependencies: `pip install PyQt5 PyQtWebEngine`
- At this point, you need to build the UI components. No windows script is provided, but one is available here: https://gist.github.com/dlon/81ca304616ee4b03c58a11581a21d048#file-build_ui-ps1
	- download the script, put it in .\anki\tools, then run powershell
	- `cd .\anki` then `.\tools\build_ui` , should run for a bit and display a success message. Yay!
- (Optional, but highly recommended) - you want to start your anki with a different profile path, so your addons and profile are seperated from your 10000 cards
	- To do this, add a new run configuration in PyCharm, specifying the venv you created earlier. Set the working directory to .\anki
	- Set the script as .\anki\runanki.py
	- Under script parameters, set `-b <path to your anki dev folder>` e.g. C:\Github\anki
	- This will create a new fresh profile, and create a .\anki\addons21 folder for your eventual addon.

At this point, you should run it, and ensure it starts up fine, and has created the addon folder inside the dev environment.


### Setting up add-on dev environment
- Create a new git repo elsewhere, e.g. C:\Github\TestAnkiAddon\
- Create a new PyCharm project there too
- So that you get autocomplete and other handy things when developing, in project settings, add your anki directory as 'Sources Root'
- Create a new Run configuration, and make it the same as you created earlier, using the venv inside .\anki
- Create a sub dir for your addon, e.g. .\TestAnkiAddon\test_addon
- Create a basic addon from the code here: https://apps.ankiweb.net/docs/addons.html, putting it inside __init__.py
- At this point, you could copy this folder into the addons directory for running, but you would have to remember to do that each time you change your addon. That's no fun!
- Enter PyCharm Deployment tools! In PyCharm, go to Tools -> Deployment and set up a new local deployment, from .\TestAnkiAddon\test_addon to .\anki\addons21\test_addon
- Because you added anki to sources root in your project, you want to exclude that from the deployment in the "excluded paths" screen
- Set the auto upload to On if you want to constantly be pushing the code from your addon dev into the anki dev folder

- Enjoy your nice environment :D


