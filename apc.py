from flask import Flask, jsonify
import subprocess
import re

app = Flask(__name__)

@app.route('/apcaccess', methods=['GET'])
def get_apcaccess_output():
    try:
        output = subprocess.check_output(['apcaccess'], universal_newlines=True)
        data = parse_apcaccess_output(output)
        return jsonify(data), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

def parse_apcaccess_output(output):
    desired_attributes = ['STATUS', 'BCHARGE', 'TIMELEFT', 'BATTV', 'NOMBATTV']
    data = {}
    for line in output.split('\n'):
        match = re.match(r'^(\w+)\s+:\s+(.+)$', line)
        if match and match.group(1) in desired_attributes:
            data[match.group(1)] = match.group(2)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
