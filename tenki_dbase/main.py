
# import sqlite3
# import json
# import requests
# import flet as ft

# def create_db_and_tables():
#     conn = sqlite3.connect('weather_app.db')
#     conn.execute('''
#     CREATE TABLE IF NOT EXISTS weather_areas (
#         code TEXT PRIMARY KEY,
#         name TEXT,
#         en_name TEXT,
#         office_name TEXT,
#         parent TEXT
#     )
#     ''')
#     conn.execute('''
#     CREATE TABLE IF NOT EXISTS weather_info (
#         area_code TEXT,
#         date TEXT,
#         weather TEXT,
#         weather_code TEXT,
#         wind TEXT,
#         wave TEXT,
#         temps_min TEXT,
#         temps_max TEXT,
#         PRIMARY KEY (area_code, date)
#     )
#     ''')
#     conn.close()

# def add_missing_columns():
#     conn = sqlite3.connect('weather_app.db')
#     c = conn.cursor()

#     # 追加したいカラムとそのデータ型のリスト
#     columns_to_add = [
#         ('weather_code', 'TEXT'),
#         ('wind', 'TEXT'),
#         ('wave', 'TEXT'),
#         ('temps_min', 'TEXT'),
#         ('temps_max', 'TEXT')
#     ]

#     for column_name, data_type in columns_to_add:
#         try:
#             c.execute(f'ALTER TABLE weather_info ADD COLUMN {column_name} {data_type}')
#             conn.commit()
#         except sqlite3.OperationalError as e:
#             # カラムが既に存在する場合のエラーを無視
#             if f'duplicate column name: {column_name}' not in str(e):
#                 raise
#     conn.close()

# def populate_area_table(data):
#     conn = sqlite3.connect('weather_app.db')
#     c = conn.cursor()
#     c.execute('DELETE FROM weather_areas')
#     for code, details in data['offices'].items():
#         c.execute('INSERT INTO weather_areas (code, name, en_name, office_name, parent) VALUES (?, ?, ?, ?, ?)',
#                   (code, details['name'], details['enName'], details['officeName'], details['parent']))
#     conn.commit()
#     conn.close()

# def store_weather_data(area_code, forecast_data):
#     conn = sqlite3.connect('weather_app.db')
#     c = conn.cursor()

#     time_series = forecast_data[0]['timeSeries'][0]
#     time_defines = time_series['timeDefines']
#     areas = time_series['areas']

#     temps_series = None
#     temps_time_defines = None
#     temps_areas = None
#     if len(forecast_data[0]['timeSeries']) > 1:
#         temps_series = forecast_data[0]['timeSeries'][1]
#         temps_time_defines = temps_series['timeDefines']
#         temps_areas = temps_series['areas']

#     for area in areas:
#         area_name = area['area']['name']
#         weather_codes = area.get('weatherCodes', [])
#         weathers = area.get('weathers', [])
#         winds = area.get('winds', [])
#         waves = area.get('waves', [])

#         for i, date in enumerate(time_defines):
#             date_short = date[:10]
#             weather_code = weather_codes[i] if i < len(weather_codes) else ''
#             weather = weathers[i] if i < len(weathers) else ''
#             wind = winds[i] if i < len(winds) else ''
#             wave = waves[i] if i < len(waves) else ''

#             temps_min = ''
#             temps_max = ''
#             # 対応する気温情報を取得
#             if temps_areas:
#                 for temps_area in temps_areas:
#                     if temps_area['area']['name'] == area_name:
#                         try:
#                             idx = temps_time_defines.index(date)
#                             temps_min_list = temps_area.get('tempsMin', [])
#                             temps_max_list = temps_area.get('tempsMax', [])
#                             temps_min = temps_min_list[idx] if idx < len(temps_min_list) else ''
#                             temps_max = temps_max_list[idx] if idx < len(temps_max_list) else ''
#                         except ValueError:
#                             pass  # dateがtemps_time_definesにない場合
#                         break

#             c.execute('INSERT OR REPLACE INTO weather_info (area_code, date, weather_code, weather, wind, wave, temps_min, temps_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
#                       (area_code, date, weather_code, weather, wind, wave, temps_min, temps_max))

#     conn.commit()
#     conn.close()

# def fetch_and_display_forecast(page: ft.Page, area_code):
#     response = requests.get(f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json")
#     if response.status_code == 200:
#         forecast_data = response.json()

#         # データベースに格納
#         store_weather_data(area_code, forecast_data)
        
#         # 天気情報の表示
#         display_weather_info(page, area_code)
#     else:
#         # 失敗したときのハンドリング
#         weather_text = page.controls[0].controls[2] if len(page.controls[0].controls) > 2 else ft.TextField()
#         weather_text.value = "データの取得に失敗しました。"
#         page.update()

# # 天気コードと画像ファイル名のマッピングを作成
# weather_code_to_image = {
#     # 実際の天気コードと画像ファイル名をすべてマッピングする必要があります
#     # 以下は例として一部を記載しています
#     "100": "100.png",
#     "101": "101.png",
#     "102": "102.png",
#     "103": "103.png",
#     "104": "104.png",
#     "105": "105.png",
#     "106": "106.png",
#     "107": "107.png",
#     "108": "108.png",
#     "110": "110.png",
#     "112": "112.png",
#     "115": "115.png",
#     "120": "120.png",
#     "122": "122.png",
#     "123": "123.png",
#     "124": "124.png",
#     "125": "125.png",
#     "126": "126.png",
#     "127": "127.png",
#     "128": "128.png",
#     "130": "130.png",
#     "131": "131.png",
#     "132": "132.png",
#     "140": "140.png",
#     "160": "160.png",
#     "170": "170.png",
#     "200": "200.png",
#     "201": "201.png",
#     "202": "202.png",
#     "203": "203.png",
#     "204": "204.png",
#     "205": "205.png",
#     "206": "206.png",
#     "207": "207.png",
#     "208": "208.png",
#     "209": "209.png",
#     "210": "210.png",
#     "211": "211.png",
#     "212": "212.png",
#     "213": "213.png",
#     "214": "214.png",
#     "215": "215.png",
#     "216": "216.png",
#     "217": "217.png",
#     "218": "218.png",
#     "219": "219.png",
#     "220": "220.png",
#     "221": "221.png",
#     "222": "222.png",
#     "223": "223.png",
#     "224": "224.png",
#     "225": "225.png",
#     "226": "226.png",
#     "228": "228.png",
#     "229": "229.png",
#     "230": "230.png",
#     "231": "231.png",
#     "240": "240.png",
#     "250": "250.png",
#     "260": "260.png",
#     "270": "270.png",
#     "281": "281.png",
#     "300": "300.png",
#     "301": "301.png",
#     "302": "302.png",
#     "303": "303.png",
#     "304": "304.png",
#     "305": "305.png",
#     "306": "306.png",
#     "307": "307.png",
#     "308": "308.png",
#     "309": "309.png",
#     "310": "310.png",
#     "311": "311.png",
#     "312": "312.png",
#     "313": "313.png",
#     "314": "314.png",
#     "315": "315.png",
#     "316": "316.png",
#     "317": "317.png",
#     "318": "318.png",
#     "320": "320.png",
#     "321": "321.png",
#     "322": "322.png",
#     "323": "323.png",
#     "324": "324.png",
#     "325": "325.png",
#     "326": "326.png",
#     "327": "327.png",
#     "328": "328.png",
#     "329": "329.png",
#     "330": "330.png",
#     "331": "331.png",
#     "332": "332.png",
#     "333": "333.png",
#     "334": "334.png",
#     "335": "335.png",
#     "336": "336.png",
#     "337": "337.png",
#     "338": "338.png",
#     "339": "339.png",
#     "340": "340.png",
#     "341": "341.png",
#     "342": "342.png",
#     "343": "343.png",
#     "344": "344.png",
#     "345": "345.png",
#     "346": "346.png",
#     "347": "347.png",
#     "348": "348.png",
#     "349": "349.png",
#     "350": "350.png",
#     # 必要に応じて他の天気コードも追加してください
# }

# def get_weather_icon_url(weather_code):
#     if weather_code and len(weather_code) >=3:
#         # 天気コードの先頭3文字を使用
#         code = weather_code[:3]
#         image_file = weather_code_to_image.get(code)
#         if image_file:
#             return f"https://www.jma.go.jp/bosai/forecast/img/{image_file}"
#     return "https://www.jma.go.jp/bosai/forecast/img/unknown.png"  # デフォルト画像のパス

# def display_weather_info(page: ft.Page, area_code):
#     conn = sqlite3.connect('weather_app.db')
#     c = conn.cursor()
#     c.execute('SELECT date, weather_code, weather, wind, wave, temps_min, temps_max FROM weather_info WHERE area_code=? ORDER BY date', (area_code,))
#     info = c.fetchall()
#     conn.close()

#     weather_info_controls = []
#     for row in info:
#         date = row[0][:10]  # YYYY-MM-DD 形式
#         weather_code = row[1]
#         weather_desc = row[2]
#         icon_url = get_weather_icon_url(weather_code)
#         wind = row[3]
#         wave = row[4]
#         temps_min = row[5] if row[5] else '情報なし'
#         temps_max = row[6] if row[6] else '情報なし'

#         weather_info_controls.append(
#             ft.Card(
#                 content=ft.Row([
#                     ft.Image(
#                         src=icon_url,
#                         width=50,
#                         height=50,
#                         fit=ft.ImageFit.CONTAIN,
#                         # 'error_builder' を削除
#                     ),
#                     ft.Column([
#                         ft.Text(f"{date}", size=16, weight="bold"),
#                         ft.Text(f"{weather_desc}"),
#                         ft.Text(f"風: {wind}"),
#                         ft.Text(f"波: {wave}"),
#                         ft.Text(f"最低気温: {temps_min}°C, 最高気温: {temps_max}°C"),
#                     ], alignment="start", spacing=5),
#                 ], spacing=10),
#                 width=400
#             )
#         )

#     weather_column = ft.Column(weather_info_controls, scroll='auto')
#     page.controls[0].controls[2] = weather_column
#     page.update()

# def main(page: ft.Page):
#     create_db_and_tables()
#     add_missing_columns()  # 不足しているカラムを追加
#     page.title = "天気予報アプリ"

#     # 地域リストを取得
#     area_response = requests.get("https://www.jma.go.jp/bosai/common/const/area.json")
#     if area_response.status_code != 200:
#         page.add(ft.Text("地域リストの取得に失敗しました。"))
#         return

#     area_data = area_response.json()
#     populate_area_table(area_data)  # Update DB with the latest area data

#     # ドロップダウンで使えるように地域データを加工
#     options = [ft.dropdown.Option(text=details['name'], key=code) for code, details in area_data['offices'].items()]
    
#     # 地域選択ドロップダウン
#     dropdown = ft.Dropdown(
#         options=options,
#         on_change=lambda e: fetch_and_display_forecast(page, e.control.value),
#         width=300,
#         value=options[0].key if options else None  # 初期値を設定
#     )
    
#     # 天気情報を表示するプレースホルダー
#     weather_info_placeholder = ft.Column([], scroll='auto')
    
#     # レイアウトにコントロールを配置
#     page.add(
#         ft.Column([
#             ft.Text("気象庁の天気予報アプリ", size=24, weight="bold"),
#             dropdown,
#             weather_info_placeholder
#         ], spacing=10, alignment="start")
#     )

#     # 初期表示で最初の地域の天気情報を取得
#     if options:
#         fetch_and_display_forecast(page, options[0].key)

# if __name__ == '__main__':
#     ft.app(target=main)

import sqlite3
import json
import requests
import flet as ft

def create_db_and_tables():
    conn = sqlite3.connect('weather_app.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS weather_areas (
        code TEXT PRIMARY KEY,
        name TEXT,
        en_name TEXT,
        office_name TEXT,
        parent TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS weather_info (
        area_code TEXT,
        date TEXT,
        weather TEXT,
        weather_code TEXT,
        wind TEXT,
        wave TEXT,
        PRIMARY KEY (area_code, date)
    )
    ''')
    conn.close()

def add_missing_columns():
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()

    # 追加したいカラムとそのデータ型のリスト
    columns_to_add = [
        ('weather_code', 'TEXT'),
        ('wind', 'TEXT'),
        ('wave', 'TEXT'),
    ]

    for column_name, data_type in columns_to_add:
        try:
            c.execute(f'ALTER TABLE weather_info ADD COLUMN {column_name} {data_type}')
            conn.commit()
        except sqlite3.OperationalError as e:
            # カラムが既に存在する場合のエラーを無視
            if f'duplicate column name: {column_name}' not in str(e):
                raise
    conn.close()

def populate_area_table(data):
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()
    c.execute('DELETE FROM weather_areas')
    for code, details in data['offices'].items():
        c.execute('INSERT INTO weather_areas (code, name, en_name, office_name, parent) VALUES (?, ?, ?, ?, ?)',
                  (code, details['name'], details['enName'], details['officeName'], details['parent']))
    conn.commit()
    conn.close()

def store_weather_data(area_code, forecast_data):
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()

    time_series = forecast_data[0]['timeSeries'][0]
    time_defines = time_series['timeDefines']
    areas = time_series['areas']

    for area in areas:
        area_name = area['area']['name']
        weather_codes = area.get('weatherCodes', [])
        weathers = area.get('weathers', [])
        winds = area.get('winds', [])
        waves = area.get('waves', [])

        for i, date in enumerate(time_defines):
            date_short = date[:10]
            weather_code = weather_codes[i] if i < len(weather_codes) else ''
            weather = weathers[i] if i < len(weathers) else ''
            wind = winds[i] if i < len(winds) else ''
            wave = waves[i] if i < len(waves) else ''

            c.execute('INSERT OR REPLACE INTO weather_info (area_code, date, weather_code, weather, wind, wave) VALUES (?, ?, ?, ?, ?, ?)',
                      (area_code, date, weather_code, weather, wind, wave))

    conn.commit()
    conn.close()

# 天気コードと画像ファイル名のマッピングを作成
weather_code_to_image = {
    # 天気コードと画像ファイル名をすべてマッピングしてください
    "100": "100.png",
    "101": "101.png",
    "102": "102.png",
    "103": "103.png",
    "104": "104.png",
    "105": "105.png",
    "106": "106.png",
    "107": "107.png",
    "108": "108.png",
    "110": "110.png",
    "112": "112.png",
    "115": "115.png",
    "120": "120.png",
    "122": "122.png",
    "123": "123.png",
    "124": "124.png",
    "125": "125.png",
    "126": "126.png",
    "127": "127.png",
    "128": "128.png",
    "130": "130.png",
    "131": "131.png",
    "132": "132.png",
    "140": "140.png",
    "160": "160.png",
    "170": "170.png",
    "200": "200.png",
    "201": "201.png",
    "202": "202.png",
    "203": "203.png",
    "204": "204.png",
    "205": "205.png",
    "206": "206.png",
    "207": "207.png",
    "208": "208.png",
    "209": "209.png",
    "210": "210.png",
    "211": "211.png",
    "212": "212.png",
    "213": "213.png",
    "214": "214.png",
    "215": "215.png",
    "216": "216.png",
    "217": "217.png",
    "218": "218.png",
    "219": "219.png",
    "220": "220.png",
    "221": "221.png",
    "222": "222.png",
    "223": "223.png",
    "224": "224.png",
    "225": "225.png",
    "226": "226.png",
    "228": "228.png",
    "229": "229.png",
    "230": "230.png",
    "231": "231.png",
    "240": "240.png",
    "250": "250.png",
    "260": "260.png",
    "270": "270.png",
    "281": "281.png",
    "300": "300.png",
    "301": "301.png",
    "302": "302.png",
    "303": "303.png",
    "304": "304.png",
    "305": "305.png",
    "306": "306.png",
    "307": "307.png",
    "308": "308.png",
    "309": "309.png",
    "310": "310.png",
    "311": "311.png",
    "312": "312.png",
    "313": "313.png",
    "314": "314.png",
    "315": "315.png",
    "316": "316.png",
    "317": "317.png",
    "318": "318.png",
    "320": "320.png",
    "321": "321.png",
    "322": "322.png",
    "323": "323.png",
    "324": "324.png",
    "325": "325.png",
    "326": "326.png",
    "327": "327.png",
    "328": "328.png",
    "329": "329.png",
    "330": "330.png",
    "331": "331.png",
    "332": "332.png",
    "333": "333.png",
    "334": "334.png",
    "335": "335.png",
    "336": "336.png",
    "337": "337.png",
    "338": "338.png",
    "339": "339.png",
    "340": "340.png",
    "341": "341.png",
    "342": "342.png",
    "343": "343.png",
    "344": "344.png",
    "345": "345.png",
    "346": "346.png",
    "347": "347.png",
    "348": "348.png",
    "349": "349.png",
    "350": "350.png",
    # 他の天気コードも追加してください
}

def get_weather_icon_url(weather_code):
    if weather_code and len(weather_code) >=3:
        # 天気コードの先頭3文字を使用
        code = weather_code[:3]
        image_file = weather_code_to_image.get(code)
        if image_file:
            return f"https://www.jma.go.jp/bosai/forecast/img/{image_file}"
    return "https://www.jma.go.jp/bosai/forecast/img/unknown.png"  # デフォルト画像のパス

def fetch_and_display_forecast(page: ft.Page, area_code):
    # ローディングインジケーターを表示
    loading_indicator = ft.ProgressRing()
    
    # 天気情報プレースホルダーを取得
    weather_info_placeholder = page.controls[0].controls[2]
    weather_info_placeholder.controls.clear()
    weather_info_placeholder.controls.append(loading_indicator)
    page.update()

    # データ取得
    response = requests.get(f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json")

    if response.status_code == 200:
        forecast_data = response.json()

        # データベースに格納
        store_weather_data(area_code, forecast_data)
        
        # 天気情報の表示
        display_weather_info(page, area_code)
    else:
        # 失敗したときのハンドリング
        weather_info_placeholder.controls.clear()
        weather_info_placeholder.controls.append(ft.Text("データの取得に失敗しました。"))
        page.update()

def display_weather_info(page: ft.Page, area_code):
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()
    c.execute('SELECT date, weather_code, weather, wind, wave FROM weather_info WHERE area_code=? ORDER BY date', (area_code,))
    info = c.fetchall()
    conn.close()

    weather_info_controls = []
    for row in info:
        date = row[0][:10]  # YYYY-MM-DD 形式
        weather_code = row[1]
        weather_desc = row[2]
        icon_url = get_weather_icon_url(weather_code)
        wind = row[3]
        wave = row[4]

        weather_info_controls.append(
            ft.Card(
                content=ft.Row([
                    ft.Image(
                        src=icon_url,
                        width=50,
                        height=50,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Column([
                        ft.Text(f"{date}", size=16, weight="bold"),
                        ft.Text(f"{weather_desc}"),
                        ft.Text(f"風: {wind}"),
                        ft.Text(f"波: {wave}"),
                    ], alignment="start", spacing=5),
                ], spacing=10),
                width=400
            )
        )

    weather_column = ft.Column(weather_info_controls, scroll='auto')
    
    # 天気情報プレースホルダーを取得し更新
    weather_info_placeholder = page.controls[0].controls[2]
    weather_info_placeholder.controls.clear()
    weather_info_placeholder.controls.append(weather_column)
    page.update()

def main(page: ft.Page):
    create_db_and_tables()
    add_missing_columns()  # 不足しているカラムを追加
    page.title = "天気予報アプリ"

    # 地域リストを取得
    area_response = requests.get("https://www.jma.go.jp/bosai/common/const/area.json")
    if area_response.status_code != 200:
        page.add(ft.Text("地域リストの取得に失敗しました。"))
        return

    area_data = area_response.json()
    populate_area_table(area_data)  # 最新の地域データでDBを更新

    # ドロップダウンで使えるように地域データを加工
    options = [ft.dropdown.Option(text=details['name'], key=code) for code, details in area_data['offices'].items()]
    
    # 地域選択ドロップダウン
    dropdown = ft.Dropdown(
        options=options,
        on_change=lambda e: fetch_and_display_forecast(page, e.control.value),
        width=300,
        value=options[0].key if options else None  # 初期値を設定
    )
    
    # 天気情報を表示するプレースホルダー
    weather_info_placeholder = ft.Column([], scroll='auto')
    
    # レイアウトにコントロールを配置
    page.add(
        ft.Column([
            ft.Text("気象庁の天気予報アプリ", size=24, weight="bold"),
            dropdown,
            weather_info_placeholder
        ], spacing=10, alignment="start")
    )

    # 初期表示で最初の地域の天気情報を取得
    if options:
        fetch_and_display_forecast(page, options[0].key)

if __name__ == '__main__':
    ft.app(target=main)