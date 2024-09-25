
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    name_clean VARCHAR(255),
    image_type VARCHAR(50),
    image VARCHAR(255),
    ready_in_minutes INTEGER,
    cooking_minutes INTEGER,
    preparation_minutes INTEGER,
    health_score NUMERIC(5, 2),
    weight_watcher_smart_points INTEGER,
    price_per_serving NUMERIC(10, 2),
    servings INTEGER,
    spoonacular_source_url VARCHAR(255),
    source_url VARCHAR(255),
    summary TEXT,
    credits_text VARCHAR(255),
    author VARCHAR(255),
    aggregate_likes INTEGER,
    likes INTEGER,
    very_healthy BOOLEAN,
    very_popular BOOLEAN,
    cheap BOOLEAN,
    sustainable BOOLEAN,
    gaps VARCHAR(50),
    low_fodmap BOOLEAN,
    gluten_free BOOLEAN,
    dairy_free BOOLEAN,
    vegan BOOLEAN,
    vegetarian BOOLEAN,
    spoonacular_score NUMERIC(5, 2)
);

CREATE TABLE nutrition (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    percent_carbs NUMERIC(5, 2),
    percent_protein NUMERIC(5, 2),
    percent_fat NUMERIC(5, 2),
    percent_of_daily_needs NUMERIC(5, 2),
    caloric_breakdown TEXT,
    weight_per_serving NUMERIC(10, 2)
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255),
    extended_name VARCHAR(255),
    original_name VARCHAR(255),
    consistency VARCHAR(50),
    aisle VARCHAR(255),
    amount NUMERIC(10, 2),
    unit VARCHAR(50),
    unit_short VARCHAR(10),
    unit_long VARCHAR(50)
);

CREATE TABLE nutrients (
    id SERIAL PRIMARY KEY,
    ingredient_id INTEGER REFERENCES ingredients(id) ON DELETE CASCADE,
    name VARCHAR(255),
    amount NUMERIC(10, 2),
    unit VARCHAR(50),
    percent_of_daily_needs NUMERIC(5, 2)
);

CREATE TABLE instructions (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER,
    step_description TEXT
);

CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255)
);

CREATE TABLE occasions (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255)
);

CREATE TABLE dish_types (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    type_name VARCHAR(255)
);

CREATE TABLE cuisines (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255)
);

CREATE TABLE missed_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255),
    amount NUMERIC(10, 2),
    unit VARCHAR(50),
    aisle VARCHAR(255)
);

CREATE TABLE used_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255),
    amount NUMERIC(10, 2),
    unit VARCHAR(50),
    aisle VARCHAR(255)
);

CREATE TABLE flavonoids (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(255),
    amount NUMERIC(10, 2)
);
