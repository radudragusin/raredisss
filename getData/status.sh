ps aux | grep [w]get
ps aux | grep [p]ython

for i in ../../data/*-data; do echo $i; find $i/ -type f | wc -l; done
