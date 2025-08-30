#! /bin/bash --

#.. Determine groups of identical files.

BackUpDir="$1"
CkSums="Cksum.txt"
Groups="Groups.txt"

#.. Group all the files by checksum, and report them.

fileGroup () {

    local Awk='
BEGIN { Db = 0; reCut2 = "^[ ]*[^ ]+[ ]+[^ ]+[ ]+"; }
{ if (Db) printf ("\n%s\n", $0); }

#.. Add a new cksum value.
! (($1,0) in Fname) {
    Cksum[++Cksum[0]] = $1;
    if (Db) printf ("Added Cksum %d value %s.\n", 
        Cksum[0], Cksum[Cksum[0]]);
    Fname[$1,0] = 0;
}
#.. Add a filename.
{
    Fname[$1,++Fname[$1,0]] = $0;
    sub (reCut2, "", Fname[$1,Fname[$1,0]]);
    if (Db) printf ("Fname [%s,%s] is \047%s\047\n",
        $1, Fname[$1,0], Fname[$1, Fname[$1,0]]);
}
#.. Report the identical files, grouped by checksum.
function Report (Local, k, ke, cs, j, je, Single) {
    ke = Cksum[0];
    for (k = 1; k <= ke; ++k) {
        cs = Cksum[k];
        je = Fname[cs,0];
        if (je < 2) { ++Single; continue; }
        printf ("\nGroup of %d files for cksum %s\n", je, cs);
        for (j = 1; j <= je; ++j) printf ("    %s\n", Fname[cs,j]);
    }
    printf ("\nCounted %d non-grouped files.\n", Single);
}
END { Report( ); }
'
    awk -f <( printf '%s' "${Awk}" )
}

#### Script Body Starts Here.

    #.. Checksum all the files, and show some statistics.
    [ x ] && {
        time ( cd "${BackUpDir}" && cksum */* ) > "${CkSums}"
        du -s -h "${BackUpDir}"
        head -n 3 "${CkSums}"
        awk '{ Bytes += $2; }
            END { printf ("Files %d, %.2f MB\n", FNR, Bytes / (1024 * 1024)); }
            ' "${CkSums}"
    }

    #.. Analyse the cksum data.
    time fileGroup < "${CkSums}" > "${Groups}"
