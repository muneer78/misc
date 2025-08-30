#!/usr/bin/perl
# print-boobs.pl
# run as follows perl printboobs.pl -w
use warnings;
use strict;
use Getopt::Std;
use Time::HiRes qw(sleep);  
use vars qw($opt_w $opt_n);
$|=1;
getopts("wn:");
if ($opt_w) {
  while($opt_w){
    print '(.  )(.  )' . "\r";
    sleep(0.25);
    print '( ^ )( ^ )' . "\r";
    sleep(0.25);
    print '(  .)(  .)' . "\r";
    sleep(0.25);
    print '( ^ )( ^ )' . "\r";
    sleep(0.25);
  }
} elsif ($opt_n) {
for (my $i=0; $i < $opt_n; $i++) {
    print "( . )( . )\n";
  }
} else {
  print "No boobies for you\n";
}
exit(0);