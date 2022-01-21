# pdf table scraping instructions

use tabula to extract the table regions. I had to run tablula with a different port as described here

https://github.com/tabulapdf/tabula#known-issues

`java -Dfile.encoding=utf-8 -Xms256M -Xmx1024M -Dwarbler.port=9999 -jar tabula.jar`

had to press ctrl-C in the prompt to get the web page to unfreeze


1. extract table with tabula
2. export to `tabula_template.json`
3. run extract.py