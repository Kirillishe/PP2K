import json

# JSON
file = open(r'json/sample-data.json', 'r')
data = json.load(file)

# VALUES
headings = {'DN' : 50,
            'Description' : 20,
            'Speed' : 7,
            'MTU' : 4}
jsonHeadings = {'dn' : 50,
                'descr' : 20,
                'speed' : 7,
                'mtu' : 4}

# FUNCS
def getHeading(headings : dict):
    for k, v in headings.items():
        yield k + ' '*(v-len(k))
        
def sep(sep, headings : dict):
    for v in headings.values():
        yield sep*(v)
        
def info(data : dict, headings: dict):
    answ = dict()
    for k, v in data.items():
        if k in headings:
            answ[k] = v + ' '*(headings[k] - len(v))
    return answ
        

# MAIN
print("Interface Status")
print('=' * sum(headings.values(), len(headings.keys())-1))
# headings
for head in getHeading(headings):
    print(head, end=' ')
print()
# separator
for s in sep('-', headings):
    print(s, end=' ')
print()
# info
for phys in data['imdata']:
    i = info(phys['l1PhysIf']['attributes'], jsonHeadings)
    print(i['dn'], i['descr'], i['speed'], i['mtu'])