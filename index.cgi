#!/usr/local/bin/perl
# $Id: index.cgi,v 1.7 2009/11/07 07:00:15 makoto Exp $
use strict;
require 'cgi-lib.pl';
ReadParse();

# set default prefix and suffix for photo file
   $c::PREF = 'dscn';
   $c::SUF = 'jpg';
my $COL  = 8;  ## three columns to display photo's

# fixed directory names
my $D640  = "640x480";
my $DORG  = "original";
my $DCOMM = "comment";	# the name of the directory for (short) comment
my $DNOTE = "note";	# the name of the directory for note

# Network Kanji Filter to output iso-2022-jp
my $NKF   = '/usr/local/bin/nkf -j';

if ( -f "config.ph" ) {
    require './config.ph';
}
# get title and comment for <title></title> and top page comment
my ($TITLE) = $c::TITLE;
my ($TOP_COMMENT) = $c::COMMENT;
my $UP    = $TITLE;
   $UP    =~ s/photo//; $UP =~ s|/||g; # not used for now ?

# pickup from query string
my $single_photo = $main::in{'photo'};
my $size         = $main::in{'size'};

# get update time information of photo *.jpg
my $d640_t = (lstat($D640))[9];   # 9 = mtime
my $dorg_t  = (lstat($DORG))[9];
my $dcomm_t = (lstat($DCOMM))[9];

my $time = $d640_t;
if ( $dorg_t > $time ) { $time = $dorg_t}
if ( $dcomm_t > $time ) { $time = $dcomm_t}

my $query = $ENV{'QUERY_STRING'};

# get list of thum files 
my @thum;   
   @thum = `(cd thum;ls *.$c::SUF)`;

# Now ready to output
open(STDOUT,"|$NKF");

if ( $query ) {
    single($single_photo,$size);
}
else {
    header($TITLE);

    print $#thum +1 , " photos";
    print $TOP_COMMENT, "<br>\n";
## print ", last update: ";
## print $time

    listing();}
trail();
exit;
# -----------------------------------------------------------
sub trail  {
    print "</body></html>\n";
}

sub header {
    my $title = shift;
    print "Last-Modified: ",scalar(gmtime($time)),"\n";
    print "Content-Type: text/html;charset=iso-2022-jp\n\n";

    print <<HEADER;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML  4.01//EN">
<html lang="ja">
<head>
<title>$title</title>
<STYLE TYPE="text/css">
table   {
    border-color: white; /* not effective now */
}
td.note {
    vertical-align: top;
    text-aling: top
}
 span.rev { 
color: white; 
background-color: #304050 ;
}
span.small { 
font-size: small;    
}
span.pale {
background-color: #ffffff ;
}
span.dark {
background-color: #d8d8e0 ;
}
 pre { 
  font-size: small;

  padding:      0.5em;
  border-color: #ffeeb0;
  border-style: outset;
  border-width: 1px;
  background: #c8c8c8;
  font-family:monospace;
 }
</STYLE>
</head><body>
HEADER



}
# show list of photo/link just above the single photo
sub show_list {
    my $self = shift;
    my @list = @_;

#    print `pwd`;
    my $showing = 0;	# to mark as this is it.
    my $next;		# to return the next photo number (to link).
    my @TEXT;           # for delayed listing (store and return text)

    foreach my $i (@list) {
	my $tmp = $c::PREF;
	$i =~ s/$tmp//;
	$i =~ s/\.$c::SUF//;
	chomp($i);
	my $photo = "$size/$i";
	if ($self eq $i ) {		# mark as it is you, by inversion
	    $showing = 1;

	    push(@TEXT,
	    	  "<span class=\"rev\">$i</span>\n" );}
	else {				# normal link to photo

	    push(@TEXT,
	    	  "<a href=\"./?photo=$i&size=$size\">$i</a>\n");
	    if ($showing) { $next = $i; $showing = 0;} # it was showing
	}
	if ( -r $photo ) { 
	    push(@TEXT, $photo) ;}
    }
    return ($next, @TEXT);

}
sub note {
    my $file = shift;
    my @note_lines;
    if ( -r $file ) {
	open(NOTE, $file) ;
	@note_lines = <NOTE>;
	close(NOTE);
    }
    return join ("\n", @note_lines);
}
# -----------------------------------------------------
#       show single photo
# -----------------------------------------------------
sub single {
    my $photo   = shift;
    my $size    = shift;
    my %big = ('640x480','original',
	    'original','640x480',
    );
    my $comment = "$DCOMM/$c::PREF$photo";
    $comment =~ s/\.$c::SUF$//;

    my $note = "$DNOTE/$c::PREF$photo";
    $note =~ s/\.$c::SUF$//;

    # get page structure if note/img_nnnn exists
    my($note_text) =  note ($note);

    header($photo);
# --------------------------------------------------------

    if ($size == 'original') {
    print "<a href=\"./?photo=$photo&size=640x480\">縮少</a>\n";
    }
    print "<br>\n";

    if ($note_text ) {
	print "<table cellspacing=0 cellpadding=5 border=0><tr><td>\n";
    }
    # -------------------------------
    #   make link text first
    # -------------------------------
    my ($next, @TEXT)  = show_list($photo, @thum);
    if ($next) { print "<a href=\"./?photo=$next&size=$size\">";}
    # -------------------------------
    #   show single photo
    # -------------------------------

    print "<img src=";
    print "\"$size/$c::PREF".$photo.".$c::SUF\" border=0>";
    if ($note_text ) {
	print "</td><td class=\"note\">\n";
	print $note_text;
	print "</td></tr></table>\n";	
    }
    if ($next) { print "</a>";}

    my $toggle = $big{"$size"};

    print "<br>\n";
    comment ($comment);
    print @TEXT;

    print "<a href=\"./?photo=$photo&size=$toggle\">";
    print "(拡大縮少)</a><br>\n";

    print "<a href=\"./\">一覧</a><br>\n";

# prepare to link to next photo (by clicking img)
    if ($next)  {print "(写真をクリックすると次を表示します)";}
    print " \n";
my $URL = $ENV{'REQUEST_URI'};
    top_link($URL);

}
# add comment for each photo
sub comment {
    my $file = shift;
if ( -r $file ) {
	open(COMMENT,$file) ;
	print <COMMENT>;
	close(COMMENT);
	print "<br>";
	 }

}
# show list of photo's at entry page
sub listing {
if ($#thum == -1 ) { print "Sorry, no photo *.$c::SUF found in thum/.<br>\n" ;}

my $serial = 1;
#comment("$DCOMM/index");
    print "<table border=0>\n";
my $column_count = 0;
foreach my $i (@thum) {
    chomp $i;

    my $s640     = "$D640/$i";
    my $original = "$DORG/$i";
    my $photo    = $i;
    $photo    =~ s/$c::PREF//;
    $photo    =~ s/\.$c::SUF//;
    my $href = ''; my $a = '';

    if ( -f $s640 ) { 
	$href = "<a href=\"?photo=$photo&size=$D640\">";
	$a    = "</a>";    } 
    elsif ( -f $original ) {
	$href = "<a href=\"?photo=$photo&size=$DORG\">";
	$a    = "</a>";    } 
    if ($column_count == 0) {  print "<tr>"}
    print "<td>$href<img src=\"thum/$i\" border=0>$a ",$photo,"<br>";    
    my $comment = "$DCOMM/$i";
    $comment =~ s/\.$c::SUF$//;
    comment ($comment);

    if ( -f $s640 ) { 
	print "<a href=\"?photo=$photo&size=$D640\">$D640</a> | ";  }
    print "<a href=\"?photo=$photo&size=$DORG\">original size</a>";    
    print "</td>\n";
    if ($column_count++ == $COL - 1 ) {  print "</tr>\n"; $column_count = 0;}    
}

print "</table>\n";
}
# show links by looking at upper directory
sub top_link {
    my $URL = shift;
       $URL =~ s|\?.*||; # omit ? and after (argument)
    my @URL = split '/', $URL;
    my $DATE = pop @URL;
    my (@DIRS) = `ls  ../`;
    my $short_dir;
#    my $toggle = 0; # toggle background color
    my $bg;
    print "<span class=\"small\">\n";
    foreach my $dir (@DIRS){
	chomp($dir);
	if ( $dir =~ /~$/ ) { next;}
	if ( $dir eq /CVS/ ) { next;}
	if ( -f "../$dir/.htaccess") {next;}
	$short_dir = $dir;
#	if ($toggle)	{ $bg = "pale"}
#	$toggle = 1 - $toggle;
	if (substr($dir,4,2)%2) { $bg = "pale"}
	else		{ $bg = "dark"}
	
	if (substr($DATE,0,4) eq substr($dir,0,4) ) {
	    $short_dir = substr($dir,4,2).'/'.substr($dir,6,9);
	}
	if ($dir eq $DATE) {
	    print "<span class=\"rev\">$short_dir</span>\n";}
	else {
	    print "<span class=\"$bg\"><a href=\"../$dir\">$short_dir</a></span>\n";}
    }
    print "</span><br>";
}
__END__

