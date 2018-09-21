// (cf.) https://node-postgres.com
// (cf.) https://node-postgres.com/features/connecting

var http = require('http');
var querystring = require('querystring');
var ApiMethodController = require('./apiMethodController');
var TestController = require('./testController');

var ServerHost = "127.0.0.1";
var ServerPort = 8080;

function onRequest(request, response) {
    var url = request.url;
    var method = request.method;

    console.log(url);
    console.log(method);

    response.setHeader('Access-Control-Allow-Origin', '*');

    var controller = new ApiMethodController();
    var testController = new TestController();

    if (method == 'GET') {
        var apiMethod = getApiMethod(url);
        console.log(apiMethod);

        if (apiMethod == '/update_recipe') {
            var queryMap = getQueryParameters(url);
            if (queryMap.length == 0) {
                response.statusCode = 400;
                response.end();
            }
            controller.update_recipe(request, response, queryMap);
        } else if (url == '/get_ingredient_list') {
            controller.get_ingredient_list(request, response);
        } else if (url == '/get_image') {
            testController.get_image(request, response);
        } else if (url == '/get_sample_html') {
            testController.get_sample_html(request, response);
        } else {
            response.end();
        }
    } else {
        response.end();
    }
}

function getQueryParameters(url) {
    console.log('getQueryParameters()');

    // ? 以降の文字列を取得
    var indexQuery = url.indexOf('?');
    if (indexQuery == -1) {
        return [];
    }
    var queryStr = url.substring(indexQuery + 1);
    //console.log(queryStr);

    var queryMap = querystring.parse(queryStr);
    //console.log(queryMap);

    return queryMap;
}

// url: /update_recipe_test?ingredient_name='トマト'
// url: /get_image
function getApiMethod(url) {
    console.log('getApiMethod()');

    var indexQuery = url.indexOf('?');
    if (indexQuery == -1) {
        return url;
    }

    var apiMethod = url.substring(0, indexQuery);
    return apiMethod;
}

function init() {
    http.createServer(onRequest).listen(ServerPort, ServerHost);
}

init();
