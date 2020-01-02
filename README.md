# AnkiWikiPopup
Anki 2.1 addon to display Wikipedia page previews inside of Anki


This is currently in beta stage - things will almost certainly break! Please submit a bug report if it does.

Significant portions of the code (as marked in the source files)
 were based on the Anki add-on [Pop-up Dictionary](https://github.com/glutanimate/popup-dictionary/) by Glutanimate. [Click here to support Glutanimate's work](https://glutanimate.com/support-my-work/).

I would also like to thank the team at [AMBOSS](https://www.amboss.com/) for their encouragment and insipration for this work. Some css and js code was taken from their [extremely good Anki Addon](https://www.amboss.com/us/anki-amboss?hp=header).


Additionally, this add-on includes the following javascript libraries:
- jQuery (v1.12.4), (c) jQuery Foundation, licensed under the MIT license
- qTip2 (v2.1.1), (c) 2011-2018 Craig Michael Thompson, licensed under the MIT license
- jQuery.highlight, (c) 2007-2014 Johann Burkard, licensed under the MIT license



### Known issues

- Clicking on links inside the popup opens the browser, but with the wrong URL
- Disambiguation pages are not handled well
- Does not work with NightMode due to the way Night-Mode monkeypatches Reviewer.revHtml, see [this github issue here](https://github.com/krassowski/Anki-Night-Mode/issues/53)
