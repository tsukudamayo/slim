import requests

def main():
    request()

def request():
    #response = requests.get('http://localhost:8080/update_recipe?ingredient_name1=tomato&ingredient_name2=')
    print('pre request')
    response = requests.get('http://localhost:8080/update_recipe?ingredient_name1=tomato')
    print('post response')

if __name__ == '__main__':
    main();
