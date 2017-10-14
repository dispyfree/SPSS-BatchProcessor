* Encoding: UTF-8.
* Encoding: .
* Encoding: UTF-8.

GET
  /FILE='<OUTPUTDIR>Zusammenfassung.sav'.
 ADD FILES /FILE=* 
  /FILE='<INFILE>'.

EXECUTE.
SAVE OUTFILE='<OUTPUTDIR>Zusammenfassung.sav'
  /COMPRESSED.
