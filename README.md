This directory contains the utility to show photo albums by cgi-bin.
* FEATURES:

 ** Create cgi-bin enabled photo-album directory
 ** (appearance):
  -  showing upper level directories
  -  easily choice on three step size thum/640x480/original
  -  easy navigation to next photo by click
  -  highliting self directory (easy to see where i am)

 ** (creation):
  - easy to operate.
   + setup environment (once)
   + copy photo files (from your memory card)
   + adjust one line to point the album location
   + just make

  - automatic Date/Time insertion (if EXIF available)
  - automatic Rotation correction (ditto)
  - comment insertion manually afterward.

* DIRECTORY CONFIGURATION:
 ** (working directory) ... shell access on local machine
    Makefile
    config.ph
    exif-datetime
    exif-rotate
    index.cgi

 ** (target directory) ... httpd access
  The typical configuration on Web server.
    PHOTO_directory/directories/original/
				thum/
				640x480/
				comment/
				config.ph
				index.cgi

 ** (environment for local make)
  Following commands are necessary to
  generate directories/files 
    make
    perl 
    exif
    convert (of ImageMagick)

 ** (environment for remote Web server)
    cgi-bin access
    perl
    nkf (to convert kanji code)

* INSTALL/SETUP:
 ** (1) Have the copy of this working directory (anywhere on any machine)

 ** (2) make target directory  (on your Web server or local copy of them)
    PHOTO_directory/directories/original
    (for example)
    make -p PHOTO_directory/directories/original

 ** (3) copy your *.jpg (etc) files to above original 
    directory.

 ** (4) Adjust (working_directory)/Makefile to point
   target directory (edit one line of Makefile)
   (Following line)
   TPATH   =  /home/makoto/public_html/p09/20091103

 ** (5) cd working directory
    make

    Then all necessary directories and files are
    generated.

    adjust config.ph

    You may also need to edit the first line of perl path
    in index.cgi

 ** (6) edit comment/img_file  (no .jpg suffix)
    to add comments on each photo

* Limitation:
  (1) http environment
      (a) Your web server needs to execute *.cgi (perl cgi-bin)
      (b)  index.cgi is to be listed in DirectoryIndex directive on http.conf
      (c)  or .htaccess is allowed and (b) equivalent is in it.

  (2) machine environment
     Currently you need to have direct access to files on Web server
     from shell access environment (but you may copy set of files 
     from you local shell-access-machine to remote-web-server after
     you execute make.)

  (3) photo files:
  Your *.jpeg file to be expected EXIF compliant.
  Date/Time/Rotation will be extracted from exif info.

  (4) related files/commands (on your local machine)
  You may need shell access to create files/directories
  by 'make'. And also 'exif' and 'convert' command should be in the PATH.

  (5) appearance on Web server:
   Currently  'directories' on target directory will
  all be shown at web server. This should be convenient 
  for no need to make indexes of all the directories.

* Problems:
   (0) Either you don't have exif nor exif fails to execute.
       You may skip that part. Not soley important for the album.

   (1) If you get 'no files *.jpg', check
       (a) You have files under thum/*.jpg
       (b) Check config.ph to reflect the photo file name convention.
           If your photo name is like PB033001.JPG,
	   $c::PREF = 'PB0'; # or just 'PB'
	   $c::SUF  = 'JPG';
   (2) Server error 500
       (a) check if *.cgi is enabled
       (b) Is 'perl -wc index.cgi' OK ?
       (c) The first line of your index.cgi match your environment ?
       (d) execute permission is set on index.cgi ?
           chown +x index.cgi

   (3) Abort in the middle
      If you interrupt make by Control-C, make stops.
      You may type 'make clean' to remove cookie files.

You may use this utility for your album with no charge.
Thanks for reading:
Copyright makoto (at) ki (dot) nu 2009

   $Date: 2009/11/07 03:45:57 $ UTC
   $RCSfile: README.en,v $'
   $Revision: 1.5 $
   $Author: makoto $'

Local Variables:
mode: outline-minor
outline-regexp: "[\t ]*[*\f]+"
End:
