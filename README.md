work in progress bot to check the differences in Stunfisk wiki changes

###How it works:

  - The bot has a cached version of all pokemon pages in a binary file that's been serialized using the Python *pickle* library
  - It checks /r/stunfisk/wiki/revisions for recent revisions and checks the pages that have been changed if the page that was edited is a pokemon
  - It logs the changes and records the change in its cache.  
  - Cache is located in /obj/poke_dict.pkl


Uses the same libraries as StunfiskDexter
