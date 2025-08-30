{
    if ($NF ~ /\*$/) {
        print "---"
    }
    print $0
}