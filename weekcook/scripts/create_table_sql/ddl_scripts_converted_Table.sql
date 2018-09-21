CREATE TABLE Alias_Definition(
	alias_id int4  NOT NULL,
	ingredient_id int4 NOT NULL,
	alias_name varchar NOT NULL,
	delete_flag int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL
);

CREATE TABLE Author(
	author_id int4  NOT NULL,
	author_name varchar NOT NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(author_id)
);

CREATE TABLE Back_Office_Courses_Setting(
	course_id int4 NOT NULL,
	recommend_dish_pattern int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(course_id)
);

CREATE TABLE Back_Office_One_Menu_Courses_Setting(
	one_menu_course_id int4 NOT NULL,
	recommend_dish_pattern int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_course_id)
);

CREATE TABLE Btob_Client_Contract_Courses(
	btob_client_contract_course_id int8  NOT NULL,
	btob_client_contract_id int8 NOT NULL,
	course_id int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_client_contract_course_id)
);

CREATE TABLE Btob_Client_Contract_Courses_Layout(
	btob_client_contract_course_id int8 NOT NULL,
	course_name_disp varchar NOT NULL,
	original_history_tpl_flag bit NOT NULL,
	history_lead text NULL,
	original_index_tpl_flag bit NOT NULL,
	contents_header_btn_flag bit NULL,
	top_btn_flag bit NULL,
	top_btn_text varchar NULL,
	top_btn_no int4 NULL,
	top_btn_link_url varchar NULL,
	top_btn_target_flag bit NULL,
	bottom_btn_flag bit NULL,
	bottom_btn_text varchar NULL,
	bottom_btn_no int4 NULL,
	bottom_btn_link_url varchar NULL,
	bottom_btn_target_flag bit NULL,
	transition_btn_disp_flag bit NULL,
	each_day_label_disp_type int4 NULL,
	nutrients_info_disp_type int4 NULL,
	partial_disp_flag bit NOT NULL,
	rice_quantity_cup varchar NULL,
	rice_quantity_kcal float NULL,
	original_shoppinglist_tpl_flag bit NOT NULL,
	shoppinglist_remarks_text_color varchar NULL,
	original_weekend_tpl_flag bit NOT NULL,
	weekend_remarks_text_color varchar NULL,
	original_recipe_tpl_flag bit NOT NULL,
	recipe_remarks_text_color varchar NULL,
	contents_bottom_text text NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_client_contract_course_id)
);

CREATE TABLE Btob_Client_Contracts(
	btob_client_contract_id int8  NOT NULL,
	btob_client_id int4 NOT NULL,
	contract_id int8 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_client_contract_id)
);

CREATE TABLE Btob_Client_Contracts_Layout(
	btob_client_contract_id int8 NOT NULL,
	btob_client_name_disp varchar NOT NULL,
	original_header_flag bit NOT NULL,
	header_background_color nchar(6) NULL,
	logo_alt varchar NULL,
	logo_link_url varchar NULL,
	logo_link_target_flag bit NULL,
	btn1_flag bit NULL,
	btn1_alt varchar NULL,
	btn1_url varchar NULL,
	btn1_target_flag bit NULL,
	btn2_flag bit NULL,
	btn2_alt varchar NULL,
	btn2_url varchar NULL,
	btn2_target_flag bit NULL,
	original_footer_flag bit NOT NULL,
	footer_background_color nchar(6) NULL,
	weekcook_link_flag bit NULL,
	addthis_flag bit NULL,
	addthis_id varchar NULL,
	footer_html text NULL,
	original_recipe_tpl_flag bit NOT NULL,
	btob_design_theme_id int4 NULL,
	still_disp_flag bit NOT NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_client_contract_id)
);

CREATE TABLE Btob_Clients(
	btob_client_id int4  NOT NULL,
	btob_client_name varchar NOT NULL,
	enable_flag int2 NOT NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_client_id)
);

CREATE TABLE Btob_Design_Themes(
	btob_design_theme_id int4  NOT NULL,
	btob_design_theme_name nchar(2) NOT NULL,
	btob_design_theme_description varchar NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(btob_design_theme_id)
);

CREATE TABLE contents_profile(
	contents_profile_id int4  NOT NULL,
	cp_course_id int4 NULL,
	cp_menu_tpl varchar NULL,
	cp_index_tpl varchar NOT NULL,
	cp_shopping_tpl varchar NOT NULL,
	cp_weekend_tpl varchar NOT NULL,
	cp_recipe_tpl varchar NOT NULL,
	cp_history_tpl varchar NOT NULL,
	cp_dir varchar NOT NULL,
	cp_recipe_dir varchar NOT NULL,
	cp_logic varchar NOT NULL,
	cp_day int4 NULL,
	cp_open_correct int4 NOT NULL,
	cp_is_nutrition int4 NOT NULL,
	PRIMARY KEY(contents_profile_id)
);

CREATE TABLE Contracts(
	contract_id int8  NOT NULL,
	contract_name varchar NOT NULL,
	contract varchar NOT NULL,
	contract_start_date date NOT NULL,
	contract_end_date date NOT NULL,
	contract_officer_name varchar NULL,
	contract_phone_number varchar NULL,
	note varchar NULL,
	admin_note varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(contract_id)
);

CREATE TABLE Cook_Ahead(
	cook_ahead_id int2  NOT NULL,
	cook_ahead varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(cook_ahead_id)
);

CREATE TABLE Cooking_Method(
	cooking_method_id int4  NOT NULL,
	cooking_method_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(cooking_method_id)
);

CREATE TABLE Cooking_Procedure_Parameter(
	directions_detail_id int8 NOT NULL,
	number_of_people_id int2 NOT NULL,
	param_index int4 NOT NULL,
	param_type int4 NOT NULL,
	ingredient_id int4 NULL,
	quantity int4 NULL,
	quantity_id int4 NULL,
	quantity_numerator int2 NULL,
	quantity_denominator int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(directions_detail_id, number_of_people_id, param_index)
);

CREATE TABLE Courses(
	course_id int4  NOT NULL,
	course_name varchar NOT NULL,
	course_short_name varchar NULL,
	number_of_people_id int2 NOT NULL,
	directions_detail_pattern int2 NOT NULL,
	consider_pre_cooking int2 NOT NULL,
	days int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(course_id)
);

CREATE TABLE Courses_Author(
	course_id int4 NOT NULL,
	author_id int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(course_id, author_id)
);

CREATE TABLE Courses_Dish_Types(
	course_id int4 NOT NULL,
	dish_type_id int2 NOT NULL,
	limit_number_of_days int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(course_id, dish_type_id)
);

CREATE TABLE Cutting_Types(
	cutting_types_id int4  NOT NULL,
	ingredient_id int4 NOT NULL,
	cutting_name varchar NULL,
	cooking_time int4 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(cutting_types_id)
);

CREATE TABLE Defrosting_Methods(
	defrosting_methods_id int2  NOT NULL,
	defrosting_methods varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(defrosting_methods_id)
);

CREATE TABLE Directions_Detail(
	directions_detail_id int8  NOT NULL,
	recipe_id int8 NOT NULL,
	cooking_procedure varchar NOT NULL,
	holiday_flag int2 NOT NULL,
	classification_id int4 NOT NULL,
	cutting_types_id int4 NULL,
	meat_used_flag int2 NOT NULL,
	intermediate_id int8 NULL,
	repair_flag int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(directions_detail_id)
);

CREATE TABLE Directions_Detail_Number_Of_People(
	directions_detail_id int8 NOT NULL,
	number_of_people_id int2 NOT NULL,
	cooking_time int4 NOT NULL,
	defrosting_methods_id int2 NULL,
	description varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	person_exclusive_use_flag int2 NOT NULL,
	PRIMARY KEY(directions_detail_id, number_of_people_id)
);

CREATE TABLE Directions_Detail_Pattern(
	directions_detail_pattern_id int8  NOT NULL,
	pattern int2 NOT NULL,
	directions_detail_id int8 NOT NULL,
	sequence_no int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(directions_detail_pattern_id)
);

CREATE TABLE Directions_Detail_Picture(
	directions_detail_id int8 NOT NULL,
	picture_id int8 NOT NULL,
	order_number int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(directions_detail_id, picture_id)
);

CREATE TABLE Directions_Previous_Process(
	directions_detail_pattern_id int8 NOT NULL,
	previous_process int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	previous_dependence_level int4 NOT NULL,
	PRIMARY KEY(directions_detail_pattern_id, previous_process)
);

CREATE TABLE Dish_Types(
	dish_type_id int2  NOT NULL,
	dish_type_name varchar NOT NULL,
	dish_type_alias varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(dish_type_id)
);

CREATE TABLE Finish_Method_On_Weekdays(
	finish_method_on_weekdays_id int4  NOT NULL,
	finish_method_on_weekdays varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(finish_method_on_weekdays_id)
);

CREATE TABLE Food_Types(
	food_type_id int4  NOT NULL,
	food_type_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(food_type_id)
);

CREATE TABLE Genre(
	genre_id int4  NOT NULL,
	genre_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(genre_id)
);

CREATE TABLE Ingredient_Classification(
	ingredient_classification_id int4  NOT NULL,
	large_classification_id int2 NOT NULL,
	small_classification varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(ingredient_classification_id)
);

CREATE TABLE Ingredient_Priority(
	ingredient_id int4 NOT NULL,
	priority int2 NOT NULL,
	delete_flag int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL
);

CREATE TABLE Ingredient_Season(
	ingredient_season_id int4  NOT NULL,
	ingredient_id int4 NOT NULL,
	season_start int2 NULL,
	season_end int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(ingredient_season_id)
);

CREATE TABLE Ingredient_Substitutions(
	ingredient_substitutions_id int4  NOT NULL,
	ingredient_id int4 NOT NULL,
	substitute_id int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(ingredient_substitutions_id)
);

CREATE TABLE Ingredient_Types(
	ingredient_type_id int2  NOT NULL,
	ingredient_type_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(ingredient_type_id)
);

CREATE TABLE Ingredient_Unit(
	ingredient_unit_id int4  NOT NULL,
	ingredient_id int4 NOT NULL,
	quantity_id int4 NOT NULL,
	standart_quantity int4 NULL,
	price varchar NULL,
	full_of_use_quantity int2 NULL,
	full_of_use_quantity_numerator int2 NULL,
	full_of_use_quantity_denominator int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(ingredient_unit_id)
);

CREATE TABLE Ingredients(
	ingredient_id int4  NOT NULL,
	ingredient_name varchar NOT NULL,
	ingredient_kana varchar NOT NULL,
	ingredient_classification_id int4 NOT NULL,
	ingredient_type_id int2 NOT NULL,
	recipe_id int8 NULL,
	sweetness_flag int2 NOT NULL,
	sourness_flag int2 NOT NULL,
	saltiness_flag int2 NOT NULL,
	bitterness_flag int2 NOT NULL,
	umami_flag int2 NOT NULL,
	spicy_flag int2 NOT NULL,
	strong_taste_flag int2 NOT NULL,
	deleted_at timestamp NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	admin_note varchar NULL,
	fridge_shelf_life_id int2 NULL,
	freezer_shelf_life_id int2 NULL,
	PRIMARY KEY(ingredient_id)
);

CREATE TABLE Intermediate(
	intermediate_id int8  NOT NULL,
	intermediate_name varchar NOT NULL,
	picture_id int8 NULL,
	fridge_shelf_life_id int2 NULL,
	freezer_shelf_life_id int2 NULL,
	partial_shelf_life_id int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(intermediate_id)
);

CREATE TABLE Large_Classification(
	large_classification_id int2  NOT NULL,
	large_classification varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(large_classification_id)
);

CREATE TABLE Marks(
	mark_id int2  NOT NULL,
	mark_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(mark_id)
);

CREATE TABLE Multiday_Menu(
	multiday_menu_id int8  NOT NULL,
	menu_composed_one_menu_ids varchar(900) NULL UNIQUE,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(multiday_menu_id)
);

CREATE TABLE Multiday_Menu_List(
	multiday_menu_list_id int8  NOT NULL,
	multiday_menu_id int8 NOT NULL,
	one_menu_id int8 NOT NULL,
	cooking_day int4 NOT NULL,
	cooking_time_zone_id int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(multiday_menu_list_id)
);

CREATE TABLE Number_Of_People(
	number_of_people_id int2  NOT NULL,
	number_of_people decimal(3, 1) NOT NULL UNIQUE,
	notation varchar NOT NULL,
	stove int2 NULL,
	microwave int2 NULL,
	grill int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(number_of_people_id)
);

CREATE TABLE Occupation_Matrix(
	occupation_matrix_id int2  NOT NULL,
	classification_id int4 NOT NULL,
	resource_id int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(occupation_matrix_id)
);

CREATE TABLE One_Menu(
	one_menu_id int8  NOT NULL,
	menu_composed_of_recipe_ids varchar(1000) NOT NULL UNIQUE,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_id)
);

CREATE TABLE One_Menu_Courses(
	one_menu_course_id int4  NOT NULL,
	course_name varchar NOT NULL,
	course_short_name varchar NULL,
	number_of_people_id int2 NOT NULL,
	directions_detail_pattern int2 NOT NULL,
	consider_pre_cooking int2 NOT NULL,
	days int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_course_id)
);

CREATE TABLE One_Menu_Courses_Author(
	one_menu_course_id int4 NOT NULL,
	author_id int4 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_course_id, author_id)
);

CREATE TABLE One_Menu_Courses_Dish_Types(
	one_menu_course_id int4 NOT NULL,
	dish_type_id int2 NOT NULL,
	limit_number_of_days int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_course_id, dish_type_id)
);

CREATE TABLE One_Menu_Meal(
	one_menu_meal_id int8  NOT NULL,
	one_menu_course_id int4 NOT NULL,
	one_menu_id int8 NOT NULL,
	title varchar NULL,
	main_theme varchar NULL,
	sub_theme varchar NULL,
	release_date date NULL,
	release_status int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	admin_note varchar NULL,
	shoppinglist_remarks varchar NULL,
	precooking_remarks varchar NULL,
	cooking_remarks varchar NULL,
	one_day_schedule_algorithm int2 NULL,
	pre_cooking_schedule_algorithm int2 NULL,
	cooking_schedule_algorithm int2 NULL,
	PRIMARY KEY(one_menu_meal_id)
);

CREATE TABLE One_Menu_Recipe_List(
	one_menu_recipe_list_id int8  NOT NULL,
	one_menu_id int8 NOT NULL,
	recipe_id int8 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(one_menu_recipe_list_id)
);

CREATE TABLE Picture(
	picture_id int8  NOT NULL,
	picture_type_id int2 NOT NULL,
	picture_name varchar NULL,
	file_name varchar NULL,
	keywords varchar NULL,
	description varchar NULL,
	deleted_at timestamp NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	author_id int4 NULL,
	PRIMARY KEY(picture_id)
);

CREATE TABLE Picture_Type(
	picture_type_id int2  NOT NULL,
	picture_type_name varchar(100) NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(picture_type_id)
);

CREATE TABLE Process_Classification(
	classification_id int4  NOT NULL,
	classification_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(classification_id)
);

CREATE TABLE Quantity_Range(
	recipe_ingredient_id int8 NOT NULL,
	number_of_people_id int2 NOT NULL,
	quantity_id int4 NOT NULL,
	max_quantity int4 NULL,
	min_quantity int4 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(recipe_ingredient_id, number_of_people_id)
);

CREATE TABLE Quantity_Unit(
	quantity_id int4  NOT NULL,
	quantity_name varchar NOT NULL,
	quantity_type int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(quantity_id)
);

CREATE TABLE Rcmd_Recipe_List(
	rcmd_recipe_list_id int4  NOT NULL,
	recipe_id int8 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(rcmd_recipe_list_id)
);

CREATE TABLE Recipe_Ingredients(
	recipe_ingredient_id int8  NOT NULL,
	recipe_id int8 NOT NULL,
	ingredient_id int4 NOT NULL,
	holiday_flag int2 NOT NULL,
	mark_id int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(recipe_ingredient_id)
);

CREATE TABLE Recipe_Ingredients_Number_Of_People(
	recipe_ingredient_id int8 NOT NULL,
	number_of_people_id int2 NOT NULL,
	quantity_id int4 NOT NULL,
	quantity int4 NULL,
	quantity_numerator int2 NULL,
	quantity_denominator int2 NULL,
	description varchar NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(recipe_ingredient_id, number_of_people_id)
);

CREATE TABLE Recipe_Nutrition(
	recipe_nutrition_id int8  NOT NULL,
	recipe_id int8 NOT NULL,
	kcal float NOT NULL,
	protein float NOT NULL,
	lipid float NOT NULL,
	saturated_fatty_acid float NOT NULL,
	monounsaturated_fatty_acid float NOT NULL,
	polyunsaturated_fatty_acid float NOT NULL,
	n6_fatty_acid float NOT NULL,
	n3_fatty_acid float NOT NULL,
	cholesterol float NOT NULL,
	carbohydrate float NOT NULL,
	dietary_fiber float NOT NULL,
	soluble_dietary_fiber float NOT NULL,
	insoluble_dietary_fiber float NOT NULL,
	sodium float NOT NULL,
	potassium float NOT NULL,
	calcium float NOT NULL,
	magnesium float NOT NULL,
	phosphorus float NOT NULL,
	iron float NOT NULL,
	zinc float NOT NULL,
	copper float NOT NULL,
	manganese float NOT NULL,
	iodine float NOT NULL,
	selenium float NOT NULL,
	chromium float NOT NULL,
	molybdenum float NOT NULL,
	vitamine_a float NOT NULL,
	vitamine_d float NOT NULL,
	vitamine_e float NOT NULL,
	vitamine_k float NOT NULL,
	vitamine_b1 float NOT NULL,
	vitamine_b2 float NOT NULL,
	niacin float NOT NULL,
	vitamine_b6 float NOT NULL,
	vitamine_b12 float NOT NULL,
	folic_acid float NOT NULL,
	pantothenic_acid float NOT NULL,
	biotin float NOT NULL,
	vitamine_c float NOT NULL,
	salt float NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(recipe_nutrition_id)
);

CREATE TABLE Recipe_Priority(
	recipe_id int8 NOT NULL,
	priority int2 NOT NULL,
	delete_flag int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL
);

CREATE TABLE Recipe_Season(
	recipe_season_id int8  NOT NULL,
	recipe_id int8 NOT NULL,
	season_start int2 NULL,
	season_end int2 NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(recipe_season_id)
);

CREATE TABLE Recipes(
	recipe_id int8  NOT NULL,
	original_recipe_id int8 NULL,
	copy_type int4 NOT NULL,
	recipe_name varchar NOT NULL,
	recipe_name_kana varchar NOT NULL,
	genre_id int4 NOT NULL,
	dish_type_id int2 NOT NULL,
	food_type_id int4 NOT NULL,
	cook_ahead_id int2 NOT NULL,
	finish_method_on_weekdays_id int4 NULL,
	picture_id int8 NOT NULL,
	cooking_time int2 NOT NULL,
	author_id int4 NULL,
	cooking_method_id int4 NULL,
	description varchar NULL,
	introductory_essay varchar NULL,
	ingredient_id int4 NULL,
	out_of_season_flag int2 NOT NULL,
	url varchar NULL,
	search_word varchar NOT NULL,
	default_number_of_people_id int2 NULL,
	release_status int2 NULL,
	release_date date NULL,
	deleted_at timestamp NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	admin_note varchar NULL,
	PRIMARY KEY(recipe_id)
);

CREATE TABLE Resource(
	resource_id int2  NOT NULL,
	resource_name varchar NOT NULL,
	type varchar NOT NULL,
	offset_time int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(resource_id)
);

CREATE TABLE Rice_Nutrition(
	rice_nutrition_id int8  NOT NULL,
	course_id int4 NOT NULL,
	kcal float NULL,
	protein float NULL,
	lipid float NULL,
	carbohydrate float NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(rice_nutrition_id)
);

CREATE TABLE Role_Detail(
	role_id int4 NOT NULL,
	function_id varchar(100) NOT NULL,
	enable_flag int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(role_id, function_id)
);

CREATE TABLE Roles(
	role_id int4  NOT NULL,
	role_name varchar NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(role_id)
);

CREATE TABLE Schedules(
	schedule_id int8  NOT NULL,
	menu_id int8 NOT NULL,
	history_no int4 NOT NULL,
	cooking_date int2 NOT NULL,
	recipe_id int8 NOT NULL,
	directions_detail_id int8 NOT NULL,
	sequence_no int4 NOT NULL,
	directions_detail varchar NULL,
	cooking_order int2 NOT NULL,
	start_of_cooking_time real NOT NULL,
	end_of_cooking_time real NOT NULL,
	indent_no int2 NOT NULL,
	start_pararell_flag int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(schedule_id)
);

CREATE TABLE Shelf_Life(
	shelf_life_id int2  NOT NULL,
	shelf_life varchar NOT NULL,
	days int2 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(shelf_life_id)
);

CREATE TABLE Users(
	id int8  NOT NULL,
	name varchar NOT NULL,
	email varchar(255) NOT NULL,
	password varchar(60) NOT NULL,
	remember_token varchar(100) NULL,
	admin_flag int2 NOT NULL,
	role_id int4 NULL,
	deleted_at timestamp NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(id)
);

CREATE TABLE Weekly_Meal(
	menu_id int8  NOT NULL,
	multiday_menu_id int8 NULL,
	used_week date NULL,
	title varchar NULL,
	main_theme varchar NULL,
	sub_theme varchar NULL,
	note varchar NULL,
	admin_note varchar NULL,
	course_id int4 NULL,
	mon_main_recipe_id int8 NULL,
	mon_main2_recipe_id int8 NULL,
	mon_side1_recipe_id int8 NULL,
	mon_side2_recipe_id int8 NULL,
	mon_soup_recipe_id int8 NULL,
	mon_dessert_recipe_id int8 NULL,
	tue_main_recipe_id int8 NULL,
	tue_main2_recipe_id int8 NULL,
	tue_side1_recipe_id int8 NULL,
	tue_side2_recipe_id int8 NULL,
	tue_soup_recipe_id int8 NULL,
	tue_dessert_recipe_id int8 NULL,
	wed_main_recipe_id int8 NULL,
	wed_main2_recipe_id int8 NULL,
	wed_side1_recipe_id int8 NULL,
	wed_side2_recipe_id int8 NULL,
	wed_soup_recipe_id int8 NULL,
	wed_dessert_recipe_id int8 NULL,
	thu_main_recipe_id int8 NULL,
	thu_main2_recipe_id int8 NULL,
	thu_side1_recipe_id int8 NULL,
	thu_side2_recipe_id int8 NULL,
	thu_soup_recipe_id int8 NULL,
	thu_dessert_recipe_id int8 NULL,
	fri_main_recipe_id int8 NULL,
	fri_main2_recipe_id int8 NULL,
	fri_side1_recipe_id int8 NULL,
	fri_side2_recipe_id int8 NULL,
	fri_soup_recipe_id int8 NULL,
	fri_dessert_recipe_id int8 NULL,
	sat_main_recipe_id int8 NULL,
	sat_main2_recipe_id int8 NULL,
	sat_side1_recipe_id int8 NULL,
	sat_side2_recipe_id int8 NULL,
	sat_soup_recipe_id int8 NULL,
	sat_dessert_recipe_id int8 NULL,
	sun_main_recipe_id int8 NULL,
	sun_main2_recipe_id int8 NULL,
	sun_side1_recipe_id int8 NULL,
	sun_side2_recipe_id int8 NULL,
	sun_soup_recipe_id int8 NULL,
	sun_dessert_recipe_id int8 NULL,
	release_status int2 NULL,
	release_date date NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	shoppinglist_remarks varchar NULL,
	precooking_remarks varchar NULL,
	cooking_remarks varchar NULL,
	one_day_schedule_algorithm int2 NULL,
	pre_cooking_schedule_algorithm int2 NULL,
	cooking_schedule_algorithm int2 NULL,
	PRIMARY KEY(menu_id)
);

CREATE TABLE Wsp_Recipe_Search_Exclusions(
	wsp_recipe_search_exclusions_id int4  NOT NULL,
	recipe_id int8 NOT NULL,
	created_id int8 NULL,
	created_at timestamp NULL,
	updated_id int8 NULL,
	updated_at timestamp NULL,
	PRIMARY KEY(wsp_recipe_search_exclusions_id)
);
