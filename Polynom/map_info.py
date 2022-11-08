import api
from sys import argv

def main():
    api_key = "97b8ff47-ad44-4018-645e-08dabbf9e85f"
    base_api_path = "https://api.considition.com/api/game/"
    map = int(argv[1])
    maps = ["Suburbia", "Fancyville", "Farmville", "Mountana", "Pleasure Ville", "Scy Scrape City"]
    map_name = "mountana"

    print(api.map_info(api_key, map_name))

if __name__ == "__main__":
    main()