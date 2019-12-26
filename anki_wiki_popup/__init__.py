from ._version import __version__


def checkFor2114ImportError():
    from .consts import ADDON
    try:
        # litmus test for Anki import bug
        from .libaddon.platform import anki_version  # noqa: F401
        return True
    except ImportError:
        # Disable add-on and inform user of the bug
        from aqt.utils import showWarning
        from aqt import mw
        from anki import version as anki_version

        mw.addonManager.toggleEnabled(__name__, enable=False)

        bug = "https://anki.tenderapp.com/discussions/ankidesktop/34836"
        downloads = "https://apps.ankiweb.net#download"
        beta = "https://apps.ankiweb.net/downloads/beta/"
        vers = "2.1.15"
        title = "Warning: {name} disabled".format(name=ADDON.NAME)
        msg = ("<b>WARNING</b>: {name} had to be disabled because the "
               "version of Anki that is currently installed on your system "
               "({anki_version}) is incompatible with the add-on.<br><br> "
               "Earlier releases of Anki like this one "
               "suffer from a <a href='{bug}'>bug</a> that breaks "
               "{name} and many other add-ons on your system. "
               "In order to fix this you will have to update Anki "
               "to version {vers} or higher.<br><br>"
               "As of writing this message, Anki {vers} is still in "
               "beta testing, but that might have "
               "changed in the meantime. Please check with the "
               "<a href='{downloads}'>releases page</a> to see if {vers} "
               "or a later release is available, otherwise download and "
               "install the 2.1.15 beta <a href='{beta}'>here</a>.<br><br>"
               "After updating Anki, please re-enable "
               "{name} by heading to Tools → Add-ons, selecting the "
               "add-on, and clicking <i>Toggle Enabled</i>.".format(
            name=ADDON.NAME, anki_version=anki_version, bug=bug,
            vers=vers, downloads=downloads, beta=beta
        ))

        showWarning(msg, title=title, textFormat="rich")

        return False


def initializeAddon():
    """Initializes add-on after performing a few checks

    Allows more fine-grained control over add-on execution, which can
    be helpful when implementing workarounds for Anki bugs (e.g. the module
    import bug present in all Anki 2.1 versions up to 2.1.14)
    """

    if not checkFor2114ImportError():
        return False

    from .consts import ADDON
    from .libaddon.consts import setAddonProperties

    setAddonProperties(ADDON)

    from .libaddon.debug import maybeStartDebugging

    maybeStartDebugging()

    from .reviewer import initializeReviewer
    from .web import initializeWeb

    initializeWeb()
    initializeReviewer()


initializeAddon()
