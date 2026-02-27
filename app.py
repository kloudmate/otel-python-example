"""
Simple Hello World Flask application with OpenTelemetry instrumentation.
This demonstrates both auto-instrumentation and custom spans.
"""
import time
import random
import uuid
from flask import Flask, jsonify
from opentelemetry import trace

# Get a tracer for creating custom spans
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Simple hello world endpoint."""
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success'
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'otel-python-example'
    })


@app.route('/process')
def process():
    """
    Endpoint that demonstrates custom span creation.
    Simulates some processing work with custom spans.
    """
    with tracer.start_as_current_span("process_request") as span:
        # Add some attributes to the span
        span.set_attribute("request.type", "process")
        span.set_attribute("user.operation", "data_processing")
        
        # Simulate some work with nested spans
        result = do_work()
        
        span.set_attribute("result.count", result['processed_items'])
        
        return jsonify(result)


def do_work():
    """
    Worker function that demonstrates custom span creation.
    This simulates processing work with nested spans.
    """
    with tracer.start_as_current_span("do_work") as span:
        span.set_attribute("work.type", "data_processing")
        
        # Simulate step 1: Fetch data
        data = fetch_data()
        span.set_attribute("data.fetched", len(data))
        
        # Simulate step 2: Process data
        processed = process_data(data)
        span.set_attribute("data.processed", len(processed))
        
        return {
            'status': 'completed',
            'processed_items': len(processed),
            'original_items': len(data)
        }


def fetch_data():
    """
    Simulates fetching data with a custom span.
    """
    with tracer.start_as_current_span("fetch_data") as span:
        # Simulate database or API call
        time.sleep(0.1)
        data = ['item1', 'item2', 'item3', 'item4', 'item5']
        span.set_attribute("data.source", "simulated_database")
        span.set_attribute("data.count", len(data))
        return data


def process_data(data):
    """
    Simulates processing data with a custom span.
    """
    with tracer.start_as_current_span("process_data") as span:
        # Simulate some processing work
        time.sleep(0.15)
        processed = [item.upper() for item in data]
        span.set_attribute("processing.type", "uppercase_transformation")
        return processed


# --- K-Commerce Scenario ---

def check_inventory(item_ids):
    with tracer.start_as_current_span("inventory.check") as span:
        span.set_attribute("inventory.items_count", len(item_ids))
        span.set_attribute("inventory.warehouse", "US-East-1")
        span.set_attribute("inventory.items", str(item_ids))
        
        time.sleep(random.uniform(0.1, 0.3))
        
        # 10% chance of out-of-stock
        if random.random() < 0.1:
            span.add_event("inventory.out_of_stock", {"item.id": item_ids[0]})
            span.set_status(trace.Status(trace.StatusCode.ERROR, f"Item {item_ids[0]} out of stock"))
            raise ValueError(f"Item {item_ids[0]} is out of stock!")
            
        span.set_attribute("inventory.status", "available")
        return True

def process_payment(order_amount, user_id):
    with tracer.start_as_current_span("payment.process") as span:
        span.set_attribute("payment.amount", order_amount)
        span.set_attribute("payment.currency", "USD")
        span.set_attribute("payment.method", "credit_card")
        span.set_attribute("payment.gateway", "stripe")
        span.set_attribute("user.id", user_id)
        
        span.add_event("payment.gateway.initiated")
        time.sleep(random.uniform(0.3, 0.8))
        
        # 5% chance of payment failure
        if random.random() < 0.05:
            span.add_event("payment.gateway.declined")
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Payment declined by gateway"))
            raise RuntimeError("Payment declined by bank")
            
        span.add_event("payment.gateway.success", {
            "transaction.id": f"txn_{random.randint(10000, 99999)}"
        })
        return True

def schedule_shipping(order_id):
    with tracer.start_as_current_span("logistics.schedule") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("logistics.provider", "fedex")
        span.set_attribute("logistics.shipping_method", "express")
        
        time.sleep(random.uniform(0.1, 0.4))
        
        tracking_number = f"1Z999{random.randint(1000000, 9999999)}"
        span.set_attribute("logistics.tracking_number", tracking_number)
        return tracking_number

from flask import request

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    """
    Complex k-commerce checkout endpoint.
    Expects POST, but handles GET with mock data for easy testing.
    """
    if request.method == 'POST':
        order_data = request.json or {}
    else:
        # Mock data for quick GET testing via browser or simple curl
        order_data = {
            "order_id": f"ORD-{uuid.uuid4().hex[:6].upper()}",
            "user_id": f"USR-{random.randint(100, 999)}",
            "amount": round(random.uniform(10.0, 500.0), 2),
            "items": [f"item_{random.randint(1, 100)}", f"item_{random.randint(1, 100)}"]
        }
        
    order_id = order_data.get("order_id", "UNKNOWN-ORDER")
    
    # We wrap the business logic in an explicit span that attaches to the Flask auto-instrumented span
    with tracer.start_as_current_span("order.process") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("user.id", order_data.get("user_id", "unknown"))
        span.set_attribute("order.total_value", order_data.get("amount", 0.0))
        span.add_event("order.started")
        
        try:
            check_inventory(order_data.get("items", []))
            process_payment(order_data.get("amount", 0.0), order_data.get("user_id", "unknown"))
            tracking = schedule_shipping(order_id)
            
            span.set_attribute("order.status", "completed")
            span.set_status(trace.Status(trace.StatusCode.OK))
            span.add_event("order.completed", {"tracking.number": tracking})
            
            return jsonify({
                "status": "success",
                "order_id": order_id,
                "tracking_number": tracking,
                "message": "Order processed successfully."
            })
            
        except ValueError as e:
            span.record_exception(e)
            span.set_attribute("order.status", "failed_inventory")
            return jsonify({"status": "error", "error": str(e)}), 400
            
        except RuntimeError as e:
            span.record_exception(e)
            span.set_attribute("order.status", "failed_payment")
            return jsonify({"status": "error", "error": str(e)}), 402
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.set_attribute("order.status", "failed_unknown")
            return jsonify({"status": "error", "error": "Internal server error"}), 500


if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
