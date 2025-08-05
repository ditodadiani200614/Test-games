import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import HTTPError


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter city name: ",self)
        self.city_inpt=QLineEdit(self)
        self.weather_button=QPushButton("Get weather",self)
        self.temperature=QLabel(self)
        self.emoji=QLabel(self)
        self.description=QLabel(self)
        self.initUi()
    def initUi(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_inpt)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_inpt.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_inpt.setObjectName("city_inpt")
        self.weather_button.setObjectName("weather_button")
        self.temperature.setObjectName("temperature")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("description")

        self.setStyleSheet(""" 
        QLabel,QPushButton{
            font-family: calibri;
            }
        QLabel#city_label{
            font-size: 40px;
            font-style: italic; 
            }
        QLineEdit#city_inpt{
            font-size: 40px;
            }
        QPushButton{
            font-size: 30px;
            font-weight: bold;}
        QLabel#temperature{
            font-size: 75px;
            }  
        QLabel#emoji{
            font-size: 100px;
            font-family: Segoe UI emoji;}
        QLabel#description{
        font-size: 50px;
        }
        """)

        self.weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api_key='87d0aae916a3a4ec6de347e40fd60ee7'
        city=self.city_inpt.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data=response.json()
            if data['cod']==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as httperror:
            match response.status_code:
                case 400:
                    self.display_error('Bad Request:\nPlease check your Input')
                case 401:
                    self.display_error('Unauthorized:\nInvalid API key')
                case 403:
                    self.display_error('Forbidden:\nAccess Denied')
                case 404:
                    self.display_error('Not found:\nCity not found')
                case 500:
                    self.display_error('Internal Server Eror:\nPlease try again later')
                case 502:
                    self.display_error('Bad Gateway:\nInvalid response from the Server')
                case 503:
                    self.display_error('Service Unavailable:\nServer is down')
                case 504:
                    self.display_error('Gateway Timeout:\nNo response from the server')
                case _:
                    self.display_error(f"HTTP Error:\n{httperror}")
        except requests.exceptions.ConnectionError:
            self.display_error('Connection Error\nPlease check your internet connection')
        except requests.exceptions.Timeout:
            self.display_error('Timeout Error\nRequest Timed out')
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nCheck the Url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")


    def display_error(self,message):
        self.temperature.setStyleSheet("font-size: 30px;")
        self.temperature.setText(message)
        self.emoji.clear()
        self.description.clear()

    def display_weather(self,data):
        self.temperature.setStyleSheet("font-size: 75px;")
        temperature_k=data['main']['temp']
        temperature_C=temperature_k - 273.15
        weather_id=data["weather"][0]["id"]
        self.temperature.setText(f"{round (temperature_C,1)}°C")
        self.emoji.setText(self.get_weather_emoji(weather_id))
        weather_description=data['weather'][0]['description']
        self.description.setText(f"{weather_description}")
        # print(data)
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""




if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())