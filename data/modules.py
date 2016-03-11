#!/usr/bin/python
import json
import MySQLdb

# ---------------------------------------------

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="toolkit_yc118")
cur = db.cursor()

# ---------------------------------------------

def getSlot(db, typeID, effectID):
    cur2 = db.cursor()
    cur2.execute("SELECT typeID FROM dgmTypeEffects WHERE typeID = {0} AND effectID = {1}".format(typeID, effectID))
    return cur2.fetchone()

module_classes = dict()

cur.execute("SELECT groupID, groupName FROM invGroups WHERE categoryID = 7")
for res in cur.fetchall():
    groupID = res[0]
    groupName = res[1]
    module_classes[groupName] = groupID

modules = []

for groupName in module_classes:
    cur.execute("SELECT typeID, typeName FROM invTypes WHERE groupID = {0} AND published = 1".format(module_classes[groupName]))
    for res in cur.fetchall():
	typeID = res[0]
	typeName = res[1]

	slot = "?"
	if getSlot(db, typeID, 11):
	    slot = "L"
	elif getSlot(db, typeID, 13):
	    slot = "M"
	elif getSlot(db, typeID, 12):
	    slot = "H"
	elif getSlot(db, typeID, 2663):
	    slot = "R"
	else:
	    continue

	modules.append({'name': typeName, 'slot': slot})

f = open("../webroot/modules.json",'w')
json.dump(modules, f)
f.close()

# ---------------------------------------------
