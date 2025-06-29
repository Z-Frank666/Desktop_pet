import requests
from bs4 import BeautifulSoup

# 城市代码映射表（部分城市）
CITY_CODES = {
    "北京": "101010100", "上海": "101020100", "广州": "101280101",
    "深圳": "101280601", "杭州": "101210101", "成都": "101270101",
    "武汉": "101200101", "南京": "101190101", "重庆": "101040100",
    "西安": "101110101", "长沙": "101250101", "天津": "101030100"
}


def get_city_code(city_name):
    """获取城市对应的天气代码，支持中文名或直接输入代码"""
    if city_name in CITY_CODES:
        return CITY_CODES[city_name]
    # 检查是否直接输入了代码
    if city_name.isdigit() and len(city_name) == 9:
        return city_name
    print(f"未找到城市: {city_name}，使用默认值（北京）")
    return CITY_CODES["北京"]


def get_weather_data(city_code):
    """爬取指定城市的天气数据"""
    # https: // www.weather.com.cn / weather1d / 101200101.shtml  # search
    url = f'https://www.weather.com.cn/weather1d/{city_code}.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"请求失败: HTTP {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取当前温度
        try:
            temp = soup.find('div', class_='tem').get_text(strip=True)
        except AttributeError:
            temp = "未获取到温度数据"

        # 提取天气状况
        try:
            condition = soup.find('div', class_='wea').get_text(strip=True)
        except AttributeError:
            condition = "未获取到天气状况"

        # 提取24小时预报（未来6小时）
        hourly_forecast = []
        try:
            hourly_items = soup.find('div', class_='hour3data').find_all('li')[:6]
            for item in hourly_items:
                time = item.find('span', class_='time').get_text(strip=True)
                temp_hour = item.find('span', class_='tem').get_text(strip=True)
                weather = item.find('span', class_='weather').get_text(strip=True)
                hourly_forecast.append(f"{time}: {weather} {temp_hour}")
        except Exception:
            hourly_forecast = ["暂无小时预报数据"]

        return {
            'temperature': temp,
            'condition': condition,
            'hourly_forecast': hourly_forecast
        }

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None, None


def main():
    """主程序：用户交互获取天气信息"""
    print("\n=== 中国天气查询 ===")
    print("支持的城市:", list(CITY_CODES.keys()))
    print("-" * 30)

    while True:
        city_name = input("请输入城市名称（或代码，回车退出）：").strip()

        if not city_name:
            break

        city_code = get_city_code(city_name)
        weather_data = get_weather_data(city_code)

        if weather_data:
            print(f"\n{city_name} 当前天气:")
            print(f"温度: {weather_data['temperature']}")
            print(f"天气状况: {weather_data['condition']}")
            print("\n未来6小时预报:")
            for forecast in weather_data['hourly_forecast']:
                print(f"  • {forecast}")
            print("-" * 30)
        else:
            print(f"未能获取 {city_name} 的天气数据")


if __name__ == "__main__":
    main()