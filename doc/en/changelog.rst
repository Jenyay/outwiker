Version History
===============

Current developing version
--------------------------

2.0.0.808 beta (January 26, 2017)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added the ability to add alias to page.
* Changed GUI to set hot keys.
* Added options to change editor margin color.
* Added options to change background color of the selected text.

2.0.0.806 beta (November 14, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added the menu items to move cursor in text.
* Added the menu items to copy / cut the current line to clipboard.
* Bug fixes.


2.0.0.804 dev (October 20, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fixed deb package for Ubuntu 16.10.

2.0.0.802 dev
~~~~~~~~~~~~~

* Internal changes.

2.0.0.800 dev (August 20, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added the Swedish translation.
* Added the "--page, -p" command line parameter to select page when starting.
* Added the "--normal" command line parameter to disable minimizing when starting.
* Added the "--debug" command line parameter to run in the debug mode.
* Bug fixes.

2.0.0.798 dev (July 27, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Restored availability the icon in the system tray on Linux.
* The editor adds the ability to join lines with the hot key or menu item.
* The editor adds the ability to remove word to beginning / ending with the hot key or menu item.
* The editor adds the ability to decreade nesting level of the list items with the hot key or menu item.
* Changed tabs style.

2.0.0.796 dev (July 02, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The editor adds the ability to duplicate the current line with hot key or menu item.
* The editor adds the ability to delete the current line with hot key or menu item.
* The editor adds the ability to move lines up / down with hot keys or menu items.
* Improved heading inserting in wiki pages.
* Build system refactoring.
* Bug fixes.


2.0.0.794 (May 30, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~

* Fixed errors related with migration to wxPython 3.0.

2.0.0.792 (May 10, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~

* The program now uses wxPython 3.0 library.


Previous versions
-----------------

1.9.0.790 (April 09, 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added spell checker.
* Created the groups for the icons.
* Now users can add custom icons.
* The choice of colors for the tag cloud.
* The choise the action when you make left or middle mouse click on the tag.
* The choise the action when you make double mouse click on the attached file.
* Added the new wiki commands for the table creation: [=(:table:), (:row:), (:cell:), (:hcell:)=].
* Improved search het keys for the actions.
* Added new icons.
* Added new page styles.
* Now in the link inserting dialog you can select an attached file to create link to it.
* Added help.


1.8.1.752 (October 20, 2014)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Bug fixes


1.8.0.750 (October 11, 2014)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added the ability to customize keyboard shortcuts.
* Added the ability to refer to a page using unique identifiers.
* Added the ability to navigate through the links to pages with the anchors ({+[=page://bla-bla-bla/#anchor=]+}).
* Added the ability to use relative paths in the links on the pages ({+[=../../page 1/page 2=]+}).
* Added the ability to change the page style for branch of the pages at the same time.
* Added the ability of search and replace on the page.
* Added the buttons "Forward" and "Back" for the return to the previous pages.
* Added the ability to change the editor colors.
* Added the ability to change the behaviour of the Home / End keys id the editor (go to begin / end of the string or the paragraph).
* Added a new tag of the wiki syntax for quoting: [=[>...<]=].
* Added the button and menu item insertion the current date and time
* Added the commands [=(:crdate:) and (:eddate:)=] for insertion the creation and edition dates of the page respectively.
* Added the dialogs for the comands [=(:attachlist:), (:childlist:) and (:include:)=].
* Added the ability to sort child pages for the creation and edition date in the command [=(:childlist:)=].
* On the global search page added the ability to sort child pages for the creation date.
* Added new command line parameter "-r" or "--readonly" for the opening the notes tree readonly.
* Added the popup tooltips for icons in the property dialog for page.
* Added a new styles for page design.
* Added the button and menu item for opening a folder with a attached files in a system file manager.
* Added the saving recent used page style.
* Added the saving cursor position for page before closing.
* Added the Italian localization.
* Now in the attachments panel showed the files icons.
* Changed the hyphenation algorithm (''br'' tags instead of ''p'').
* Now opening the notes tree and global search cunduct in a separate thread.
* Now for every page saved the creation date.
* Now all HTML tags, which the wiki parser create, in a lowercase.
* Now help will be open in a separate window.
* Settings moved from ~/.outwiker more ideologically correct place (depending on the operating system).
* Added new icons for pages.
* Many accelerations.
* Bug fixes and improvments.

