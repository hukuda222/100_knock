wc po.txt
sed 's/\t/ /g' po.txt
cut -f 1  po.txt >> col1_.txt 
cut -f 2  po.txt >> col2_.txt 
paste col1_.txt col2_.txt >> col_.txt
head -n 10 po.txt
tail -n 10 po.txt
split -l 8 po.txt poyo-
cut -f 1 po.txt | sort | uniq
sort -t "\t" -k 3 -r po.txt
cut -f 1 po.txt |sort|uniq -c|sort -k 1
