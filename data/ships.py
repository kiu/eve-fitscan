#!/usr/bin/python
import json
import MySQLdb

# ---------------------------------------------

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="toolkit_yc118")
cur = db.cursor()

# ---------------------------------------------

def getSlot(db, typeID, attributeID):
    cur2 = db.cursor()
    cur2.execute("SELECT valueInt, valueFloat FROM dgmTypeAttributes WHERE typeID = {0} AND attributeID = {1}".format(typeID, attributeID))
    res = cur2.fetchone()
    slot = 0
    if res:
	if res[0]:
	    slot = int(res[0])
	if res[1]:
	    slot = int(res[1])
    return slot


ship_classes = dict()

cur.execute("SELECT groupID, groupName FROM invGroups WHERE categoryID = 6")
for res in cur.fetchall():
    groupID = res[0]
    groupName = res[1]
    ship_classes[groupName] = groupID

ships = []

for groupName in ship_classes:
    cur.execute("SELECT typeID, typeName FROM invTypes WHERE groupID = {0} AND published = 1".format(ship_classes[groupName]))
    for res in cur.fetchall():
	typeID = res[0]
	typeName = res[1]
	slotLow = getSlot(db, typeID, 12)
	slotMed = getSlot(db, typeID, 13)
	slotHgh = getSlot(db, typeID, 14)
	slotRig = getSlot(db, typeID, 1137)

	ships.append({'class': groupName, 'name': typeName, 'slotLow': slotLow, 'slotMed': slotMed, 'slotHgh': slotHgh, 'slotRig': slotRig})

f = open("../webroot/ships.json",'w')
json.dump(ships, f)
f.close()

# ---------------------------------------------
