// (cf.) https://node-postgres.com
// (cf.) https://node-postgres.com/features/connecting

//const { Pool, Client } = require('pg');
const { Client } = require('pg');
//const connectionString = 'postgresql://postgres:admin@localhost:5432/postgres'
//const connectionString = 'postgresql://postgres:admin@localhost:5432/postgres?encoding=UTF8'
const fs = require('fs');

var sqlKey_recipe_name = 'recipe_name';
var sqlKey_introductory_essay = 'introductory_essay';
var sqlKey_dish_type_name = 'dish_type_name';
var sqlKey_genre_name = 'genre_name';
var sqlKey_food_type_name = 'food_type_name';
var sqlKey_file_name = 'file_name';

/*
var dbClientSetting = {
    connectionString: connectionString
};
*/

var dbClientSetting = {
    user: 'postgres',
    password: 'postgres',
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    client_encoding: 'utf8'
};

module.exports = class ApiMethodController {
    constructor(serverPushSetting, queryKeys) {
        this.serverPushSetting = serverPushSetting;
        this.queryKeys = queryKeys;
        this.single_sql_format =
	    
// "SELECT " +
// "	html.recipe_id " +
// "	, html.recipe_name " +
// "	, html.recipe_name_kana " +
// "	, html.introductory_essay " +
// "	, html.dish_type_name " +
// "	, html.genre_name " +
// "	, html.food_type_name " +
// "	, html.file_name " +
// "	, html.ranking " +
// "FROM " +
// "( " +
// "	SELECT DISTINCT " +
// "	       o.recipe_id " +
// "	       , o.recipe_name " +
// "	       , o.recipe_name_kana " +
// "	       , o.introductory_essay " +
// "	       , o.dish_type_name " +
// "	       , o.genre_name " +
// "	       , o.food_type_name " +
// "	       , o.file_name " +
// "	       , o.ingredient_name " +
// "	       , o.ranking AS ranking" +
// "	       , o.ingredient_id" +
// "	       FROM " +
// "	       ( " +
// "			SELECT " +
// "				ri.recipe_id " +
// "				, r.recipe_name " +
// "				, r.recipe_name_kana " +
// "				, r.introductory_essay " +
// "				, dt.dish_type_name " +
// "				, g.genre_name " +
// "				, ft.food_type_name " +
// "				, p.file_name " +
// "				, ing.ingredient_name " +
// "				, ri.recipe_ingredient_id " +
// "				, ri.ingredient_id " +
// "				, rank() OVER (PARTITION BY ri.recipe_id ORDER BY ri.recipe_ingredient_id) AS ranking " +
// "			FROM " +
// "				recipe_ingredients AS ri " +
// "				INNER JOIN ingredients AS ing " +
// "				ON ri.ingredient_id = ing.ingredient_id " +
// "				INNER JOIN recipes AS r " +
// "				ON r.recipe_id = ri.recipe_id " +
// "				INNER JOIN genre AS g " +
// "				ON r.genre_id = g.genre_id " +
// "				INNER JOIN food_types AS ft " +
// "				ON r.food_type_id = ft.food_type_id " +
// "				INNER JOIN dish_types AS dt " +
// "				ON r.dish_type_id = dt.dish_type_id " +
// "				INNER JOIN picture AS p ON r.picture_id = p.picture_id " +
// "		) AS o " +
// "	WHERE " +
// "		o.ingredient_id IN ({ingredient_csv}) " +
// "	ORDER BY " +
// 	    "		o.ranking " +
// "	) AS html ";

	    
            "SELECT DISTINCT " +
            "	ri.recipe_id, " +
            "	r.recipe_name, " +
            "	r.recipe_name_kana, " +
            "	r.introductory_essay, " +
            "	dt.dish_type_name, " +
            "	g.genre_name, " +
            "	ft.food_type_name, " +
            "	p.file_name " +
            "FROM Recipe_Ingredients AS ri " +
            "	INNER JOIN Ingredients AS ing ON ri.ingredient_id = ing.ingredient_id " +
            "	INNER JOIN Recipes AS r ON r.recipe_id = ri.recipe_id " +
            "	INNER JOIN Genre AS g ON r.genre_id = g.genre_id " +
            "	INNER JOIN Food_Types AS ft ON r.food_type_id = ft.food_type_id " +
            "	INNER JOIN Dish_Types AS dt ON r.dish_type_id = dt.dish_type_id " +
            "	INNER JOIN Picture AS p ON r.picture_id = p.picture_id " +
            "WHERE " +
            "   ing.ingredient_id IN ({ingredient_csv})";
    }

    // GET update_recipe
    update_recipe(request, response, queryMap, ws_connection) {
        console.log('update_recipe()');

        var dbClient = new Client(dbClientSetting);
        var per_page = this.serverPushSetting.showItemsPerPage;
        var page_index = queryMap[this.queryKeys.page];
        if (!page_index) {
            page_index = 0;
        }

        console.log('per_page: ' + per_page + ', page_index: ' + page_index);

        dbClient.connect();

        console.log('passed dbClient.connect()');
        console.log(queryMap);

        var sql_count = this.construct_recipe_count_query(queryMap);
        // query は非同期に実行される
        dbClient.query(sql_count, (err, res) => {
            console.log('#1 passed count query.');

            if (!res) {
                console.log('count query is wrong. sql_count: ' + sql_count);
                dbClient.end();
                response.end();
                return;
            }

            var count_records = 0;
            if (res.rows.length > 0) {
                count_records = res.rows[0]['count'];
                console.log('count_records: ' + count_records);
            } else {
                console.log('count_records is 0 ("query_result is empty" or "query_count is 0").');
                dbClient.end();
                response.end();
                return;
            }

            // ページ指定でのクエリー (先頭ページを取得)
            var sql = this.construct_recipe_query(queryMap, count_records, per_page, page_index);
	    fs.writeFileSync('output.sql', sql)
            dbClient.query(sql, (err2, res2) => {
                console.log('#2 passed contents query.');

                if (!res2) {
                    console.log('query is wrong. sql: ' + sql);
                    dbClient.end();
                    response.end();
                    return;
                }

                console.log(res2.rows.length);
                if (res2.rows.length == 0) {
                    dbClient.end();
                    response.end();
                    return;
                }

                console.log('#3 pre construct_push_html().');

                var response_html = this.construct_push_html(res2.rows, queryMap, count_records, per_page, page_index);
                if (response_html != '') {
                    response.write(response_html);
                    console.log(response_html);

                    if (ws_connection) {
                        //ws_connection.send('_PUSH_ FROM server.');
                        ws_connection.send(response_html);
                    }
                }
                dbClient.end();
                response.end();
            });
        });
    }

    // 食材が1つの場合
    // 食材が2つの場合
    construct_recipe_query(queryMap, total_count, per_page, page_index) {
        var sql = '';

        var offset = per_page * page_index;
        var csv_count = this.get_ingredient_csv_count(queryMap[this.queryKeys.ids1], queryMap[this.queryKeys.ids2]);
        console.log(queryMap);
        console.log(this.queryKeys.ids1);
        console.log(this.queryKeys.ids2);
        if (csv_count == 0) {
            return null;
        } else if (csv_count == 1) {
            var ingredient_csv = '';
            if (queryMap[this.queryKeys.ids1] != '') {
                ingredient_csv = queryMap[this.queryKeys.ids1];
            } else {
                ingredient_csv = queryMap[this.queryKeys.ids2];
            }
            sql = this.single_sql_format.replace('{ingredient_csv}', ingredient_csv) +
                " OFFSET " + offset + " LIMIT " + per_page;
        } else if (csv_count == 2) {
            // レシピの共通部を取る
            // OFFSET, LIMIT 指定用にインラインビュー化する
            sql =
                "SELECT * FROM ( " +
                this.single_sql_format.replace('{ingredient_csv}', queryMap[this.queryKeys.ids1]) +
                " INTERSECT " +
                this.single_sql_format.replace('{ingredient_csv}', queryMap[this.queryKeys.ids2]) +
                " ) AS TEMP " +
                " OFFSET " + offset + " LIMIT " + per_page;
	    // ingredient_csv = queryMap[this.queryKeys.ids1] + ',' + queryMap[this.queryKeys.ids2]
	    // sql =
	    // 	"SELECT * FROM ( " +
	    // 	this.single_sql_format.replace(
	    // 	    "{ingredient_csv}", ingredient_csv
	    // 	) +
	    // 	" ) AS TEMP " +
	    // 	"OFFSET " + offset + " LIMIT " + per_page;
	            
        } else {
            return null;
        }

        console.log(sql);

        return sql;
    }

    construct_recipe_count_query(queryMap) {
        var csv_count = this.get_ingredient_csv_count(queryMap[this.queryKeys.ids1], queryMap[this.queryKeys.ids2]);

        var sql_count = '';

        if (csv_count == 0) {
            return null;
        } else if (csv_count == 1) {
            var ingredient_csv = '';
            if (queryMap[this.queryKeys.ids1] != '') {
                ingredient_csv = queryMap[this.queryKeys.ids1];
            } else {
                ingredient_csv = queryMap[this.queryKeys.ids2];
            }
            sql_count =
                "SELECT COUNT(*) FROM ( " +
                this.single_sql_format +
                " ) AS TEMP";
            sql_count = sql_count.replace('{ingredient_csv}', ingredient_csv);
        } else if (csv_count == 2) {
            sql_count =
                "SELECT COUNT(*) FROM ( " +
                this.single_sql_format.replace('{ingredient_csv}', queryMap[this.queryKeys.ids1]) +
                " INTERSECT " +
                this.single_sql_format.replace('{ingredient_csv}', queryMap[this.queryKeys.ids2]) +
                " ) AS TEMP ";
        } else {
            return null;
        }

        //console.log(sql_count);

        return sql_count;
    }

    compute_offset(total_count, per_page, page_index) {
        return page_index * per_page;
    }

    get_ingredient_csv_count(ingredient_ids1, ingredient_ids2) {
        var ids1_is_empty = ingredient_ids1 == null || ingredient_ids1 == '';
        var ids2_is_empty = ingredient_ids2 == null || ingredient_ids2 == '';

        if (ids1_is_empty) {
            if (ids2_is_empty) {
                return 0;
            } else {
                return 1;
            }
        } else {
            if (ids2_is_empty) {
                return 1;
            } else {
                return 2;
            }
        }

        return -1;
    }

    construct_push_html(res_rows, queryMap, count_records, per_page, page_index) {
        console.log('construct_push_html()');

        if (res_rows.length == 0) {
            return '';
        }

        var table = this.construct_table_partial_html(res_rows);
        var pagination = this.construct_pagination_partial_html(queryMap, count_records, per_page, page_index);
        var html_body =
            '<div>' +
            '    <div>' +
            table +
            '    </div>' +
            '    <div>' +
            pagination +
            '    </div>' +
            '</div>';

        var html = "<div>" + html_body + "</div>";
        return html;
    }

    //_TEST_
    construct_table_partial_html(res_rows) {
        var table_format = '<table class="table table"><thead>{thead}</thead><tbody>{tbody}</tbody></table>';
        var table_header = '<th>#</th><th>recipe_name</th><th>introductory_essay</th><th>disy_type</th><th>genre</th><th>food_type</th><th>file_name</th>';
        var table_content = '';

        for (var i = 0; i < res_rows.length; ++i) {
            var row = res_rows[i];

            var recipe_name = row[sqlKey_recipe_name];
            var introductory_essay = row[sqlKey_introductory_essay];
            var dish_type_name = row[sqlKey_dish_type_name];
            var genre_name = row[sqlKey_genre_name];
            var food_type_name = row[sqlKey_food_type_name];
            var file_name = row[sqlKey_file_name];

            table_content +=
                '<tr>' +
                '<td>' + (i + 1) + '</td>' +
                '<td>' + recipe_name + '</td>' +
                '<td>' + introductory_essay + '</td>' +
                '<td>' + dish_type_name + '</td>' +
                '<td>' + genre_name + '</td>' +
                '<td>' + food_type_name + '</td>' +
                '<td><img src="./public/picture/' + file_name + '"></td>' +
                '</tr>';

            //_TEST_
            if (i == 0) {
                console.log(row);
            }
        }

        var table = table_format.replace('{thead}', table_header).replace('{tbody}', table_content);
        return table;
    }

    construct_pagination_partial_html(queryMap, count_records, per_page, page_index) {
        var count_page_icons = count_records / per_page;
        if (count_records % per_page != 0) {
            ++count_page_icons;
        }

        var pagination = '<ul class="pagination">{list}</ul>';
        var list = '';
        // icon.prev
        if (page_index > 0) {
            list += this.get_pagination_list(queryMap, page_index - 1, '1つ前');
        }
        // icon.pages
        for (var i = 0; i < count_page_icons; ++i) {
            list += this.get_pagination_list(queryMap, i, (i + 1).toString());
        }
        // icon.next
        if (page_index < count_page_icons - 1) {
            list += this.get_pagination_list(queryMap, page_index + 1, '1つ後');
        }
        pagination = pagination.replace('{list}', list);

        return pagination;
    }

    get_pagination_list(queryMap, target_page_index, text) {
        var url = this.get_pagination_href(queryMap, target_page_index);
        var script =
            "$.get('" + url + "', function (data, status) { $('#partial_view').html(data); });";
        //console.log(script);
        var list =
            '<li class="page-item"><a class="page-link" href="#" onclick="' + script + '">' + text + '</a></li>';
        //console.log(list);
        return list;
    }

    get_pagination_href(queryMap, page_index) {
        var href =
            'http://localhost:8080/update_recipe?ingredient_ids1=' + queryMap[this.queryKeys.ids1] +
            '&ingredient_ids2=' + queryMap[this.queryKeys.ids2] + '&frying_pan=' + queryMap[this.queryKeys.pan] + '&page_index=' + page_index;
        return href;
    }
}
