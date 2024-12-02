
import requests
import flet as ft

# 地域リストの取得
def get_area_list():
    url = 'http://www.jma.go.jp/bosai/common/const/area.json'
    response = requests.get(url)
    if response.status_code == 200:
        area_data = response.json()
        
        # 再帰的に地域コードを取得
        area_codes = get_all_area_codes(area_data)
        return area_codes
    else:
        print("地域リストの取得に失敗しました。")
        return None

# 再帰的に地域コードを取得する関数
def get_all_area_codes(area_data):
    area_codes = {}

    # 各地域クラス（class10s, class15s, class20s など）を順に処理
    for area_class, areas in area_data.items():
        if isinstance(areas, dict):  # classXXs は辞書形式
            for area_code, area_info in areas.items():
                # 'name' が存在するか確認
                area_name = area_info.get('name', f"名前不明 ({area_code})")
                if not area_name:
                    area_name = area_info.get('enName', f"英名不明 ({area_code})")
                
                # area_code を格納
                area_codes[area_code] = {
                    'name': area_name,
                    'children': area_info.get('children', [])
                }

                # 子エリアがあれば再帰的に処理
                children = area_info.get('children', [])
                for child_code in children:
                    if child_code not in area_codes:
                        # 子エリアを再帰的に取得
                        child_area_data = {
                            area_class: {child_code: area_data[area_class].get(child_code, {})}
                        }
                        area_codes.update(get_all_area_codes(child_area_data))
    
    return area_codes

# 天気予報の取得
def get_weather_forecast(area_code):
    url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print(f"{area_code} の天気予報の取得に失敗しました。")
        return None

# 天気予報を表示
def display_weather_forecast(page, weather_data, weather_text):
    weather_info = ""
    
    # 時間ごとの天気予報を取得
    for time_series in weather_data[0]['timeSeries']:
        time_defines = time_series.get('timeDefines', [])
        for idx, area in enumerate(time_series['areas']):
            area_name = area['area']['name']
            weather_info += f"地域名: {area_name}\n"
            
            # 時間ごとの天気、気温、降水確率などを表示
            if 'weathers' in area:
                weather_info += f"天気: {area['weathers'][idx]}\n"
            if 'temps' in area:
                temps = area['temps']
                weather_info += f"気温: {temps[idx]}°C\n"
            if 'pops' in area:
                pops = area['pops']
                weather_info += f"降水確率: {pops[idx]}%\n"
            
            weather_info += "------\n"
    
    weather_text.value = weather_info
    page.update()

# 地域リストを表示
def display_area_list(page, area_dict, weather_text):
    # プルダウンリストに地域を追加
    area_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(text=area_info['name'], key=area_code) for area_code, area_info in area_dict.items()],
        on_change=lambda e: on_area_selected(page, e.control.value, weather_text, area_dict)
    )
    
    # 天気情報を表示するためのテキストを追加
    weather_text.value = "地域を選択してください"
    page.controls.clear()
    page.add(area_dropdown, weather_text)
    page.update()

# 地域が選択された時に呼ばれる関数
def on_area_selected(page, selected_area_code, weather_text, area_dict):
    # 天気予報を取得
    weather_data = get_weather_forecast(selected_area_code)
    if weather_data:
        display_weather_forecast(page, weather_data, weather_text)

# Fletのアプリケーションを実行
def main(page: ft.Page):
    page.title = "気象庁の天気予報アプリ"
    
    # 地域リストを取得
    area_codes = get_area_list()
    if not area_codes:
        page.add(ft.Text("地域リストの取得に失敗しました。"))
        return

    # 地域コードと名前を取得しやすくするために、リストを整理
    area_dict = {area_code: {'name': area_info['name'], 'children': area_info['children']} for area_code, area_info in area_codes.items()}

    # 天気情報を表示するテキストを追加
    weather_text = ft.Text(value="", size=14, color="black")

    # 地域リストを表示
    display_area_list(page, area_dict, weather_text)
    
    # 天気情報を表示するためのテキストを追加
    page.add(weather_text)

# Fletアプリを開始
ft.app(target=main)
