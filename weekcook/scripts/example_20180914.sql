SELECT
	o.recipe_id
	, o.ingredient_name
	, o.recipe_ingredient_id
	, rank() OVER (PARTITION BY o.recipe_id ORDER BY o.recipe_ingredient_id) AS seq
	
	FROM
	(
		SELECT
			r.recipe_id
			, ing.ingredient_name
			, ri.recipe_ingredient_id
		FROM 
	
			recipe_ingredients AS ri
			
			INNER JOIN ingredients AS ing
			ON ri.ingredient_id = ing.ingredient_id
			
			INNER JOIN recipes AS r
			ON ri.recipe_id = r.recipe_id
	) as o

LIMIT
	100;
