SELECT DISTINCT
       ri.recipe_id
       , r.recipe_name
       , r.recipe_name_kana
       , r.introductory_essay
       , dt.dish_type_name
       , g.genre_name
       , ft.food_type_name
       , p.file_name
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

WHERE
	ing.ingredient_id IN (42)

ORDER BY
	ri.recipe_id;
