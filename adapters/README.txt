How to run queries for hashedcubes from csv:

cat brightkite-32-2016-02-22-tile.csv \
	| cut -d, -f6 \
	| sed 's!^!http://localhost:8000/rest!' \
	| python run_queries.py

How to run queries for hashedcubes from csv:

cat brightkite-32-2016-02-22-tile.csv \
	| cut -d, -f6 \
	| python ./hc_query_to_nc.py
	| python run_queries.py


