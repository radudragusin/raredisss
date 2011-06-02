rm -vf *.log *.pid *-pys

echo "Starting fresh..."

echo "Start to get data from medical sites."
sh getWeb.sh &

echo "Start to get data from medical databases."
sh getBulk.sh &
