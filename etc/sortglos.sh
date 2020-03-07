export gls="glossarydefs.csv"
echo "Sort $gls"
tail -n +2 $gls > tosort.csv
head -1 $gls > t.csv
sort tosort.csv >> t.csv
mv t.csv $gls
rm tosort.csv


