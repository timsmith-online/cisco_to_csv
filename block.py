import csv

# cisco.config is formated before python script
with open('cisco.config', 'r') as file:
    config_text = file.read()

blocks = []
current_block = {}

lines = config_text.strip().splitlines()

# Create block splitting on interface
for line in lines:
    line = line.strip()
    if line.startswith('interface '):
        if current_block:
            blocks.append(current_block)
        current_block = {
            'interface': line.split('interface ')[1],
            'description': '',
            'switchport trunk': '',
            'switchport access': '',
            'switchport mode': '',
            'switchport voice': ''
        }
    # Block Condition
    elif line.startswith('description '):
        current_block['description'] = line.split('description ')[1]
    elif line.startswith('switchport trunk allowed vlan '):
        current_block['switchport trunk'] = line.split('switchport trunk allowed vlan ')[1]
    elif line.startswith('switchport access vlan '):
        current_block['switchport access'] = line.split('switchport access vlan ')[1]
    elif line.startswith('switchport mode '):
        current_block['switchport mode'] = line.split('switchport mode ')[1]
    elif line.startswith('switchport voice vlan '):
        current_block['switchport voice'] = line.split('switchport voice vlan ')[1]

if current_block:
    blocks.append(current_block)

fieldnames = ['interface', 'description', 'switchport trunk', 'switchport add', 'switchport access', 'switchport mode', 'switchport voice']

# output.csv will be so leave it as is
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for block in blocks:
        writer.writerow(block)

print("config done")
