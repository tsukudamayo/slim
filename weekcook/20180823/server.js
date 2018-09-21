// (cf.) https://node-postgres.com
// (cf.) https://node-postgres.com/features/connecting

var http = require('http');
var querystring = require('querystring');
var WebSocketServer = require('websocket').server;
var ApiMethodController = require('./apiMethodController');

var ServerHost = "127.0.0.1";
var ServerPort = 8080;

// 設定をサーバ側に持つ
var ServerPushSetting = {
    showItemsPerPage: 3
};

var QueryKeys = {
    ids1: 'ingredient_ids1',
    ids2: 'ingredient_ids2',
    pan: 'frying_pan',
    page: 'page_index'
};

var ws_connection;

function onRequest(request, response) {
    var url = request.url;
    var method = request.method;

    console.log(url);
    console.log(method);

    response.setHeader('Access-Control-Allow-Origin', '*');

    var controller = new ApiMethodController(ServerPushSetting, QueryKeys);

    if (method == 'GET') {
        var apiMethod = getApiMethod(url);
        console.log(apiMethod);

        if (apiMethod == '/update_recipe') {
            var queryMap = getQueryParameters(url);
            if (queryMap.length == 0) {
                response.statusCode = 400;
                response.end();
                return;
            }
            controller.update_recipe(request, response, queryMap, ws_connection);
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

// url: /update_recipe_test?ingredient_ids1=1,2,3
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
    var plainHttpServer = http.createServer(onRequest).listen(ServerPort, ServerHost);
    var websocketServer = new WebSocketServer({ httpServer: plainHttpServer, autoAcceptConnections: false });
    websocketServer.on('request', function (req) {
        ws_connection = req.accept(null, req.origin);

        // client からメッセージを受けた場合
        ws_connection.on('message', function (message) {
            console.log('ws_connection.message');
        });

        ws_connection.on('close', function (reasonCode, description) {
            console.log('ws_connection.close');
        });
    });
}

init();


