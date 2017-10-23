* Encoding: UTF-8.

GET
  /FILE='<OUTPUTDIR>accumulate.sav'.
ADD FILES
	/FILE=*
	/FILE='<INFILE>'.

EXECUTE.
SAVE OUTFILE='<OUTPUTDIR>accumulate.sav'
  /COMPRESSED.
