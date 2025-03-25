#!/usr/bin/perl
use LWP::Simple;
use HTML::TokeParser;
use Data::Dumper;

open(FH, "links.txt");
my @filecontent=<FH>;
close FH;

open(HANDLE, ">filecontents.html");

foreach my $url(@filecontent){

print "Fetching content for url: $url \n\n";

my $content = get($url);

open(WH,">temp");
print WH $content;
close WH;

my $tp=HTML::TokeParser->new("temp");
$tp->empty_element_tags(1);
my $content_top_area="";
my $content_header="";	
my $content_bottom_area="";

	while (my $token=$tp->get_token){
		if(($token->[0] eq"S")&&($token->[1] eq"div")&&($token->[2]{id} eq"content-header")){
			while(my $token=$tp->get_token){
				if(($token->[0] eq"E")&&($token->[1] eq"div")){
					last;
				}
				if($token->[0] eq "T"){
       				 $content_header.=$token->[1];
     				}
    				 if($token->[0] eq "S"){
				 $content_header.=$token->[4];
    				 }
    				 if($token->[0] eq "E"){
    				  $content_header.=$token->[2];
   				 }
			}
		}
		if(($token->[0] eq"S")&&($token->[1] eq"div")&&($token->[2]{id} eq"node-body-top")){
			while(my $token=$tp->get_token){


				if(($token->[0] eq"E")&&($token->[1] eq"div")){
					last;
				}
				if($token->[0] eq "T"){
       				 $content_top_area.=$token->[1];
     				}
    				 if($token->[0] eq "S"){
				 $content_top_area.=$token->[4];
    				 }
    				 if($token->[0] eq "E"){
    				  $content_top_area.=$token->[2];
   				 }
			}
		}
		if(($token->[0] eq"S")&&($token->[1] eq"div")&&($token->[2]{id} eq"node-body-bottom")){
			while(my $token=$tp->get_token){
				$counter=1;

				if(($token->[0] eq"E")&&($token->[1] eq"div")){
					last;
				}
				if($token->[0] eq "T"){
       				 $content_bottom_area.=$token->[1];
     				}
    				 if($token->[0] eq "S"){
				 $content_bottom_area.=$token->[4];
    				 }
    				 if($token->[0] eq "E"){
    				  $content_bottom_area.=$token->[2];
   				 }
			}
		}
	}
my $contents= $content_header.$content_top_area.$content_bottom_area;
print HANDLE $contents;

}
close HANDLE;
