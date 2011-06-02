ls -1 ../../links/webLinks.*.txt > /dev/null 2>&1
if [ ! "$?" = "0" ];
  then
    echo 'No web link files found!'
    exit 2
fi

mkdir -p ../../links/temp-web
cp ../../links/webLinks.*.txt ../../links/temp-web
for i in ../../links/temp-web/webLinks.*.txt; do 
   mv $i ${i%\.txt}; 
done

for f in ../../links/temp-web/webLinks.*; do 
    rm -rf ../../data/${f#../../links/temp-web/webLinks.}-data
    echo 'Downloading:' ${f#../../links/temp-web/webLinks.}
    wget -b -a web.log -i $f -w 0.5 -x -P ../../data/${f#../../links/temp-web/webLinks.}-data >> web.pid
    echo ${f#../../links/temp-web/webLinks.}.py >> web-pys;
done

rm -r ../../links/temp-web

sed -i 's/[^0-9]*//g' web.pid

python ../getTrec/getTrec.py web
