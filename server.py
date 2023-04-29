from flask import Flask, request
import csv
import time

app = Flask(__name__)
filename = "http.csv"


# Define the route to handle incoming JSON messages
# curl -X POST -H "Content-Type: application/json" -d '{"name": "John", "timestamp": "2023-04-13T10:30:00"}' 
# http://localhost:5000/receive
@app.route("/receive", methods=["POST"])
def receive():
    # Parse the JSON request data
    data = request.get_json()

    # Extract the fields from the JSON data
    name = data["name"]
    timestamp = data["timestamp"]

    # Write the data to a CSV file
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, timestamp])
    return "Message received and processed."

# curl -X GET http://localhost:5000/time
@app.route("/time", methods=["GET"])
def send():
    return str(time.time()) + "\n"

# curl -X PUT -H "Content-Type: application/json" -d '{"filename": "flyfile.csv"}' http://localhost:5000/file
@app.route("/file", methods=["PUT"])
def file():
    data = request.get_json()
    filename = data["filename"]
    
    with open(filename, "w", newline="") as csvfile:
        return "File created." + "\n"


if __name__ == "__main__":
    app.run(debug=True)
