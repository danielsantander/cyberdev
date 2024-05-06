#!/usr/bin/perl

print "Hello World!\n";
print "\n------------------------------------------";
print "\nExamples";
print "\n------------------------------------------";
print "\nperforming string_manipulation...";
print "\n";
string_manipulation();


sub string_manipulation
{
    # EXAMPLE -- print number fixed with two decimal places.
    my $num = 1;

    # force string to have certain width (5), pad with zeros, and have it fixed two decimal places.
    # src: https://stackoverflow.com/a/73976916/14745606
    my $str = sprintf "%05.2f", $num;   # 01.00



    print "\n\tforcing certain width, pad with zeros, and enforce two decimal plances: \n\t\t$num -> apply \'sprint \%05.2f\ ' -> $str\n"; # 1 -> 01.00
}
