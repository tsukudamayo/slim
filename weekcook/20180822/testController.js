//var fs = require('fs');
const { Client } = require('pg');
const connectionString = 'postgresql://postgres:admin@localhost:5432/postgres'

const client = new Client({
    connectionString: connectionString
});

module.exports = class TestController {
    constructor() {
    }

    // GET get_image
    // TODO: Test
    get_image(request, response) {
        console.log(request.url);

        response.setHeader('Content-Type', 'text/html');
        var partial_view = '<div><img src="./public/picture/01_2.jpg"></div>';
        response.write(partial_view);

        response.end();
    }

    // GET get_sample_html
    get_sample_html(request, response) {
        client.connect();

        var sql = this.construct_test_sql();
        client.query(sql, (err, res) => {

        });

        response.end();
    }

    // レシピ名、画像、ジャンルを (2件ヒットする例で) 取得
    construct_test_sql() {
        var sql =
            "";

        return sql;
    }

    // TODO: レシピ名、画像、ジャンルを (10件ほどヒットする例で) ページング
    // 
}
