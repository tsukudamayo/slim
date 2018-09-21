// (cf.) https://node-postgres.com
// (cf.) https://node-postgres.com/features/connecting

//const { Pool, Client } = require('pg');
const { Client } = require('pg');
//const connectionString = 'postgresql://postgres:admin@localhost:5432/postgres'
//const connectionString = 'postgresql://postgres:admin@localhost:5432/postgres?encoding=UTF8'

var queryKey1 = 'ingredient_name1';
var queryKey2 = 'ingredient_name2';

var sqlKey_recipe_name = 'recipe_name';
var sqlKey_introductory_essay = 'introductory_essay';
var sqlKey_dish_type_name = 'dish_type_name';
var sqlKey_genre_name = 'genre_name';
var sqlKey_food_type_name = 'food_type_name';
var sqlKey_file_name = 'file_name';

var dbClientSetting = {
    //connectionString: connectionString,
    //
    user: 'postgres',
    password: 'postgres',
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    client_encoding: 'utf8'
};

module.exports = class ApiMethodController {
    constructor() {
    }

    // GET update_recipe
    update_recipe(request, response, queryMap) {
        console.log('update_recipe()');

        var dbClient = new Client(dbClientSetting);

        dbClient.connect();

        console.log('passed dbClient.connect()');
        //console.log(queryMap[queryKey1]);

        var sql = this.construct_recipe_query(queryMap);
        var response_html = '';

        // query は非同期に実行される
        dbClient.query(sql, (err, res) => {
            console.log('passed dbClient.query()');
            if (res) {
                console.log(res.rows.length);
                if (res.rows.length > 0) {
                    response_html = this.construct_html(res.rows);
                    if (response_html != '') {
                        response.write(response_html);
                        console.log(response_html);
                    }
                }
            } else {
                console.log('query is wrong. sql: ' + sql);
            }
            dbClient.end();
            response.end();
        });
    }

    construct_recipe_query(queryMap) {
        var sql =
		"SELECT DISTINCT " +
		"	ri.recipe_id, " +
		//"	ing.ingredient_id, " +
		//"	ing.ingredient_name, " +
		//"	ing.ingredient_kana, " +
		"	r.recipe_name, " +
		"	r.recipe_name_kana, " +
		"	r.introductory_essay, " +
		"	dt.dish_type_name, " +
		"	g.genre_name, " +
		"	ft.food_type_name, " +
		"	p.file_name " +
		"FROM Recipe_Ingredients AS ri " +
		"	INNER JOIN Ingredients AS ing ON ri.ingredient_id = ing.ingredient_id " +
                "	INNER JOIN Ingredient_name_map AS nmap ON ri.ingredient_id = nmap.ingredient_id " +
		"	INNER JOIN Recipes AS r ON r.recipe_id = ri.recipe_id " +
		"	INNER JOIN Genre AS g ON r.genre_id = g.genre_id " +
		"	INNER JOIN Food_Types AS ft ON r.food_type_id = ft.food_type_id " +
		"	INNER JOIN Dish_Types AS dt ON r.dish_type_id = dt.dish_type_id " +
		"	INNER JOIN Picture AS p ON r.picture_id = p.picture_id " +
		"WHERE " +
		"	nmap.search_key = '" + queryMap[queryKey1] + "';";

        console.log(sql);

        return sql;
    }

    // GET get_ingredient_list
    get_ingredient_list(request, response) {
        console.log('get_ingredient_list()');

        // 指定キーに一致する項目一覧
        var sql = this.construct_ingredients_query();

        var response_html = '';

        client.query(sql, (err, res) => {
            if (res) {
                response_html = this.construct_html(res.rows);
                if (response_html != '') {
                    response.write(response_html);
                }
            } else {
                console.log('query is wrong. sql: ' + sql);
            }
            client.end();
            response.end();
        });
    }

    construct_ingredients_query() {
        var sql = "SELECT * FROM Ingredient_name_map;"
        return sql;
    }

    // TODO: テスト > 画像のダウンロード
    // TODO: テスト > 

    // TODO: 実装
    construct_html(res_rows) {
        console.log('construct_html()');

        if (res_rows.length == 0) {
            return '';
        }

        // クライアントアプリ
        var html_body = '';
        for (var i = 0; i < res_rows.length; ++i) {
            var row = res_rows[i];

            var recipe_name = row[sqlKey_recipe_name];
            var introductory_essay = row[sqlKey_introductory_essay];
            var dish_type_name = row[sqlKey_dish_type_name];
            var genre_name = row[sqlKey_genre_name];
            var food_type_name = row[sqlKey_food_type_name];
            var file_name = row[sqlKey_file_name];

            //
            if (i == 0) {
                console.log(row);
            }
        }

        // テスト
        html_body = 'テスト ﾃｽﾄ';

        //console.log(res);
        //console.log(res.rows);
        //console.log(res.rowCount);
        //
        //console.log(res.rows[0]);
        //var recipe_name = res.rows[0]['recipe_name'];
        //console.log(recipe_name);
        //
        // res.rows is array of maps.
        //console.log(res.rows);
        //console.log(typeof res.rows);
        //console.log(res.rows[0]);
        //console.log(res.rows[0]['count']); // 821

        var html_format = "<!DOCTYPE><html><head><meta charset='UTF-8'></head><body>{0}</body></html>";
        
        var html = html_format.replace("{0}", html_body);

        return html;
    }
}
