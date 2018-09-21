SELECT
	html.recipe_id
	, html.recipe_name
	, html.recipe_name_kana
	, html.introductory_essay
	, html.dish_type_name
	, html.genre_name
	, html.food_type_name
	, html.file_name

FROM
(
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
	       , o.ranking
	       , o.ingredient_id
	       
	       FROM
	       (
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
				, rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS ranking
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
			
				INNER JOIN picture AS p ON r.picture_id = p.picture_id
	
		) AS o
	
	WHERE
		o.ingredient_id IN (42, 36)
	
	ORDER BY
		o.ranking
		
	) AS html

;








