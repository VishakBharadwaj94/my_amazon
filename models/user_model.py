from pymongo import MongoClient
from bson.objectid import ObjectId
from fuzzywuzzy import fuzz

client = MongoClient()
db = client['dummy_amazon']



def user_signup(user_info):
	#save user info dictionary inside mongo


	results = db['users'].insert_one(user_info)

	return True 

def check_user(username):
	filter_query = {'username' :username}
	results= db['users'].find(filter_query)

	if(results.count()>0):
		return results.next()

	else:
		return None

def Product_addition(product_info):
	#saves the products inside mongoDB
	results = db['products'].insert_one(product_info)

	return True


def search_user_by_username(username):
	filter_query = {'username' :username}
	results = db['users'].find(filter_query)

	if(results.count()>0):
		return results.next()

	else:
		return None 



def products_by_username(username):
    filter_query = {'username' : username}
    results = db['products'].find(filter_query)
    results['product name']


def seller_products(user_id):
	ans =[]
	filter_query = {'user_id': user_id}
	results = db["products"].find(filter_query)
	for post in results:
		ans.append(post)
		#ans =list(results)
	return ans

def buyer_products():
	ans =[]
	result = db["products"].find({})
	#you can also use $natural to skip a step in the above find() method which gives you the order
	#you entered. but with natural, it just gives the op the way it has been stored in memory so time less

	#result=db["products"].find().sort([('$natual')])	
	for post in result:
		ans.append(post)
	return ans


	
def cart_details(user_id):
	results =[]
	
	filter_query1 = {"_id":ObjectId(user_id)}
	result = db["users"].find_one(filter_query1)
	cart_list=result["cart_details"]

	for item in cart_list:
		filter_query2 = {"_id":ObjectId(item["product_id"])}
		results.append(db["products"].find_one(filter_query2))
	return results	

def update_cart_details(user_id,product_id,quantity):
    user_info = db["users"].find_one({"_id":ObjectId(user_id)})
    cart_dict = user_info["cart"]
    db["users"].update({"_id" : ObjectId(user_id)},{"$inc" : {"cart."+product_id : quantity}})

    return True

def remove_item(product_id,user_id):
    user_info = db['users'].find_one({"_id":ObjectId(user_id)})
    cart_dict = user_info['cart']
    cart_dict.pop(product_id)
    db["users"].update({"_id": ObjectId(user_id)},{"$unset": {"cart."+product_id: ""}})

    return True		 

#def search_products_in_page(search):

#	result=[]
#	a=db["products"].find_one()

#	for dict1 in a:

#		if fuzz.ratio(dict1["product name"],search)>80:

#		so what has to be done first is the comparison and then return the output

#	return result

#	result=[]
#	filter_query = {"product name" : search}
#	result = db['products'].find(filter_query)
#	return result




