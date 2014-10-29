max_grep
========

A python implemented grep to filter out virus and human from a sam

# Virus:
`grep chrvirus $1 | sed '/@SQ/d;/@PG/d' > $2 `  
$1 = file  
$2 = file_Human_Virus_no_header.txt

# Human:
`grep chr[1-9,XYM] $1 | sed '/@SQ/d;/@PG/d' > $2 && No_homopolymerA_or_T_in_STAR_output_files_regular_expressions_Match_any_20_no_endog_retroviruses_hani.py $2 && more $3 |awk '{print $1, $3}' | sort | uniq -c > $4 && more $4 |awk '{print $2, $3}' > $5 && more $5 | awk '!x[$1]++' > $6 && more $6 | awk '{print $2}' | sort | uniq -c > $7 && rm $1; rm $2; rm $3; rm $4; rm $5; rm $6;`  
$1 = file  
$2 = file_Human_Only_no_header.txt  
$3 = file_Human_Only_no_header.txt.no_polyA_or_polyT_reads.txt  
$4 = file_Human_Only_no_header.txt​.no_polyA_or_polyT_reads.txt_temp1  
$5 = file_Human_Only_no_header.txt​.no_polyA_or_polyT_reads.txt_temp2  
$6 = file_Human_Only_no_header.txt​.no_polyA_or_polyT_reads.txt_temp3  
$7 = file_Human_Only_quantification_unique_count.txt  
