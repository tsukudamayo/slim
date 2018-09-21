-- select
-- 	*
-- FROM (
-- 	list1 AS sql1
-- 	INNER JOIN list2 AS sql2
-- 	ON sql1.recipe_id = sql2.recipe_id

-- SELECT
-- 	temp.ingredient_name
-- 	, ARRAY_AGG(temp.ingredient_id) AS ing_agg
-- 	-- *

-- FROM (

SELECT DISTINCT
	temp.recipe_id
	, temp.recipe_name
	, temp.recipe_name_kana
	, temp.introductory_essay
	, temp.dish_type_name
	, temp.genre_name
	, temp.food_type_name
	, temp.file_name
	-- , temp.ranking
	, temp.ingredient_name
	, temp.ingredient_id
	-- , ARRAY_AGG(temp.recipe_name) AS uni
FROM (

     SELECT
     	html1.recipe_id
     	, html1.recipe_name
     	, html1.recipe_name_kana
     	, html1.introductory_essay
     	, html1.dish_type_name
     	, html1.genre_name
     	, html1.food_type_name
     	, html1.file_name
     	-- , html1.ranking
     	, html1.ingredient_name
     	, html1.ingredient_id
     FROM (
     	  SELECT DISTINCT
     	  o.recipe_id
     	  , o.recipe_name
     	  , o.recipe_name_kana
     	  , o.introductory_essay
     	  , o.dish_type_name
     	  , o.genre_name
     	  , o.food_type_name
     	  , o.file_name
     	  , o.ingredient_name
     	  -- , o.ranking AS ranking
     	  , o.ingredient_id
     	  FROM (
     	       SELECT
     	       ri.recipe_id
     	       , r.recipe_name
     	       , r.recipe_name_kana
     	       , r.introductory_essay
     	       , dt.dish_type_name
     	       , g.genre_name
     	       , ft.food_type_name
     	       , p.file_name
     	       , ing.ingredient_name
     	       , ri.recipe_ingredient_id
     	       , ri.ingredient_id
     	       -- , rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS ranking
     	       FROM
     			recipe_ingredients AS ri
     			INNER JOIN ingredients AS ing
     			ON ri.ingredient_id = ing.ingredient_id
     			INNER JOIN recipes AS r
     			ON r.recipe_id = ri.recipe_id
     			INNER JOIN genre AS g
     			ON r.genre_id = g.genre_id
     			INNER JOIN food_types AS ft
     			ON r.food_type_id = ft.food_type_id
     			INNER JOIN dish_types AS dt
     			ON r.dish_type_id = dt.dish_type_id
     			INNER JOIN picture AS p ON r.picture_id = p.picture_id			) AS o
     		WHERE
     			o.ingredient_id IN (36)
     		-- ORDER BY
     		-- 	o.ranking
		ORDER BY
			o.recipe_id
     	 ) AS html1



     -- ) AS list1
     
INTERSECT
-- UNION ALL
-- INNER JOIN

	SELECT
	  html2.recipe_id
	  , html2.recipe_name
	  , html2.recipe_name_kana
	  , html2.introductory_essay
	  , html2.dish_type_name
	  , html2.genre_name
	  , html2.food_type_name
	  , html2.file_name
	  -- , html2.ranking
	  , html2.ingredient_name
	  , html2.ingredient_id
	  FROM (
 	       SELECT DISTINCT
 	       o.recipe_id
	       , o.recipe_name
 	       , o.recipe_name_kana
 	       , o.introductory_essay
 	       , o.dish_type_name
 	       , o.genre_name
 	       , o.food_type_name
 	       , o.file_name
 	       , o.ingredient_name
 	       -- , o.ranking AS ranking
	       , o.ingredient_id
	       FROM (
 	       	    SELECT
		    ri.recipe_id
		    , r.recipe_name
		    , r.recipe_name_kana
 		    , r.introductory_essay
		    , dt.dish_type_name
		    , g.genre_name
		    , ft.food_type_name
		    , p.file_name
		    , ing.ingredient_name
		    , ri.recipe_ingredient_id
		    , ri.ingredient_id
		    -- , rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS ranking
 		    FROM 
			recipe_ingredients AS ri
			INNER JOIN ingredients AS ing
			ON ri.ingredient_id = ing.ingredient_id
			INNER JOIN recipes AS r
			ON r.recipe_id = ri.recipe_id
			INNER JOIN genre AS g
			ON r.genre_id = g.genre_id
			INNER JOIN food_types AS ft
			ON r.food_type_id = ft.food_type_id
			INNER JOIN dish_types AS dt
 			ON r.dish_type_id = dt.dish_type_id
			INNER JOIN picture AS p ON r.picture_id = p.picture_id			) AS o
		WHERE
			o.ingredient_id IN (42)
 		-- ORDER BY
 		--         o.ranking
		ORDER BY
			o.recipe_id
 	) AS html2
	
-- ) AS list2



) AS temp -- OFFSET 0 LIMIT 3
-- WHERE temp.ingredient_id IN (36, 42)

-- GROUP BY
--       temp.recipe_id
--       , temp.recipe_name
--       , temp.recipe_name_kana
--       , temp.introductory_essay
--       , temp.dish_type_name
--       , temp.genre_name
--       , temp.food_type_name
--       , temp.file_name
--       , temp.ranking
--       , temp.ingredient_name
--       , temp.ingredient_id
--       HAVING COUNT(temp.recipe_id) = 2

-- ORDER BY temp.recipe_id    


;
