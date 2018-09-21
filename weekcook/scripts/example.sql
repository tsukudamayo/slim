

INNER JOIN (

    SELECT
        *
    FROM (
    
        SELECT
            ri.recipe_id
            , r.recipe_name
            , ing.ingredient_name
            , ri.recipe_ingredient_id
            , ri.ingredient_id
            , rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS rank2
        
        FROM
            Recipe_Ingredients AS ri
            INNER JOIN Ingredients AS ing
            ON ri.ingredient_id = ing.ingredient_id
            INNER JOIN Recipes AS r
            ON r.recipe_id = ri.recipe_id
            INNER JOIN Genre AS g
            ON r.genre_id = g.genre_id
            INNER JOIN Food_Types AS ft
            ON r.food_type_id = ft.food_type_id
            INNER JOIN Dish_Types AS dt
            ON r.dish_type_id = dt.dish_type_id
            INNER JOIN Picture AS p
            ON r.picture_id = p.picture_id
        ) AS table2
    
    WHERE table2.ingredient_id = 36



