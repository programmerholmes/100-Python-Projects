# https://documenter.getpostman.com/view/51396904/2sBXVfiWiC

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

class Base(DeclarativeBase):
    pass


##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            No longer needed in the newer version
db = SQLAlchemy(model_class=Base)
db.init_app(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    # A helper method to turn a database row into a dictionary
    def to_dict(self):
        # This is much cleaner than manually typing every key!
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

# @app.route('/random', methods=["GET"])
# def random():
#     pass
## But GET is allowed by default on all routes.
# So this is much simpler:

@app.route('/random')
def get_random_cafe():
    # Execute a select query to get all cafes
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()

    if all_cafes:
        random_cafe = random.choice(all_cafes)
        # We use our helper method to convert the object to a dictionary for JSON
        return jsonify(cafe=random_cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "No cafes in the database."}), 404



@app.route('/all')
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    all_cafes_dict = [cafe.to_dict() for cafe in all_cafes]   # list comprehension, a list of dictionaries in this case
    return jsonify(cafes=all_cafes_dict)


# @app.route('/search/<location>')  by doing this it looks like .../search/London, still correct but we want it
# to be like .../search?loc=London, the standard, so we will use the other way, which means no argument parameter

@app.route('/search')
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()

    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=["POST"])
def post_new_cafe():

    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(int(request.form.get("sockets"))),
        has_toilet=bool(int(request.form.get("toilet"))),
        has_wifi=bool(int(request.form.get("wifi"))),
        can_take_calls=bool(int(request.form.get("calls"))),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),

    )

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"Success": "Successfully added the new cafe."})


@app.route('/update-price/<int:cafe_id>', methods=["Patch"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")

    cafe = db.session.get(Cafe, cafe_id)

    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success="Successfully updated the price."), 200
    else:
        return jsonify(error={"Not Found": "No cafe found with that ID"}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")

    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403




if __name__ == '__main__':
    app.run(debug=True)




## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)




"""
The to_dict Helper: This is a crucial "pro" move. 
Since jsonify can't handle a database object directly, 
we need a dictionary. Instead of writing out every single column name manually, 
this line loops through your table's columns and builds the dictionary for you automatically.

The jsonify() function is a specialized "translator." 
It knows how to translate standard Python data 
(Strings, Integers, Booleans, Lists, and Dictionaries) into JSON format.

if this isn't used return {column.name: getattr(self, column.name) for column in self.__table__.columns},
This is the dictionary comprehension, since jsonify understands dictionaries, that's why we convert our 
database data using dict comprehension. 

If we decide not to use this function at all, we can still work a way around it, but in that case, we would
manually have to entry each entry in the jsonify, as it can't read directly from the database.  And it would look
like this 


 return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })
    
Now since we have used it, it looks like this, 

 return jsonify(cafe=random_cafe.to_dict())

Big difference right, yeah we are going pro.

"""


"""
what it means 

3. Breaking Down the "Pro" Helper
Now look at the magic line: return {column.name: getattr(self, column.name) for column in self.__table__.columns}

This is a Dictionary Comprehension. It’s like a for loop compressed into one line.

self.__table__.columns: Every SQLAlchemy model has a hidden attribute called __table__. 
This part says: "Look at the blueprint of this table and give me a list of all the 
column names (id, name, location, etc.)."

for column in ...: We start a loop through those columns.

column.name: This is the "Key" (e.g., "name").

getattr(self, column.name): This is a built-in Python function. 
It means: "Go to this specific cafe (self) and get the value stored in the attribute named column.name."

If the column name is "coffee_price", it gets "$2.50".

"""


"""
Having said that, then you can't do things like making sub-sections, like these 

return jsonify(cafe={
        #Omit the id from the response
        # "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        
        #Put some properties in a sub-category
        "amenities": {
          "seats": random_cafe.seats,
          "has_toilet": random_cafe.has_toilet,
          "has_wifi": random_cafe.has_wifi,
          "has_sockets": random_cafe.has_sockets,
          "can_take_calls": random_cafe.can_take_calls,
          "coffee_price": random_cafe.coffee_price,
        }
    })
    
well, everything has its ups and downs.  


"""

""" Method 2 

def to_dict(self):
        #Method 2. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


"""