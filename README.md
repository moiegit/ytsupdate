# ytsupdate
End of the week reminder of free movies your can watch. 

PLEASE DO NOT SUPPORT PIRACY.

Automate my weekly life by emailing me a list of new movies from YTS. Coded in Python and run behind Azure Functions.
Every Friday at 5pm, send me a list of the new movies uploaded on the website.
Provide links on every movie directed to its download page.


I - scrape YTS featured movies page
  - pull out the Movie Titles, Year released, Download Link
II - send the list to my personal email every Friday at the end of the day for a potential movie marathon at home
   - set up cron timer at "0 0 17 * * 5"
   - set up Azure function with env variables to be used for credentials
