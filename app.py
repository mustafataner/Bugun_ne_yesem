from flask import Flask, render_template, request, jsonify
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)

data = pd.read_csv("final_diyarbakır_data_unique(1).csv")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    user_location = request.json.get('user_location')
    max_distance_km = request.json.get('max_distance_km')

    if user_location:
        user_lat, user_lon = user_location

        data['distance'] = data.apply(
            lambda row: geodesic((user_lat, user_lon), (row['latitude'], row['longitude'])).kilometers, axis=1)
        suitable_restaurants = data[data['distance'] <= max_distance_km]

        if not suitable_restaurants.empty:
            random_restaurant = suitable_restaurants.sample(1).iloc[0]
            return jsonify({
                'success': True,
                'name': random_restaurant['name'],
                'latitude': random_restaurant['latitude'],
                'longitude': random_restaurant['longitude']
            })
        else:
            return jsonify({'success': False})

    return jsonify({'success': False})


if __name__ == "__main__":
    app.run(debug=False)
