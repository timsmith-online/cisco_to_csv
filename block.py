import pandas as pd
import os
import xlsxwriter

cur_dir = "/Users/timothy.s/port_map"

data = pd.read_csv('dhcp_snooping.csv')
data1 = pd.read_csv('outputs.csv')
data2 = pd.read_csv('brief.csv')
data3 = pd.read_csv('status.csv')

list_csv = [data, data1, data2, data3]
name_csv = ['dh.csv', 'out.csv', 'bri.csv', 'stat.csv']

for csv_file in range(len(list_csv)):
	cur_df = list_csv[csv_file]
	if 'interface' in cur_df.columns:
		cur_df["interface"] = cur_df["interface"].replace({
			'FastEthernet': 'Fa',
		  'TenGigabitEthernet': 'Te',
		  'TwentyFiveGigabitEthernet': 'Twe',
		  'FortyGigabitEthernet': 'Fo',
		  'HundredGigabitEthernet': 'Hu',
		  'TwoHundredGigabitEthernet': 'Two',
		  'FourHundredGigabitEthernet': 'Fo',
		  'GigabitEthernet': 'Gi',
		  'TwentyFiveGigE': 'Twe',
		  'HundredGigE': 'Hu',
		  'Ethernet': 'Et',
		  'Serial': 'Se',
		  'ATM': 'At',
		  'POS': 'Po',
		  'Loopback': 'Lo',
		  'Vlan': 'Vl',
		  'Port-channel': 'Po',
		  'Tunnel': 'Tu',
		  'Apphosting': 'Ap',
		  'Interface_ign': 'In',
		  'Management': 'Mg',
		  'Router': 'Ro',
		  'Switch': 'Sw'}, regex=True)
		cur_df.to_csv(name_csv[csv_file])
	else:
		cur_df.to_csv(name_csv[csv_file])

data = pd.read_csv('dh.csv')
data1 = pd.read_csv('out.csv')
data2 = pd.read_csv('bri.csv')
data3 = pd.read_csv('stat.csv')

df = pd.DataFrame(data)
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

df = df[['interface', 'ip_address', 'mac_address']]
y = df.dropna().empty
if y == True:		
	combined_df = pd.merge(df1, df2, on="interface", how="right")
	combined_df = pd.merge(df3, combined_df, on="interface", how="right")
	combined_df = combined_df[['interface', 'description', 'vlans', 'data_vlan', 'vlan_type', 'switchport mode', 'status_y', 'duplex', 'speed', 'type']]
	with pd.ExcelWriter('final.xlsx', engine='xlsxwriter') as writer: 
		combined_df.to_excel(writer, sheet_name='sheet1', index=False)
else:
	combined_df = pd.merge(df, df1, on="interface", how="right")
	combined_df = pd.merge(df2, combined_df, on="interface", how="right")
	combined_df = pd.merge(df3, combined_df, on="interface", how="right")
	combined_df = combined_df[['interface', 'status_y', 'ip_address', 'mac_address', 'description', 'vlans', 'data_vlan', 'vlan_type', 'switchport mode', 'duplex', 'speed', 'type']]
	with pd.ExcelWriter('final.xlsx', engine='xlsxwriter') as writer: 
		combined_df.to_excel(writer, sheet_name='sheet1', index=False)







