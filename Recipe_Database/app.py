from flask import Flask, request, make_response
import sqlite3

app = Flask(__name__)

@app.route('/recipes', methods=["POST"])
def create_recipe():
    try:
        # create connection to DB
        db_connection = sqlite3.connect("recipes.db")
        recipes_db = db_connection.cursor()

        # parse information for recipe
        data = request.get_json()
        recipe_name = data["name"]
        recipe_calories = int(data["calories"])
        recipe_ingredients = data['ingredients']

        # search for recipe name already exist
        query = "SELECT id from Recipes WHERE name='{name}'".format(name=recipe_name)
        try:
            recipe_id = recipes_db.execute(query).fetchone()[0]
            if recipe_id:
                # recipe already exists, return error
                db_connection.close()
                return "Recipe already exists", 409
        except: # if query fails, then we do not have this recipe yet
            pass

        # create the recipe
        query = """
                INSERT INTO Recipes
                (name, calories) VALUES ('{name}', {calories}) 
                """.format(name=recipe_name, calories=recipe_calories)
        recipes_db.execute(query)

        # get row id of recipe
        query = "SELECT id from Recipes WHERE name='{name}';".format(name=recipe_name)
        recipe_id = recipes_db.execute(query).fetchone()[0]

        # parse information for the ingredients
        for ingredient in recipe_ingredients:
            ingredient_name = ingredient["name"]
            ingredient_qty = ingredient["quantity"]
            ingredient_units = ingredient["units"]

            # create the ingredient or update the ingredient
            query = """
            INSERT OR IGNORE INTO Ingredients
            (name) VALUES ('{name}') ;
            """.format(name=ingredient_name)
            recipes_db.execute(query)

            # get the ingredient ID
            query = "SELECT id from Ingredients WHERE name='{name}';".format(name=ingredient_name)
            ingredient_id = recipes_db.execute(query).fetchone()[0]

            # add the RecipeComponent row
            query = """
            INSERT INTO RecipeComponents (recipe_id, ingredient_id, quantity, units) 
            VALUES ({recipe_id}, {ingredient_id}, {quantity}, '{units}');
            """.format(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=ingredient_qty, units=ingredient_units)
            recipes_db.execute(query)

        db_connection.commit()
        return "ok", 201

    except Exception:
        # if any issue, return 400
        return "An error occurred", 400
    finally:
        db_connection.close()

@app.route('/recipes', methods=["GET"])
def get_recipe():

    try:
        db_connection = sqlite3.connect("recipes.db")
        recipes_db = db_connection.cursor()

        # generate the filters based on the request
        request_args = request.args

        # extract limit arg. otherwise set to -1 to get all
        try:
            if "limit" in request_args:
                set_limit = abs(int(request_args["limit"]))
            else:
                set_limit = -1
        except ValueError:
            set_limit = -1

        # generate the filters
        filter_list = list()

        # extract name arg
        if "name" in request_args:
            filter_list.append("UPPER(name) LIKE UPPER('%{}%')".format(request_args["name"]))

        # extract calories arg
        if "calories" in request_args:
            try:
                calories = int(request_args["calories"])
                filter_list.append("calories<{}".format(calories))

            except ValueError:
                # if calories is not an integer, then do not add it and continue
                pass

        filters_str = " AND ".join(filter_list)

        # query recipe adhering to the request filter
        query = """
        SELECT * FROM recipes {WHERE} {filters} ORDER BY RANDOM() {LIMIT} {limit_num};
        """.format(
            WHERE="WHERE" if len(filter_list) >0 else "",
            filters=filters_str,
            LIMIT="LIMIT" if set_limit >= 1 else "",
            limit_num= set_limit if set_limit >= 1 else ""
        )

        results = recipes_db.execute(query).fetchall()

        recipes = {recipe[0]: {"name":recipe[1], "calories":recipe[2], "ingredients":[]} for recipe in results}

        # collect the ingredients list required
        for result in results:
            recipe_id, recipe_name, calories = result

            query = """
            SELECT Ingredients.name, RecipeComponents.quantity, RecipeComponents.units 
            FROM RecipeComponents INNER JOIN Ingredients ON RecipeComponents.ingredient_id=Ingredients.id 
            WHERE RecipeComponents.recipe_id = {recipe_id}
            """.format(recipe_id=recipe_id)

            results = recipes_db.execute(query).fetchall()

            for ingredient in results:
                # create dict representing the ingredient
                ingredient_object = {
                    "name": ingredient[0],
                    "quantity": ingredient[1],
                    "units": ingredient[2]
                }
                # add ingredient to recipe
                recipes[recipe_id]["ingredients"].append(ingredient_object)

        return make_response(recipes)


    finally:
        db_connection.close()

@app.route('/recipes', methods=["DELETE"])
def delete_recipe():
    try:
        db_connection = sqlite3.connect("recipes.db")
        recipes_db = db_connection.cursor()

        try:
            recipe_id = int(request.args["id"])
        except (KeyError, ValueError):
            return "Bad Request", 400

        # first delete the recipe components
        query = """
        DELETE FROM RecipeComponents WHERE recipe_id = {recipe_id}; 
        """.format(recipe_id=recipe_id)
        recipes_db.execute(query)


        # second, delete the recipe itself
        query = """
        DELETE FROM Recipes WHERE id = {recipe_id};
        """.format(recipe_id=recipe_id)
        recipes_db.execute(query).fetchall()

        db_connection.commit()
        return "ok", 204
    finally:
        db_connection.close()

if __name__ == '__main__':
    app.run()

# finally:
#     db_connection.close()
