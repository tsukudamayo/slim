CREATE VIEW wsp_recipeSearchView
	AS select E.recipe_id,E.original_recipe_id,E.recipe_name ,E.recipe_name_kana ,e.dish_type_id,e.picture_id,
	(select b.ingredient_name || ' ' || b.ingredient_kana || ' '
			 from Recipe_Ingredients as a inner join Ingredients as b on a.ingredient_id = b.ingredient_id 
				 where a.recipe_id = E.recipe_id) as ings
	from Recipes as E;

CREATE VIEW wsp_recipeSearchViewBase
	AS select E.recipe_id,(select b.ingredient_name || ' ' || b.ingredient_kana || ' '
			 from Recipe_Ingredients as a inner join Ingredients as b on a.ingredient_id = b.ingredient_id 
				 where a.recipe_id = E.recipe_id) as ings
	from Recipes as E;
