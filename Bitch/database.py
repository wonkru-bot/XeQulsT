# Space_btwn Codea Due to My fucking phone [one Enterkey=2×]feck
import pymongo 

import os

MG = os.environ.get("MG","") #Doubt @WONKRU_HERE 

XEQULST = os.environ.get("XEQULST","") #Doubt @WONKRU_HERE

myr = pymongo.MongoClient(XEQULST)

bitch = myr[MG]

myrcol = myr["USER"]

def insert(chat_id):

            user_id = int(chat_id)

            user_det = {"_id":user_id,"lg_code":None}

            try:

            	myrcol.insert_one(user_det)            except:

            	pass

def set(chat_id,lg_code):

	 myrcol.update_one({"_id":chat_id},{"$set":{"lg_code":lg_code}})

	 	

def unset(chat_id):

	myrcol.update_one({"_id":chat_id},{"$set":{"lg_code":None}})

def find(chat_id):

	id =  {"_id":chat_id}

	x = myrcol.find(id)

	for i in x:

             lgcd = i["lg_code"]

             return lgcd 

def getid():

    values = []

    for key  in myrcol.find():

         id = key["_id"]

         values.append((id)) 

    return values

def find_one(id):

	return myrcol.find_one({"_id":id})
