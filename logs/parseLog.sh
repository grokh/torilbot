# collect historical account info from all logs
grep "\[36m\@" * > accounts.log
grep "\x1B\[0m\x1B\[0m\[\x1B\[37m" * > who.log
# remove regular and 256 ansi color codes
sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?(;[0-9]{1,3})?)?[m|K]//g" <accounts.log >accounts.txt
sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?(;[0-9]{1,3})?)?[m|K]//g" <who.log >who.txt
# remove log name, reformat date
sed -r "s/[a-zA-Z]+.([0-9]{4}).([0-9]{2}).([0-9]{2}).txt:/Date:\1-\2-\3,/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/[a-zA-Z]+.([0-9]{4}).([0-9]{2}).([0-9]{2}).txt:/Date:\1-\2-\3,/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
# remove RP flag, AFK flag, LFG flag
sed -r "s/\(RP\) //" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/\(RP\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\(AFK\) //" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/\(AFK\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\(LFG\) //" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/\(LFG\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\(inv\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\(In Dark\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\(Daylight\)[ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/\[RETURN for more, q to quit\][ ]?//" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
# remove crap i do for targeting
sed -r 's/\([0-9]\)[ ]?//' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/\([a-z]\)[ ]?//' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/\([0-9]\)[ ]?//' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/\([a-z]\)[ ]?//' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
# format accounts better
sed -r "s/\(@([a-zA-Z]+)\)/Account:\1/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
# format races better
sed -r "s/\(([a-zA-Z -]+)\)/,Race:\1,/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/\(([a-zA-Z -]+)\)/,Race:\1/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
# remote titles and last names
sed -r "s/(\] )([a-zA-Z]+) [^\`]*(,Race)/\1Name:\2, Race/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/(\] )([a-zA-Z]+) [^\`]*(,Race)/\1Name:\2, Race/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
# format levels and classes
sed -r "s/,\[([0-9 ]+) ([a-zA-Z -]+)\] Name/, Level:\1, Class:\2, Name/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/,\[([0-9 ]+) ([a-zA-Z-]+)\] Name/, Level:\1, Class:\2, Name/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/Level: /Level:/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/Level: /Level:/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r "s/[ ]+, Name:/, Name:/" <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r "s/[ ]+, Name:/, Name:/" <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
# turn into true csv with just values
sed -r 's/Date://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/Date://' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/ Level://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/ Level://' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/ Class://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/ Class://' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/ Name://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/ Name://' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/ Race://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/ Race://' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
sed -r 's/ Account://' <accounts.txt >accounts.tmp
rm accounts.txt;mv accounts.tmp accounts.txt
sed -r 's/\[([0-9 ]{2}) A-P\]/\1,A-P,/' <who.txt >who.tmp
rm who.txt;mv who.tmp who.txt
