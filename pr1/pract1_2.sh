awk '{print $2, $1}' /etc/protocols | sort -nr | head -n 5
