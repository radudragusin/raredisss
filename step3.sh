cd runQuery
nano retrieval_param.json
javac -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar:../../lib/opencsv-2.3.jar' RunQuery.java
java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar:../../lib/opencsv-2.3.jar' -Djava.library.path='.:../../lib/' RunQuery retrieval_param.json
