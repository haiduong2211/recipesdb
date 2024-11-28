CREATE TABLE "Recipe_Dim" (
  "recipe_id" integer PRIMARY KEY,
  "recipe_name" varchar NOT NULL,
  "recipe_description" varchar,
  "instructions" JSONB,
  "cuisine" varchar[],
  "category" varchar[],
  "source" JSONB,
  "serving" integer,
  "vegan" boolean,
  "vegetarian" boolean,
  "dish_type" varchar[]
);

CREATE TABLE "User_Dim" (
  "user_id" integer PRIMARY KEY,
  "user_name" varchar NOT NULL,
  "country" varchar,
  "signup_date" date NOT NULL
);

CREATE TABLE "Ingredient_Dim" (
  "ingredient_id" integer PRIMARY KEY,
  "ingredient_name" varchar NOT NULL,
  "category" varchar
  "calories" float,
  "fat" float,
  "carbs" float,
  "protein" float,
  "sugar" float,
  "fiber" float,
  "cholesterol" float,
  "sodium" float
);

CREATE TABLE "Date_Dim" (
  "date_id" integer PRIMARY KEY,
  "date" date UNIQUE,
  "year" integer,
  "month" integer,
  "day" integer,
  "day_of_week" integer,
  "is_weekend" boolean
);

CREATE TABLE "Recipe_Ingredients" (
  "recipe_ingredient_id" integer PRIMARY KEY,
  "recipe_id" integer NOT NULL,
  "ingredient_id" integer NOT NULL,
  "unit_of_measure" varchar,
  "quantity" float
);

CREATE TABLE "Recipe_Fact" (
  "recipe_id" integer NOT NULL,
  "user_id" integer NOT NULL,
  "date_id" integer NOT NULL,
  "rating" float NOT NULL,
  "review_count" integer NOT NULL,
  "prep_time_minutes" integer NOT NULL,
  "cook_time_minutes" integer NOT NULL,
  "total_time_minutes" integer NOT NULL,
);

COMMENT ON COLUMN "Recipe_Dim"."source" IS 'Source of the recipe (e.g., website, author, link, view_count)';
COMMENT ON COLUMN "Recipe_Dim"."serving" IS 'Number of servings the recipe yields';
COMMENT ON COLUMN "Recipe_Dim"."vegan" IS 'True if the recipe is vegan, else False';
COMMENT ON COLUMN "Recipe_Dim"."vegetarian" IS 'True if the recipe is vegetarian, else False';
COMMENT ON COLUMN "Recipe_Dim"."dish_type" IS 'Type of dish (e.g., appetizer, main course, dessert)';
COMMENT ON COLUMN "Recipe_Ingredients"."unit_of_measure" IS 'Unit of measure (e.g., grams, cups, tablespoons)';
COMMENT ON COLUMN "Recipe_Ingredients"."quantity" IS 'quantity value for the ingredient';

ALTER TABLE "Recipe_Fact" ADD FOREIGN KEY ("recipe_id") REFERENCES "Recipe_Dim" ("recipe_id");
ALTER TABLE "Recipe_Fact" ADD FOREIGN KEY ("user_id") REFERENCES "User_Dim" ("user_id");
ALTER TABLE "Recipe_Fact" ADD FOREIGN KEY ("date_id") REFERENCES "Date_Dim" ("date_id");

ALTER TABLE "Recipe_Ingredients" ADD FOREIGN KEY ("recipe_id") REFERENCES "Recipe_Dim" ("recipe_id");
ALTER TABLE "Recipe_Ingredients" ADD FOREIGN KEY ("ingredient_id") REFERENCES "Ingredient_Dim" ("ingredient_id");

-- -- Indexes for frequently queried columns
-- CREATE INDEX idx_recipe_fact_recipe_id ON "Recipe_Fact" ("recipe_id");
-- CREATE INDEX idx_recipe_fact_user_id ON "Recipe_Fact" ("user_id");
-- CREATE INDEX idx_recipe_fact_date_id ON "Recipe_Fact" ("date_id");

-- CREATE INDEX idx_recipe_ingredients_recipe_id ON "Recipe_Ingredients" ("recipe_id");
-- CREATE INDEX idx_recipe_ingredients_ingredient_id ON "Recipe_Ingredients" ("ingredient_id");
