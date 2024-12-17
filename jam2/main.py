import requests
import flet as ft

def main(page: ft.Page):
    page.title = "気象庁の天気予報アプリ"
   

    # 地域リストを取得
    area_response = requests.get("https://www.jma.go.jp/bosai/common/const/area.json")
    if area_response.status_code != 200:
        page.add(ft.Text("地域リストの取得に失敗しました。"))
        return

    areas_data = area_response.json()
    # ドロップダウンで使えるように地域データを加工
    options = [ft.dropdown.Option(text=info['name'], key=code) for code, info in areas_data['offices'].items()]

    # 地域選択ドロップダウン
    dropdown = ft.Dropdown(options=options, on_change=lambda e: on_area_selected(page, e.control))
    weather_text = ft.TextField(value="地域を選択してください。", multiline=True, expand=True)
    
    # レイアウトにコントロールを配置
    page.add(dropdown, weather_text)

def on_area_selected(page: ft.Page, dropdown: ft.Dropdown):
    # 選択された地域コードの天気予報を取得
    area_code = dropdown.value
    response = requests.get(f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json")
    weather_text = page.controls[1]  # 既にページにあるTextFieldを取得
    
    if response.status_code == 200:
        forecast_data = response.json()
        display_weather_forecast(page, forecast_data, weather_text)
    else:
        weather_text.value = "天気予報の取得に失敗しました。"
        page.update()


def display_weather_forecast(page: ft.Page, forecast_data, weather_text: ft.TextField):
    # 天気と絵文字のマッピング
   
    weather_emoji  = {
    "100": "☀️",  # 晴れ
    "101": "⛅️",  # 晴時々曇
    "102": "☀️🌥",  # 晴一時曇
    "103": "☀️🌦",  # 晴時々雨
    "104": "☀️⛆",  # 晴一時雨
    "105": "☀️⛈",  # 晴時々雷雨
    "106": "☀️❄️",  # 晴一時雪
    "107": "☀️☃️",  # 晴時々雪
    "108": "☀️🌫",  # 晴時々霧
    "110": "☀️🌁",  # 晴後曇
    "111": "☀️🌧",  # 晴後雨
    "112": "☀️🌨",  # 晴後雪
    "113": "☀️🌬",  # 晴後風
    "150": "🌤",  # 晴れ朝夕曇
    "160": "🌤⛈",  # 晴れ朝の内一時雷雨
    "170": "🌤🌬",  # 晴れ夕方一時風
    "181": "☀️⛄️",  # 晴れのち雪か雨
    "200": "🌫",  # 霧
    "201": "☁️",  # 曇り
    "202": "☁️⛅️",  # 曇時々晴
    "203": "☁️🌦",  # 曇一時雨
    "204": "☁️⛈",  # 曇時々雷雨
    "205": "☁️❄️",  # 曇時々雪
    "206": "☁️🌨",  # 曇一時雪
    "207": "☁️🌫",  # 曇り時々霧
    "208": "☁️🌧",  # 曇後雨
    "209": "☁️🌨",  # 曇後雪
    "210": "☁️🌬",  # 曇後風
    "211": "☁️🌩",  # 曇り昼頃から晴れ
    "212": "☁️☔️",  # 曇り夕方から雨
    "213": "☁️⛄️",  # 曇り夜は雪か雨
    "250": "☁️🌤",  # 曇り朝夕晴れ
    "260": "☁️⛄️",  # 曇り朝夕雪か雨
    "270": "☁️❄️⛄️",  # 曇り昼頃から雪か雨
    "300": "🌧",  # 雨
    "301": "🌦",  # 雨時々晴れ
    "302": "🌧⛅️",  # 雨時々止む
    "303": "🌧❄️",  # 雨のち雪
    "304": "🌧☀️",  # 雨のち晴れ
    "305": "🌧⛈",  # 雨時々強く降る
    "306": "🌧⚡️",  # 雨時々雷を伴う
    "308": "🌧🌁",  # 雨後霧
    "309": "🌧🌫",  # 雨時々霧雨
    "310": "🌧🌬",  # 雨後風
    "311": "🌧🌩",  # 雨後雷
    # その他の天気コードや絵文字も追加可能
}

    # 天気予報データから情報を抽出して表示
    weather_info = "📅 天気予報\n"
    publishing_office = forecast_data[0]['publishingOffice']
    report_datetime = forecast_data[0]["reportDatetime"]
    weather_info += f"発表：{publishing_office}、{report_datetime}\n\n"

    # 第一のtimeSeries（天気、風、波の情報）
    weather_info += "🌤️ 地域別天気予報\n"
    for area in forecast_data[0]['timeSeries'][0]['areas']:
        area_name = area['area']['name']
        weather_info += f"地域：{area_name}\n"
        for i, time in enumerate(forecast_data[0]['timeSeries'][0]['timeDefines']):
            time = time[:10]  # YYYY-MM-DD 形式に整形
            weather_code = area['weatherCodes'][i]
            weather = area['weathers'][i]
            emoji = weather_emoji.get(weather_code, "")  # 天気コードから絵文字を取得
            wind = area['winds'][i]
            wave = area['waves'][i]
            weather_info += f"  {time}: {weather} {emoji}, 風: {wind}, 波: {wave}\n"
        weather_info += "-----\n"

    # 気温情報の表示
    weather_info += "🌡️ 気温予報\n"
    for area in forecast_data[1]['timeSeries'][1]['areas']:
        area_name = area['area']['name']
        weather_info += f"地域：{area_name}\n"
        for i, time in enumerate(forecast_data[1]['timeSeries'][1]['timeDefines']):
            time = time[:10]
            temps_min = area['tempsMin'][i]
            temps_max = area['tempsMax'][i]
            weather_info += f"  {time}: 最低気温 {temps_min}°C, 最高気温 {temps_max}°C\n"
        weather_info += "-----\n"

    weather_text.value = weather_info
    page.update()
    

ft.app(target=main)
