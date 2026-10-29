from flask import Flask, request, render_template_string
import random, string
from datetime import datetime

app = Flask(__name__)

# ---- Static train data (never changes) ----
TRAINS = [
    {"id": "12951", "name": "Rajdhani Express", "from": "Delhi",   "to": "Mumbai",  "depart": "16:25", "arrive": "08:15", "price": 2450},
    {"id": "12002", "name": "Shatabdi Express", "from": "Delhi",   "to": "Bhopal",  "depart": "06:00", "arrive": "14:00", "price": 1200},
    {"id": "12627", "name": "Karnataka Express","from": "Bangalore","to": "Delhi",  "depart": "19:20", "arrive": "05:30", "price": 1800},
    {"id": "12723", "name": "Telangana Express","from": "Hyderabad","to": "Delhi",  "depart": "06:25", "arrive": "07:40", "price": 1650},
    {"id": "12301", "name": "Howrah Rajdhani",  "from": "Kolkata", "to": "Delhi",  "depart": "16:55", "arrive": "10:00", "price": 2200},
]

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Train Ticket Booking</title>
  <style>
    body { font-family: Arial, sans-serif; background: #eef2f7; margin: 0; padding: 20px; }
    .box { max-width: 800px; margin: auto; background: #fff; padding: 25px;
           border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { color: #0d47a1; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th { background: #0d47a1; color: #fff; padding: 10px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #ddd; }
    button { background: #0d47a1; color: #fff; padding: 8px 16px;
             border: none; border-radius: 5px; cursor: pointer; }
    button:hover { background: #1565c0; }
    input, select { padding: 6px; margin: 5px 0; width: 100%;
                    border: 1px solid #ccc; border-radius: 4px; }
    .ticket { border: 2px dashed #0d47a1; padding: 20px; border-radius: 8px;
              margin-top: 15px; background: #f1f8ff; }
    .ticket p { margin: 6px 0; font-size: 16px; }
    a.btn { display: inline-block; background: #0d47a1; color: #fff;
            padding: 8px 14px; border-radius: 5px; text-decoration: none; margin-top: 15px; }
  </style>
</head>
<body>
  <div class="box">
    {{ content|safe }}
  </div>
</body>
</html>
"""

HOME = """
<h1>🚆 Static Train Ticket Booking</h1>
<p>Choose a train below and click <b>Book</b>.</p>
<table>
  <tr>
    <th>Train ID</th><th>Name</th><th>From</th><th>To</th>
    <th>Depart</th><th>Arrive</th><th>Price</th><th>Action</th>
  </tr>
  {% for t in trains %}
  <tr>
    <td>{{ t.id }}</td>
    <td>{{ t.name }}</td>
    <td>{{ t['from'] }}</td>
    <td>{{ t['to'] }}</td>
    <td>{{ t.depart }}</td>
    <td>{{ t.arrive }}</td>
    <td>₹{{ t.price }}</td>
    <td><a class="btn" href="/book/{{ t.id }}">Book</a></td>
  </tr>
  {% endfor %}
</table>
"""

BOOK_FORM = """
<h1>🎫 Book – {{ train.name }}</h1>
<p><b>Route:</b> {{ train['from'] }} → {{ train['to'] }} |
   <b>Price:</b> ₹{{ train.price }}</p>

<form method="post">
  <label>Passenger Name</label>
  <input name="name" required>

  <label>Age</label>
  <input name="age" type="number" min="1" max="120" required>

  <label>Gender</label>
  <select name="gender">
    <option>Male</option><option>Female</option><option>Other</option>
  </select>

  <label>Number of Seats</label>
  <input name="seats" type="number" min="1" max="10" value="1" required>

  <br><br>
  <button type="submit">Confirm Booking</button>
</form>

<a href="/">← Back</a>
"""

TICKET = """
<h1>✅ Ticket Confirmed</h1>
<div class="ticket">
  <p><b>PNR:</b> {{ pnr }}</p>
  <p><b>Passenger:</b> {{ name }} ({{ age }}, {{ gender }})</p>
  <p><b>Train:</b> {{ train.name }} ({{ train.id }})</p>
  <p><b>Route:</b> {{ train['from'] }} → {{ train['to'] }}</p>
  <p><b>Departure:</b> {{ train.depart }} | <b>Arrival:</b> {{ train.arrive }}</p>
  <p><b>Seats:</b> {{ seats }}</p>
  <p><b>Total Fare:</b> ₹{{ total }}</p>
  <p><b>Booked On:</b> {{ time }}</p>
</div>
<a class="btn" href="/">Book Another Ticket</a>
"""


def find_train(tid):
    return next((t for t in TRAINS if t["id"] == tid), None)


def make_pnr():
    return "PNR" + "".join(random.choices(string.digits, k=8))


@app.route("/")
def home():
    body = render_template_string(HOME, trains=TRAINS)
    return render_template_string(PAGE, content=body)


@app.route("/book/<train_id>", methods=["GET", "POST"])
def book(train_id):
    train = find_train(train_id)
    if not train:
        return render_template_string(PAGE, content="<h2>Train not found.</h2><a href='/'>Back</a>")

    if request.method == "POST":
        name    = request.form["name"].strip()
        age     = request.form["age"]
        gender  = request.form["gender"]
        seats   = int(request.form["seats"])
        total   = seats * train["price"]
        pnr     = make_pnr()
        time    = datetime.now().strftime("%d-%b-%Y %H:%M")

        body = render_template_string(
            TICKET,
            pnr=pnr, name=name, age=age, gender=gender,
            seats=seats, total=total, time=time, train=train,
        )
        return render_template_string(PAGE, content=body)

    body = render_template_string(BOOK_FORM, train=train)
    return render_template_string(PAGE, content=body)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
