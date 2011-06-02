# Run query
# --- arguments: query text, output name
cd ../runQuery
echo "Running query with arguments:" $@
java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar:../../lib/opencsv-2.2.jar' -Djava.library.path='.:../../lib/' RunQuery "$1" index_rare "$2"

# Rerank results
# --- uses the results outputed from running the query
cd ../dumpIndex
python rerank.py ../../results/$2 index_rare

mv ../../results/$2 ~/results/$2