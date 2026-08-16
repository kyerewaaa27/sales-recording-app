from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# This list holds all sales for the day (in memory - resets when server restarts)
sales = []

@app.route("/")
def home():
    return open("index.html", encoding="utf-8").read()

@app.route("/api/sale", methods=["POST"])
def add_sale():
    data = request.get_json()
    item = data.get("item")
    price = float(data.get("price"))
    quantity = int(data.get("quantity"))

    sale = {
        "item": item,
        "price": price,
        "quantity": quantity,
        "total": price * quantity,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    sales.append(sale)
    return jsonify({"status": "ok", "sale": sale})

@app.route("/api/summary", methods=["GET"])
def summary():
    total_sales = sum(s["total"] for s in sales)
    total_units = sum(s["quantity"] for s in sales)
    num_transactions = len(sales)

    best_item = None
    if sales:
        item_totals = {}
        for s in sales:
            item_totals[s["item"]] = item_totals.get(s["item"], 0) + s["quantity"]
        best_item = max(item_totals, key=item_totals.get)

    return jsonify({
        "total_sales": total_sales,
        "num_transactions": num_transactions,
        "total_units": total_units,
        "best_item": best_item
    })

@app.route("/api/transactions", methods=["GET"])
def transactions():
    return jsonify(sales)

@app.route("/api/reset", methods=["POST"])
def reset():
    sales.clear()
    return jsonify({"status": "reset done"})

@app.route("/api/report", methods=["GET"])
def report():
    rows = "".join(
        f"<tr><td>{s['time']}</td><td>{s['item']}</td><td>{s['price']}</td><td>{s['quantity']}</td><td>{s['total']}</td></tr>"
        for s in sales
    )
    html = f"""
    <html><body>
    <h2>Daily Sales Report</h2>
    <table border="1">
    <tr><th>Time</th><th>Item</th><th>Price</th><th>Qty</th><th>Total</th></tr>
    {rows}
    </table>
    <p>Total Sales: {sum(s['total'] for s in sales)}</p>
    </body></html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)