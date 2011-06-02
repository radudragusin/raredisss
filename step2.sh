cd buildIndex
nano index_param.json
python addDocno.py 1 index_param.json
javac -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' BuildIndex.java
java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' -Djava.library.path='.:../../lib/' BuildIndex index_param.json
