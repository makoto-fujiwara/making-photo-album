# $Id: Makefile,v 1.11 2013/12/14 00:36:34 makoto Exp $
# Making album directory for Web pages
# See comment for the directory hirearchy.

# -- Tools -- exif, perl script, ImageMagick tool.
EXIF	=	exif
EXIF_DATETIME =	${PWD}/exif-datetime
EXIF_ROTATE =	${PWD}/exif-rotate
CONVERT	=	convert

# -- TARGET PATH --- ,	you need edit this line.
#			Also expectiong original/*.jpeg files
#PATH?=  /home/makoto/public_html/p12/20121104
#TPATH?=  /home/mayumi/public_html/chiba47/members/p/20161022
#TPATH?=  /home/makoto/public_html/p18/20180329
TPATH?=  /home/makoto/public_html/p19/20190201


# -- Target Directories --
ORIGNAL	=	original
THUM	=	thum
# directory name and also midsize pixcell size:
MIDSIZE	=	640x480
# -- Target Directories to be created --
DIRECTORIES =	640x480 thum comment

# -- Target related --
COOKIES = 			\
	${TPATH}/.mkdir 	\
	${TPATH}/.thum 		\
	${TPATH}/.640x480	\
	${TPATH}/.date 		\
	${TPATH}/.comment	\
	${TPATH}/.rotate	\

all: ${COOKIES}
	cp -p    index.cgi ${TPATH}/
	chmod +x index.cgi ${TPATH}/
	cp config.ph 	   ${TPATH}/

${TPATH}/.mkdir:
	(cd ${TPATH}; \
	mkdir ${DIRECTORIES} )
	touch   $@
# exif データがない時の backup があった方が良い
${TPATH}/.thum:   ${TPATH}/.mkdir
	( cd ${TPATH}/thum; \
	for i in `/bin/ls ../original/` ; \
	  do ${EXIF} -e -o $$i  ../original/$$i; \
	  echo rc: $$rc; \
	done)
	touch   $@
${TPATH}/.640x480: ${TPATH}/.mkdir
	( cd ${TPATH}/640x480; \
	for i in `/bin/ls ../original/` ; \
	  do  ${CONVERT} -resize ${MIDSIZE} ../original/$$i $$i; \
	done)
	touch   $@
${TPATH}/.date:
	(cd ${TPATH}/original; \
	${EXIF_DATETIME} * )
	touch   $@
${TPATH}/.comment:
	echo	comment
	touch   $@
${TPATH}/.rotate:  ${TPATH}/.mkdir
	(cd ${TPATH}/original; \
	env LANG=C ${EXIF_ROTATE} -e * )
	touch   $@
clean:  
	(cd ${TPATH}; \
	rm -f  ${COOKIES} ;\
	rm -rf  ${TPATH}/thum ${TPATH}/640x480 ${TPATH}/comment;\
	)

real-clean:
	(cd ${TPATH}; \
	rm -f  ${COOKIES} ;\
	rm -rf ${DIRECTORIES} \
	)
#
# (1) Have this tool directory
#	Makefile
#	index.cgi
#	config.ph (sample)
# (2) -  Decide your directory to publish on Web, for example
#         http://www.example.com/P/
#     - It would be nice to have one sub directory under P, like
#         http://www.example.com/P/items/
#     -  again you need to make one more directory with fixed name,
#        original under 'items'.
#     - Place your copy of *.jpge files on
#        P/item/original/*.jpeg.
#     - Change above 11th line for TPATH to reflect the PATH you
#       placed the jpeg files.
#
#     - Now you issue make, then the shape will be
# (3) target directory
#     TARGET/ is equivalent above P/items/ here:
#     [before make]
#        TARGET/original ... copy of original JPEG files
#
#     [after make]
#        TARGET/original ... copy of original JPEG files
#		thum
#		640x480
#		comment
#		index.cgi
#		config.ph
