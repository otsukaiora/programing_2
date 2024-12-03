import json
import requests

# JSONファイルからデータを読み込む
with open('jam/areas.json', 'r') as file:
    areas = json.load(file)

# データを各クラスに分ける（ファイルの形式によります）
class10s = areas['class10s']
class15s = areas['class15s']
class20s = areas['class20s']

# 天気情報を取得する関数
def get_weather_data(region_code):
    parent_code = class15s[region_code]["data"]["parent"]
    children = {k: v for k, v in class20s.items() if v["parent"] == parent_code} 

    for child_code, child_data in children.items():
        url = f"https://your_weather_api.com/weather?region={child_code}"
        headers = {"Authorization": "Your API Key"}  

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to fetch weather data for {child_data['name']}. Status code: {response.status_code}"
          
# ある地域の天気を取得する（地域コードは一例です）
print(get_weather_data("016023"))