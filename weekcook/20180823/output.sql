-- SELECT
-- 	*
-- FROM (
--      SELECT DISTINCT
--      	    ri.recipe_id
-- 	    , r.recipe_name
-- 	    , r.recipe_name_kana
-- 	    , r.introductory_essay
-- 	    , dt.dish_type_name
-- 	    , g.genre_name
-- 	    , ft.food_type_name
-- 	    , p.file_name
--      FROM
-- 	    Recipe_Ingredients AS ri
--  	    INNER JOIN Ingredients AS ing
-- 	    ON ri.ingredient_id = ing.ingredient_id
--  	    INNER JOIN Recipes AS r
-- 	    ON r.recipe_id = ri.recipe_id
--  	    INNER JOIN Genre AS g
-- 	    ON r.genre_id = g.genre_id
--  	    INNER JOIN Food_Types AS ft
-- 	    ON r.food_type_id = ft.food_type_id
--  	    INNER JOIN Dish_Types AS dt
-- 	    ON r.dish_type_id = dt.dish_type_id
-- 	    INNER JOIN Picture AS p
-- 	    ON r.picture_id = p.picture_id
--      WHERE
-- 	    ing.ingredient_id IN (36)

-- INTERSECT SELECT DISTINCT
-- 	    ri.recipe_id
-- 	    , r.recipe_name
-- 	    , r.recipe_name_kana
-- 	    , r.introductory_essay
-- 	    , dt.dish_type_name
-- 	    , g.genre_name
-- 	    , ft.food_type_name
-- 	    , p.file_name
--      FROM
-- 	    Recipe_Ingredients AS ri
--  	    INNER JOIN Ingredients AS ing
-- 	    ON ri.ingredient_id = ing.ingredient_id
-- 	    INNER JOIN Recipes AS r
-- 	    ON r.recipe_id = ri.recipe_id
--  	    INNER JOIN Genre AS g
-- 	    ON r.genre_id = g.genre_id
-- 	    INNER JOIN Food_Types AS ft
-- 	    ON r.food_type_id = ft.food_type_id
-- 	    INNER JOIN Dish_Types AS dt
-- 	    ON r.dish_type_id = dt.dish_type_id
--  	    INNER JOIN Picture AS p
-- 	    ON r.picture_id = p.picture_id
--      WHERE    ing.ingredient_id IN (42)

-- ) AS TEMP  -- OFFSET 0 LIMIT 3
-- ;

SELECT
    table1.recipe_id
    , table1.recipe_name
    , table1.ingredient_id
    , table1.recipe_ingredient_id
    , table1.rank1
    , table2.rank2
FROM (
    SELECT
        
        ri.recipe_id
        , r.recipe_name
        , ing.ingredient_name
        , ri.recipe_ingredient_id
        , ri.ingredient_id
        , rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS rank1
    
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
    
    ) AS table1
-- ;
    -- INNER JOIN table1 AS tb12
    INNER JOIN (

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

    ON table1.recipe_id = table2.recipe_id

;

    

-- INNER JOIN table1 as t1
-- ON table2 as t2
-- ON t1.recipe_id = t2.recipe_id
-- 
