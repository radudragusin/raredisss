cd disk/code/runQuery
echo "Running query with arguments:" $@
java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar:../../lib/opencsv-2.2.jar' -Djava.library.path='.:../../lib/' RunQuery "$1" "$2" "$3"
mv ../../results/$3 ~/results/$3
