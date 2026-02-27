import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Simple hello world endpoint."""
    return jsonify({
        'message': 'Hello, World! (Auto-Instrumentation Demo)',
        'status': 'success'
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'otel-python-auto-example'
    })

@app.route('/api/users')
def get_users():
    """
    Simulated endpoint returning users.
    Zero code instrumentation will capture this HTTP request automatically.
    """
    # Simulate DB delay
    time.sleep(0.15)
    return jsonify({
        'users': [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Charlie'}
        ],
        'total': 3
    })

@app.route('/api/computation')
def heavy_computation():
    """
    Simulated heavy computation endpoint.
    Zero code instrumentation will capture the duration automatically.
    """
    # Simulate heavy workload delay
    time.sleep(0.8)
    return jsonify({
        'status': 'success',
        'result': 42
    })

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
