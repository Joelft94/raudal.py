from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from json import dumps
from clima import current_temperature_2m, current_relative_humidity_2m, current_wind_speed_10m, current_precipitation,daily_temperature_2m_max, daily_temperature_2m_min, current_weather_code, daily_weather_code, current_is_day,current_weather_code, daily_weather_code
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drawings.db'  # SQLite database for simplicity
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes

# Define a model for drawings
class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    geojson = db.Column(db.Text)  # Storing GeoJSON data as text

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')





@app.route('/home')
def mapa():
    return render_template('home.html', current_temperature_2m = int(current_temperature_2m), day_list = day_list, current_relative_humidity_2m = current_relative_humidity_2m ,current_wind_speed_10m= current_wind_speed_10m , dt=dt, AAAA = AAAA, MM = MM, DD= DD, current_precipitation = current_precipitation, temp_dia1=temp_dia1, temp_dia2=temp_dia2,temp_dia3=temp_dia3,temp_dia4=temp_dia4, tiempo_actual = tiempo_actual, icono=icono)

# Endpoint to save drawings to the database
@app.route('/save-drawing', methods=['POST'])
def save_drawing():
    data = request.json
    geojson_list = data.get('geojson')  # Assuming you'll send a list of GeoJSON objects
    geojson_str = dumps(geojson_list)   # Convert the list to a JSON string
    new_drawing = Drawing(geojson=geojson_str)
    db.session.add(new_drawing)
    db.session.commit()
    return jsonify({"message": "Se guardaron los datos"}), 200

# Endpoint to retrieve all drawings from the database
@app.route('/get-drawings', methods=['GET'])
def get_drawings():
    drawings = Drawing.query.all()
    drawings_list = [{"id": drawing.id, "geojson": drawing.geojson} for drawing in drawings]
    return jsonify(drawings_list), 200

# Endpoint to delete all drawings from the database
@app.route('/delete-drawings', methods=['DELETE'])
def delete_drawings():
    try:
        Drawing.query.delete()
        db.session.commit()
        return jsonify({"message": "Se borraron los datos"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#Aca lo del weather



""" Primero el dia actual """
# get current datetime
dt = datetime.now()     # dt = fecha de hoy
# print('Datetime is:', dt)

# get day of week as an integer   monday = 0 
x = int(dt.weekday())
 
day0 = "Monday"

if x == 1:
    day0 = "Tuesday"
    day1 = "Wednesday"
    day2 = "Thursday"
    day3 = "Friday"
    day4 = "Saturday"
    
elif x == 2:
    day0 = "Wednesday"
    day1 = "Thursday"
    day2 = "Friday"
    day3 = "Saturday"
    day4 = "Sunday"
elif x == 3:
    day0 = "Thursday"
    day1 = "Friday"
    day2 = "Saturday"
    day3 = "Sunday"
    day4 = "Monday"
elif x == 4:
    day0 = "Friday"
    day1 = "Saturday"
    day2 = "Sunday"
    day3 = "Monday"
    day4 = "Tuesday"
elif x == 5:
    day0 = "Saturday"
    day1 = "Sunday"
    day2 = "Monday"
    day3 = "Tuesday"
    day4 = "Wednesday"
elif x == 6:
    day0 = "Sunday"
    day1 = "Monday"
    day2 = "Tuesday"
    day3 = "Wednesday"
    day4 = "Thursday"
else:
    day0 = "Monday"
    day1 = "Tuesday"
    day2 = "Wednesday"
    day3 = "Thursday"
    day4 =  "Friday"

""" Ahora la lista para los sgtes dias """

day_list = [day0, day1, day2, day3, day4 ]

#Modificamos el orden de la fecha a formato DD/MM/AAAA

fecha = str(datetime.now())
AAAA = []
contador_anho = 0
for i in fecha:
    AAAA.append(i)
    contador_anho = contador_anho + 1
    if contador_anho == 4:
        break
    
MM = []
contador_mes = 3
i2=0
for i in fecha:
    i2= i2 + 1
    if i2 >= 5:
        MM.append(i)
        contador_mes = contador_mes +1
        if contador_mes == 8:
            break

DD = []
contador_dia = 8 
i3=0
for i in fecha:
    i3=i3 + 1
    if i3 >= 8:
        DD.append(i)
        contador_dia = contador_dia + 1
        if contador_dia == 11:
            break
    
current_precipitation = str(current_precipitation)
current_wind_speed_10m = int(current_wind_speed_10m)

#promediamos la temperatura para los sgtes dias

temp_dia1 =int((daily_temperature_2m_max[1] + daily_temperature_2m_min[1])/2)
temp_dia2 =int((daily_temperature_2m_max[2] + daily_temperature_2m_min[2])/2)
temp_dia3 =int((daily_temperature_2m_max[3] + daily_temperature_2m_min[3])/2)
temp_dia4 =int((daily_temperature_2m_max[4] + daily_temperature_2m_min[4])/2)

# aca vemos el tipo de clima que va a tener el dia

tiempo_actual = ["0","1","2","3","4"]
# daily_weather_code
icono = ["0","1", "2","3","4",]

for j in range(5):
    if daily_weather_code[j] == 0:
        tiempo_actual[j]="Clear sky"
        if j == 0:
            if current_is_day == 1:
                icono[j] = "sunny"
            else:
                icono[j] = "night"
                
    elif daily_weather_code[j] == 1:
        tiempo_actual[j] = 'Mainly clear'
        if current_is_day == 1:
            icono[j] = "sunny"
        else:
            icono[j] = "night"

    elif daily_weather_code[j] == 2:
        tiempo_actual[j]= 'Partly cloudy'
        if current_is_day == 1:
            icono[j] = "mostly_cloudy"
        else:
            icono[j] = "night_cloudy"
            
    elif daily_weather_code[j] == 3:
        tiempo_actual[j] = 'Overcast'
        icono[j] = "cloudy"
        
    
    elif daily_weather_code[j] == 45:
        tiempo_actual[j]= 'Fog'
        icono[j] = "cloudy"
        
    elif daily_weather_code[j] == 48:
            tiempo_actual[j]= 'Depositing rime fog'
            icono[j] = "cloudy"


    elif daily_weather_code[j] == 51:
        tiempo_actual[j]= 'Drizzle: Light'
        icono[j] = "rain"


    elif daily_weather_code[j] == 53:
        tiempo_actual[j]= 'Drizzle: moderate'
        icono[j] = "rain"
       

    elif daily_weather_code[j] == 55:
        tiempo_actual[j]= 'Drizzle: dense instensity'
        icono[j] = "rain"
            
    elif daily_weather_code[j] == 56:
        tiempo_actual[j]= 'Freezing Drizzle: light'
        icono[j] = "rain"
        

    elif daily_weather_code[j] == 57 :
        tiempo_actual[j]= 'Freezing Drizzle: dense intensity'
        icono[j] = "rain"
        

    elif daily_weather_code[j] == 61:
        tiempo_actual[j]= 'Rain: Slight'
        icono[j] = "rain"
    

    elif daily_weather_code[j] == 63:
        tiempo_actual[j]= 'Rain: moderate'
        icono[j] = "rain"


    elif daily_weather_code[j] == 65:
        tiempo_actual[j]= 'Rain: heavy intensity'
        icono[j] = "rain"
        
    elif daily_weather_code[j] == 66:
        tiempo_actual[j]= 'Freezing Rain: Light'
        icono[j] = "rain"
        

    elif daily_weather_code[j] == 67:
        tiempo_actual[j]= 'Freezing Rain: heavy intensity'
        icono[j] = "rain"

    elif daily_weather_code[j] == 71:
        tiempo_actual[j]= 'Snow Fall: slight'
        icono[j] = "snow"


    elif daily_weather_code[j] == 73:
        tiempo_actual[j]= 'Snow Fall: moderate'
        icono[j] = "snow"

    elif daily_weather_code[j] == 75:
        tiempo_actual[j]= 'Snow Fall: heavy intensity'
        icono[j] = "snow"


    elif daily_weather_code[j] == 77:
        tiempo_actual[j]= 'Snow grains'    
        icono[j] = "snow"
        

    elif daily_weather_code[j] == 80:
        tiempo_actual[j]= 'Rain showers: slight'
        icono[j] = "rain"
        

    elif daily_weather_code[j] == 81:
        tiempo_actual[j]= 'Rain showers: moderate'
        icono[j] = "rain"
       

    elif daily_weather_code[j] == 82:
        tiempo_actual[j]= 'Rain showers: violent'
        icono[j] = "rain"
        

    elif daily_weather_code[j] == 85:
        tiempo_actual[j]= 'Snow showers: slight'
        icono[j] = "snow"
       

    elif daily_weather_code[j] == 86:
        tiempo_actual[j]= 'Snow showers: heavy'
        icono[j] = "snow"
        
            
    elif daily_weather_code[j] == 95:
        tiempo_actual[j]= 'Thunderstorm'
        icono[j] = "rain"
        
            
    elif daily_weather_code[j] == 96:
        tiempo_actual[j]= 'Thunderstorm'
        icono[j] = "rain"
      
        
    elif daily_weather_code[j] == 99:
        tiempo_actual[j]= 'Thunderstorm'
        icono[j] = "rain"
        
            
print(tiempo_actual)
print(icono)
# Aca vemos los iconitos 



@app.route("/weather")
def weather():
    return render_template("weather.html", current_temperature_2m = int(current_temperature_2m), day_list = day_list, current_relative_humidity_2m = current_relative_humidity_2m ,current_wind_speed_10m= current_wind_speed_10m , dt=dt, AAAA = AAAA, MM = MM, DD= DD, current_precipitation = current_precipitation, temp_dia1=temp_dia1, temp_dia2=temp_dia2,temp_dia3=temp_dia3,temp_dia4=temp_dia4, tiempo_actual = tiempo_actual, icono=icono)



# Move db.create_all() inside the application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)