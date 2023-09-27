DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS RecipeComponents;

CREATE TABLE Recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  calories INTEGER
);

CREATE TABLE Ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE RecipeComponents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  units TEXT,
  FOREIGN KEY (recipe_id) REFERENCES Recipes (id),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredients (id)
);