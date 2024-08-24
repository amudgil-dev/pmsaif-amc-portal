### listing pids listening on port 5002

sudo lsof -n -i :5002 | grep LISTEN
