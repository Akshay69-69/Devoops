from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Dummy train data
trains = [
    {"id": 1, "name": "Chennai Express", "from": "Chennai", "to": "Bangalore", "time": "08:30 AM"},
    {"id": 2, "name": "Rajdhani Express", "from": "Delhi", "to": "Mumbai", "time": "09:00 PM"},
    {"id": 3, "name": "Shatabdi Express", "from": "Kolkata", "to": "Patna", "time": "06:00 AM"}
]

# Temporary booking store
bookings = []

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Train Booking System</title>
    </head>
    <body style="font-family:Arial; text-align:center;">
        <h1>🚆 Available Trains</h1>
        <table border="1" align="center" cellpadding="10">
            <tr>
                <th>Train Name</th>
                <th>From</th>
                <th>To</th>
                <th>Time</th>
                <th>Book</th>
            </tr>
            {% for train in trains %}
            <tr>
                <td>{{ train.name }}</td>
                <td>{{ train.from }}</td>
                <td>{{ train.to }}</td>
                <td>{{ train.time }}</td>
                <td><a href="{{ url_for('book', train_id=train.id) }}">Book Now</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, trains=trains)

@app.route('/book/<int:train_id>', methods=['GET', 'POST'])
def book(train_id):
    train = next((t for t in trains if t["id"] == train_id), None)
    if not train:
        return "Train not found", 404

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        seats = request.form['seats']

        booking = {
            "train": train,
            "name": name,
            "age": age,
            "seats": seats
        }
        bookings.append(booking)
        return redirect(url_for('confirm', name=name))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Book Ticket</title>
    </head>
    <body style="font-family:Arial; text-align:center;">
        <h2>Book Ticket for {{ train.name }}</h2>
        <form method="POST">
            <p><strong>Name:</strong> <input type="text" name="name" required></p>
            <p><strong>Age:</strong> <input type="number" name="age" required></p>
            <p><strong>Seats:</strong> <input type="number" name="seats" required></p>
            <button type="submit">Confirm Booking</button>
        </form>
        <p><a href="/">Back to Trains</a></p>
    </body>
    </html>
    """
    return render_template_string(html, train=train)

@app.route('/confirm')
def confirm():
    name = request.args.get('name')
    booking = next((b for b in bookings if b["name"] == name), None)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking Confirmation</title>
    </head>
    <body style="font-family:Arial; text-align:center;">
        {% if booking %}
            <h1>✅ Booking Confirmed!</h1>
            <p><strong>Name:</strong> {{ booking.name }}</p>
            <p><strong>Train:</strong> {{ booking.train.name }}</p>
            <p><strong>From:</strong> {{ booking.train.from }}</p>
            <p><strong>To:</strong> {{ booking.train.to }}</p>
            <p><strong>Seats:</strong> {{ booking.seats }}</p>
        {% else %}
            <h2>No booking found.</h2>
        {% endif %}
        <p><a href="/">Book Another Ticket</a></p>
    </body>
    </html>
    """
    return render_template_string(html, booking=booking)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
