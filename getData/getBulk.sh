# check if any matchin bulkLinks exist
ls -1 ../../links/bulkLinks.*.txt > /dev/null 2>&1
if [ ! "$?" = "0" ];
  then
    echo 'No bulk link files found!'
    exit 2
fi

# copy link files to temp dir
mkdir -p ../../links/temp-bulk
cp ../../links/bulkLinks.*.txt ../../links/temp-bulk


# rename files without extension
for i in ../../links/temp-bulk/bulkLinks.*.txt; do 
   mv $i ${i%\.txt}; 
done


# download all links to destination in background, keep the wget PIDs and save the scripts to run in a file
for f in ../../links/temp-bulk/bulkLinks.*; do 
    rm -rf ../../data/${f#../../links/temp-bulk/bulkLinks.}-data
    echo 'Downloading:' ${f#../../links/temp-bulk/bulkLinks.}
    wget -b -a bulk.log -i $f -w 0.5 -nd -P ../../data/${f#../../links/temp-bulk/bulkLinks.}-data >> bulk.pid
    echo ${f#../../links/temp-bulk/bulkLinks.}.py >> bulk-pys;
done

rm -r ../../links/temp-bulk

# only keep the PID number
sed -i 's/[^0-9]*//g' bulk.pid

python ../getTrec/getTrec.py bulk

