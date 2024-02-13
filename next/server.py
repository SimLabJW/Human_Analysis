from flask import Flask, request, jsonify

app = Flask(__name__)

# 예시용 데이터
shared_data = {}

@app.route('/simulate', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        input_data = request.get_json()
        shared_data.update(input_data)
        return jsonify('')

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(shared_data)

if __name__ == '__main__':
    app.run(port=5000)
