import requests

def main():
    request()

def request():
    #tomato: トマト,ミニトマト,トマトカン,トマトミズニカン,フルーツトマト,ダイストマト,ミニトマトアカ,ホールトマトカン
    #42,46,181,182,504,571,602,774
    #broccoli: ブロッコリー,ブロッコリーコフサ,ブロッコリースプラウト
    #11,450,699
    #eggplant: ナス,ナガナス,ミズナス
    #43,617,700
    #cucumber: キュウリ
    #36
    print('pre request')
	#_GET
    #response = requests.get('http://localhost:8080/update_recipe?ingredient_ids1=42,46&ingredient_ids2=43,617&frying_pan=true&page_index=0')
    response = requests.get('http://localhost:8080/update_recipe?ingredient_ids1=42,46&ingredient_ids2=43,617&frying_pan=true')
    print('post response')

if __name__ == '__main__':
    main();
