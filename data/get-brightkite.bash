#!/bin/bash

curl http://snap.stanford.edu/data/loc-brightkite_totalCheckins.txt.gz \
	| gunzip \
	| tr '\t' ',' \
	| grep -v ,, \
	| python date_sort.py \
	> brightkite.csv
