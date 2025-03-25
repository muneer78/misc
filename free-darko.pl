#!/usr/bin/perl
use LWP::UserAgent;
use HTML::TokeParser;
use Data::Dumper;

my $ua = LWP::UserAgent->new;
$ua->agent("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)");

open(HANDLE, ">totalContent.html");

foreach my $year(2005..2011){
	foreach my $month(1..12){
	$month = sprintf("%02d", $month);
	
	my $url="http://freedarko.blogspot.in/".$year."_".$month."_01_archive.html";
	print "Fetching content for article: ".$url."\n\n";
	my $req = HTTP::Request->new(GET => $url);
	$req->content_type('application/x-www-form-urlencoded');
	my $res = $ua->request($req);
	
	my $title="";
	my $body="";

 		if ($res->is_success) {
		open(WH,">temp");
		print WH $res->content;
		close WH;

		my $tp=HTML::TokeParser->new("temp");
		$tp->empty_element_tags(1);

		while(my $token=$tp->get_token){
			if(($token->[0] eq "S")&&($token->[1] eq "div")&&($token->[2]{class} eq "post")){
			    my $divCounter=1;
			    my $post = "<div class='post'>";
			    my $isByBS=0;
				while(my $token=$tp->get_token){
				
				    if(($token->[0] eq "S") && ($token->[1] eq "div")){
					$divCounter++;
				    }
				    if(($token->[0] eq "E") && ($token->[1] eq "div")){
					$divCounter--;
				    }
				    if($token->[0] eq "T"){
					if($token->[1] =~ /posted\sby\sBethlehem\sShoals/){ 
					    $isByBS=1;
					    $post .= "posted by Bethlehem Shoals</em></p></div>";
					    goto ENDARTICLE;
					}else{
					    $post.=$token->[1];
					}
				    }
				    if($token->[0] eq "S"){
					$post.=$token->[4];
				    }
				    if($token->[0] eq "E"){
					$post.=$token->[2];
				    }
				    if($divCounter == 0){ goto ENDARTICLE; }
				}##while
		ENDARTICLE:					
			if($isByBS == 1){
				print HANDLE $post;	
				
			}
		
			}##if div post
		}##while
		}##if success
}

	if(($year eq "2011") && ($month eq "04")){ goto ENDPARSER; }

}##foreach

ENDPARSER:

close HANDLE;


