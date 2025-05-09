from flask import Flask, request, jsonify
import geocoder
import datetime

app = Flask(__name__)
LOCATION_FILE = "locations.txt"

def get_address(lat, lng):
    try:
        g = geocoder.osm([lat, lng], method='reverse')
        return g.address if g.ok else "Адрес не найден"
    except:
        return "Ошибка получения адреса"

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.get_json()
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({"error": "Неверный формат данных"}), 400
    
    lat, lng = data['lat'], data['lng']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    address = get_address(lat, lng)
    
    # Сохраняем в файл
    with open(LOCATION_FILE, "a") as f:
        f.write(f"{timestamp} | Широта: {lat}, Долгота: {lng} | Адрес: {address}\n")
    
    return jsonify({"status": "success"}), 200

@app.route('/get_location', methods=['GET'])
def get_location():
    try:
        with open(LOCATION_FILE, "r") as f:
            lines = f.readlines()
            if not lines:
                return jsonify({"error": "Нет данных"}), 404
            last_line = lines[-1]
            parts = last_line.split(" | ")
            timestamp, coords, address = parts[0], parts[1], parts[2]
            lat = float(coords.split(": ")[1].split(",")[0])
            lng = float(coords.split(": ")[2])
            return jsonify({
                "lat": lat,
                "lng": lng,
                "address": address,
                "timestamp": timestamp
            }), 200
    except:
        return jsonify({"error": "Ошибка чтения данных"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)