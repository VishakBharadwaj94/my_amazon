from flask import Flask, request,render_template,redirect,url_for,session
from models.user_model import user_signup,search_user_by_username,Product_addition,check_user,seller_products,buyer_products,cart_details,update_cart_details,search_products_in_page
from data import articles
import pdb

app = Flask(__name__)

app.secret_key = 'string'





@app.route("/")
@app.route("/home")

def home():

	return render_template("home.html")



@app.route("/welcome")
def welcome():


	if ("user_id" in session.keys()):
		
		
		return render_template('loginsuccess.html')
		
	else :

		return render_template('welcome.html',login ="False")


@app.route("/about")

def about():

	return render_template("about.html")

@app.route("/contact")

def contact():

	return render_template("contact.html")



@app.route("/login", methods=['GET','POST'])

def login():

	if request.method == 'POST':

		inbound_username = request.form['username']
		existing_user = search_user_by_username(inbound_username)
		if (existing_user is None):
			return 'you have to signup first'

		elif(request.form['password']==existing_user['password']):
			print ("login successfull, redirecting to products page")
		
			session['user_id'] = str(existing_user['_id'])
			session['account_type']=existing_user['account_type']
			session['username']=existing_user['username']
		

			return redirect(url_for("welcome"))


		else: 
			return render_template('error.html', message= 'username or password incorrect')

	else:

		if ("user_id" in session.keys()):
		
		
			return render_template('loginsuccess.html')

		else:

			return render_template("welcome.html",login ="False")




@app.route('/signup',methods=["POST"])
def signup():
	user_info={}
	user_info["username"] = request.form["username"]
	user_info["password"] = request.form["password"]
	#rpassword=request.form["rpassword"]
	user_info["email"] =  request.form["email"]
	user_info["account_type"] = request.form["account_type"]

	



	if user_info["account_type"]=="buyer":

		user_info["cart"]=[]

	if check_user(user_info["username"]) is None:

		results=user_signup(user_info)
		if(results is True):

			session['user_id'] = str(user_info['_id'])	
		return redirect(url_for('welcome'))
		
	else:	

		return 'the username already exists.please go back and enter another username'


@app.route("/addproductspage",methods=["POST"])

def addproductspage():
	return render_template('addproducts.html')


@app.route('/addproducts', methods=["POST"])
def addproducts():
	product_info={}
	product_info["product name"] = request.form["name"]
	product_info["price"] = int(request.form["price"])
	product_info["description"] =  request.form["product_description"]
	product_info["user_id"]=session['user_id']
	product_info["username"] =session["username"]
	results =Product_addition(product_info)

	return 'product added'


@app.route("/products", methods=['POST','GET'])

def products():
	if session["account_type"] =="seller":
		result = seller_products(session["user_id"])
	else:
		result = buyer_products()
	return render_template("products.html" ,result=result)


@app.route("/searchproducts", methods=["POST"])

def search_products():

	word = request.form["search"]
	search = search_products_in_page(word)

	if search is None:
		return "No products found"

	else:

		return render_template("searchproducts.html",search=search)

	



@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user_id', None)
   return redirect(url_for('home'))






@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
	
	product_id =request.form["product_id"]
	
	quantity=int(request.form["quantity"])
	update_cart_details(session["user_id"],product_id,quantity)
	
	return redirect(url_for("cart_page"))

@app.route('/cart_page')
def cart_page():
	cart= cart_details(session["user_id"])
	return render_template("cart_page.html",cart=cart)

@app.route('/articles')
def Articles():

	Articles=articles()

	return render_template("articles.html",articles=Articles)

@app.route('/article/<string:id>')

# note the change in the decorator above, article not articles
#the ID will be of type string and be fed into the url 

def Article(id):

	return render_template("article.html",id=id)


if(__name__ == "__main__"):
	app.run(debug=True)