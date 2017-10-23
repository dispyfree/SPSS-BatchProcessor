* Encoding: UTF-8.
* Encoding: .
* Encoding: UTF-8.

GET
  /FILE='<OUTPUTDIR>accumulate.sav'.
ADD FILES a
	/FILE=*
	/FILE='<INFILE>'.

EXECUTE.
SAVE OUTFILE='<OUTPUTDIR>accumulate.sav'
  /COMPRESSED.
