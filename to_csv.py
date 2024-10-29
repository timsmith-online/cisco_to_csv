import pandas as pd
import numpy as np
import sys

# args from zsh script
script_name = sys.argv[0]
if len(sys.argv) > 1:
	first_arg = sys.argv[1]
	second_arg = sys.argv[2]
else:
	print("No argument provided.")


data = pd.read_csv('./output.csv')
df = pd.DataFrame(data)


df['data_vlan'] = df[['switchport access']]

# Merge access and voice vlans -> to int -> to str
df['vla'] = df[['switchport access', 'switchport voice']].apply(lambda x: ','.join(x.dropna().astype(int).astype(str)), axis=1)

# Merge trunk ports -> to str
df['vlans'] = df[['switchport trunk', 'vla']].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
# object to str
df['vlans'] = df['vlans'].astype('string')

# test code
# df['vlans'] = df[['switchport trunk', 'vla']].apply(lambda x: ','.join(x.dropna().astype(int).astype(str)), axis=1)
# df['vl'] = df['vlans'].apply(lambda x: x.rstrip(','))
#non_numeric = df[df['vlans'].apply(lambda x: not str(x).isdigit())]
#df['yach'] = df[df['vlans'].apply(lambda x: not str(x).isdigit())]

# If 2 vlan tagged, not, untagged
df['vlan_type'] = df['vlans'].apply(lambda x: 'tagged' if ',' in x else 'untagged')

# No tag if interface = vlan
df.loc[df['interface'].str.contains('Vlan', na=False), 'vlan_type'] = np.nan

# Columns
df = df[['interface', 'description', 'vlans', 'data_vlan', 'vlan_type', 'switchport mode']]
# df = df[['interface', 'description', 'vlans', 'data_vlan', 'vlan_type', 'switchport mode', 'vl']]
print(df.dtypes)

# get from site name from DB or /etc/hosts
first_arg = first_arg + "_" + second_arg + ".csv"

df.to_csv(first_arg, index=False)
