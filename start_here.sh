#!/bin/zsh

site_ip=$1
RCONFIG=$(./e1.exp "$site_ip")
site=$(sqlite3 ~/site_id/hosts.db 'SELECT * FROM hosts;' | grep -i "$site_ip")
site_id=$(awk -F\| '{print $1}' <<< "$site")

echo "$site_ip"
echo "$site_id"

format_config=$(echo "$RCONFIG" | grep -E '^(interface (Apphosting|ATM|Ethernet|FastEthernet|FortyGigabitEthernet|FourHundredGigabitEthernet|GigabitEthernet|HundredGigabitEthernet|HundredGigE|Interface_ign|Loopback|Management|Port\-channel|POS|Router|Serial|Switch|TenGigabitEthernet|Tunnel|TwentyFiveGigabitEthernet|TwentyFiveGigE|TwoHundredGigabitEthernet|Vlan)|[[:space:]]+description|[[:space:]]+switchport (access|mode|trunk|voice))' | grep -A5 "interface" | grep -v "\-\-\|pruning");
echo "$format_config" > cisco1.config && ./format_conf.sh;
python3 ./exs.py && python3 rcsv.py "$site_id" "$site_ip";
rm ./cisco1.config;
