cd /home/www-data/master/code/runQuery
echo "Running query with arguments:" $@
java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar:../../lib/opencsv-2.3.jar' -Djava.library.path='.:../../lib/' RunQuery "$1" "$2" "$3"

cd ../dumpIndex/
echo "Reranking the results"
python rerank.py ../../results/$3 $2

mv ../../results/$3 /home/www-data/web2py/results/$3
