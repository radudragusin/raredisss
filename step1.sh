cd getLinks
nano links.param
echo -n 'Delete the existing link files? y or (n):'
read d
if [ "$d" = "y" ];
  then
    rm  -v ../../links/*
fi
python getLinks.py links.param

cd ../getData
sh getData.sh


#cd ../buildIndex
#nano index_param.json
#javac -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' BuildIndex.java
#java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' -Djava.library.path='.:../../lib/' BuildIndex index_param.json

#cd ../runQuery
#nano retrieval_param.json
#javac -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' RunQuery.java
#java -cp '.:../../lib/indri.jar:../../lib/gson-1.7.1.jar' -Djava.library.path='.:../../lib/' RunQuery retrieval_param.json
