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

# Homepage - Train list
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Train Booking System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(to right, #83a4d4, #b6fbff);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 40px;
            }
            .table {
                background-color: white;
                border-radius: 10px;
                overflow: hidden;
            }
            h1 {
                margin-bottom: 30px;
                color: #004085;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1>🚆 Available Trains</h1>
            <table class="table table-hover shadow">
                <thead class="table-primary">
                    <tr>
                        <th>Train Name</th>
                        <th>From</th>
                        <th>To</th>
                        <th>Time</th>
                        <th>Book</th>
                    </tr>
                </thead>
                <tbody>
                    {% for train in trains %}
                    <tr>
                        <td>{{ train.name }}</td>
                        <td>{{ train.from }}</td>
                        <td>{{ train.to }}</td>
                        <td>{{ train.time }}</td>
                        <td><a class="btn btn-success btn-sm" href="{{ url_for('book', train_id=train.id) }}">Book Now</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, trains=trains)


# Booking Page
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
    <html lang="en">
    <head>
        <title>Book Ticket</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(to right, #ffecd2, #fcb69f);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 60px;
            }
            .form-box {
                background-color: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            h2 {
                color: #6f42c1;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <div class="form-box mx-auto" style="max-width: 400px;">
                <h2>Book Ticket for {{ train.name }}</h2>
                <form method="POST" class="mt-3">
                    <div class="mb-3 text-start">
                        <label class="form-label">Name:</label>
                        <input type="text" class="form-control" name="name" required>
                    </div>
                    <div class="mb-3 text-start">
                        <label class="form-label">Age:</label>
                        <input type="number" class="form-control" name="age" required>
                    </div>
                    <div class="mb-3 text-start">
                        <label class="form-label">Seats:</label>
                        <input type="number" class="form-control" name="seats" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Confirm Booking</button>
                </form>
                <a href="/" class="btn btn-link mt-3">⬅ Back to Trains</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, train=train)


# Confirmation Page
@app.route('/confirm')
def confirm():
    name = request.args.get('name')
    booking = next((b for b in bookings if b["name"] == name), None)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Booking Confirmation</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(to right, #d4fc79, #96e6a1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding-top: 60px;
            }
            .confirm-box {
                background-color: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                max-width: 500px;
                margin: auto;
            }
            h1 {
                color: #155724;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <div class="confirm-box">
                {% if booking %}
                    <h1>✅ Booking Confirmed!</h1>
                    <hr>
                    <p><strong>Name:</strong> {{ booking.name }}</p>
                    <p><strong>Train:</strong> {{ booking.train.name }}</p>
                    <p><strong>From:</strong> {{ booking.train.from }}</p>
                    <p><strong>To:</strong> {{ booking.train.to }}</p>
                    <p><strong>Seats:</strong> {{ booking.seats }}</p>
                {% else %}
                    <h2>No booking found.</h2>
                {% endif %}
                <a href="/" class="btn btn-success mt-3">Book Another Ticket</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, booking=booking)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
