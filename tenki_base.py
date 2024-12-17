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
        wind TEXT,
        PRIMARY KEY (area_code, date)
    )
    ''')
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

def store_weather_data(area_code, forecasts):
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()
    for forecast in forecasts:
        for date, weather, wind in zip(forecast['date'], forecast['weather'], forecast['wind']):
            c.execute('INSERT OR REPLACE INTO weather_info (area_code, date, weather, wind) VALUES (?, ?, ?, ?)',
                      (area_code, date, weather, wind))
    conn.commit()
    conn.close()

def fetch_and_display_forecast(page: ft.Page, area_code):
    response = requests.get(f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json")
    if response.status_code == 200:
        data = response.json()

        # レスポンスのデバッグ出力（応答内容を確認）
        print(json.dumps(data, indent=2))

        forecast_data = []
        for entry in data:
            if 'timeSeries' in entry and entry['timeSeries']:
                timeseries = entry['timeSeries'][0]
                if 'areas' in timeseries and timeseries['areas']:
                    area_details = timeseries['areas'][0]

                    # 'weathers' キーが存在するか確認し、存在しない場合は空リストを使用
                    weathers = area_details.get('weathers', [])
                    winds = area_details.get('winds', [])
                    dates = timeseries.get('timeDefines', [])

                    forecast_data.append({
                        'date': dates,
                        'weather': weathers,
                        'wind': winds
                    })

        store_weather_data(area_code, forecast_data)
        display_weather_info(page, area_code)
    else:
        # 失敗したときのハンドリング
        weather_text = page.controls[1] if page.controls[1] else ft.TextField()
        weather_text.value = "データの取得に失敗しました。"
        page.update()
        
def display_weather_info(page: ft.Page, area_code):
    conn = sqlite3.connect('weather_app.db')
    c = conn.cursor()
    c.execute('SELECT date, weather, wind FROM weather_info WHERE area_code=? ORDER BY date', (area_code,))
    info = c.fetchall()
    result = "\n".join([f"Date: {row[0]}, Weather: {row[1]}, Wind: {row[2]}" for row in info])
    weather_text = page.controls[1]
    weather_text.value = result
    page.update()

def main(page: ft.Page):
    create_db_and_tables()
    page.title = "天気予報アプリ"
    area_response = requests.get("https://www.jma.go.jp/bosai/common/const/area.json")
    if area_response.status_code == 200:
        area_data = area_response.json()
        populate_area_table(area_data)  # Update DB with the latest area data
        options = [ft.dropdown.Option(text=details['name'], key=code) for code, details in area_data['offices'].items()]
        dropdown = ft.Dropdown(options=options, on_change=lambda e: fetch_and_display_forecast(page, e.control.value))
        weather_text = ft.TextField(value="地域を選択してください", multiline=True, expand=True)
        page.add(dropdown, weather_text)
    else:
        page.add(ft.Text("Failed to retrieve area data."))

if __name__ == '__main__':
    ft.app(target=main)