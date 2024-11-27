#!/bin/zsh

site_ip=$1
RCONFIG=$(./e1.exp "$site_ip")
site=$(cat /etc/hosts | grep -i "$site_ip" | awk -F, '{print $1 " " $2}')
site_id=$(awk '{print $1}' <<< "$site")


sh_dhcp=$(echo "$RCONFIG" | sed -n '/sh ip dhcp snooping binding/,/show ip interface brief/p')
sh_ip_int_brief=$(echo "$RCONFIG" | sed -n '/show ip interface brief/,/show int status/p' | grep -v "#")
sh_int_status=$(echo "$RCONFIG" | sed -n '/show int status/,/exit/p' | grep -v "#")

l2_l3=$(echo "$sh_ip_int_brief" | sed '1d' | grep -iv "vlan\|vl\|unassigned")

#Status
column_numbs() {
	
	local arg1=$1
	num_col=$(echo "$arg1" | awk -F, '{print NF}' | sort | uniq -c | sort -h | tail -n1 | awk '{print $2}')
	num_col=$((num_col - 1))
	return 0

}

# Status
status_func() {

	sh_int_status=$(echo "$sh_int_status" | 
		sed -r 's/([A-Za-z]{2,3}[0-9\/]+\ )(.*)( connected| notconn| disabled| sfpAbsent| sfpInvali| xcvrAbsen| noOperMe)/\1 \3/g' | tr -d "\r")


	sh_int_status=$(echo "$sh_int_status" | 
		grep -i "auto\|full\|half" |
		awk '{print $1 " " $2 " " $3 " " $4 " " $5 " " $6}' | 
		tr ' ' ',')

	column_numbs "$sh_int_status"
	sh_int_status=$(echo "$sh_int_status" | awk -F, -v col="$num_col" '{ if (NF > col) print }')

	headers_status=$(echo "interface,status,vlan,duplex,speed,type")
	echo "$headers_status" > ./status.csv
	echo "$sh_int_status" >> ./status.csv

	#echo "$headers_status"	
	#echo "$sh_int_status" 

	return 0

}


format_config=$(echo "$RCONFIG" | grep -E '^(interface (Apphosting|ATM|Ethernet|FastEthernet|FortyGigabitEthernet|FourHundredGigabitEthernet|GigabitEthernet|HundredGigabitEthernet|HundredGigE|Interface_ign|Loopback|Management|Port\-channel|POS|Router|Serial|Switch|TenGigabitEthernet|Tunnel|TwentyFiveGigabitEthernet|TwentyFiveGigE|TwoHundredGigabitEthernet|TwoGigabitEthernet|Vlan)|[[:space:]]+description|[[:space:]]+switchport (access|mode|trunk|voice))' | grep -A6 "interface" | grep -v "\-\-\|pruning");
echo "$format_config" > cisco1.config && ./g3.sh;
python3 ./exs.py && python3 ./rcsv.py "$site_id" "$site_ip";
rm ./cisco1.config;

# Snooping
sh_dhcp=$(sed -n '/----/,/Total/p' <<< "$sh_dhcp") 
sh_dhcp=$(sed '1d;$d' <<< "$sh_dhcp")

# Brief
sh_ip_int_brief=$(sed 's/administratively down/admin_down/g;1d' <<< "$sh_ip_int_brief")




echo "mac_address,ip_address,interface" > dhcp_snooping.csv
echo "interface,status" > brief.csv


if [[ -z "$l2_l3" ]]; then	
	
	echo "\n"
	echo "$site_id = This is a layer_2 device"
	echo "$sh_dhcp" | awk '{print $1 "," $2 "," $6}' >> dhcp_snooping.csv
	echo "$sh_ip_int_brief" | awk '{print $1 "," $5}' >> brief.csv
else
	
	echo "\n"
	echo "$site_id = This is a layer_3 device"
	echo "$sh_dhcp" | awk '{print $1 "," $2 "," $6}' >> dhcp_snooping.csv
	echo "$sh_ip_int_brief" | awk '{print $1 "," $5}' >> brief.csv
fi


status_func

python3 ./g4.py;
