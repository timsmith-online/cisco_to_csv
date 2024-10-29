#!/bin/zsh

v1=$(cat cisco1.config | tr -d "\r")

v2=$(echo "$v1" | grep -n switchport | sed -n '/switchport trunk allowed vlan/,/switchport mode trunk/p')

need_add=$(echo "$v2" | grep -E -A1 "switchport trunk allowed vlan [0-9]" | grep -B2 "\-\-" | grep -v "add\|\-\-" | awk '{print $1}')

while read -r items; do 
	v3=$(echo "$v2" | grep switchport | sed -n "/^${items} switchport/,/switchport mode trunk/p")
	v4=$(echo "$v3" | sed '1d;$d' | awk '{print $7}' | tr "\n" ",")
	item=$(echo "$items" | tr -d ":")
 	v1=$(echo "$v1" | sed "${item}s/$/,${v4}/")
done <<< "$need_add"

#echo "$v1" | grep -v add | sed -E 's/^( switchport trunk allowed vlan.*[^,])$/\1,/' > cisco.config
echo "$v1" | grep -v add | sed -E 's/,$//g' > cisco.config
