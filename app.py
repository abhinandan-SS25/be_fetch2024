from flask import Flask
from flask import request, Response, jsonify
from tinydb import TinyDB, Query, where
from datetime import datetime, timezone

app = Flask(__name__)

# Connecting to local simulated NoSql db
db = TinyDB('./transaction.json') ## keeps track of the current status of the points of the user
table = db.table('transactions') ## table to store all transactions

# We assume a single user and under this, create a generic user_id that will be used to identify transactions related to the user.
user_id = "x01"

# Function to get the balance of a user
#    Returns the balance of the user per payer in dict format
#    If the user does not have a balance record, it returns None
def get_user_balance(user_id):
    User = Query()
    points_data = db.search(User.user_id == user_id)

    balance_per_payer = {}
    if len(points_data) > 0:
        for transaction in points_data:
            payer = transaction.get("payer")
            points = transaction.get("points")
            if payer in balance_per_payer:
                balance_per_payer[payer] += points
            else:
                balance_per_payer[payer] = points
        return balance_per_payer
    else:
        return None

#  Function to add negative points to the user's account
#    points: The points to be added to the user's account
#    payer: The payer from which the points are to be added
def add_negative_points(points, payer):
    User = Query()
    points_data = db.search((User.user_id == user_id) & (User.payer == payer))
    points_data = sorted(points_data, key=lambda x: datetime.fromisoformat(x.get("timestamp"))) ## Sorting transactions by timestamp

    # Gets the balance of the user
    user_balance = get_user_balance(user_id)
    if not user_balance:
        return False
    # If the user does not have enough points for the given payer, return None
    if points > user_balance.get(payer, 0):
        return False
    
    # Removes points from the user's account for the given payer
    for transaction in points_data:
        # If the points have been removed, break the loop
        if points == 0:
            break
        else:
            transaction_points = transaction.get("points")
            # If the transaction points are greater than the points to be removed, remove the points and set points to 0 to break the loop at next iteration
            if transaction_points >= points:
                #Update the points in the db for the transaction
                db.update({"points": transaction_points + points}, (User.user_id == user_id) & (User.timestamp == transaction.get("timestamp")))
                points = 0
            else:
                #Update the points in the db for the transaction
                db.update({"points": 0}, (User.user_id == user_id) & (User.timestamp == transaction.get("timestamp")))
                points -= transaction_points
    return True

@app.route("/add", methods=['POST'])
def add_points():
    try:
        data = request.get_json()
        
        related_user_id = user_id ## uing a generic user_id for this assignment
        payer = data.get("payer", False)
        points = data.get("points", False)
        timestamp = data.get("timestamp", False)

        # Nake sure that all required fields are present in the request body
        if (payer and points and timestamp):
            # If the points are negetive, it essentially means that the user is spending points
            # So, we call the spend_points function to handle the spending of points
            # The logic is very similar to the /spend route, but for only a single payer
            if points < 0:
                if add_negative_points(points, payer):
                    return "", 200
                else:
                    return "Negetive points cannot be added due to lack of points for this payer.", 400

            # insert record of transaction in the db
            db.insert(
                {
                    "user_id": related_user_id,
                    "payer": payer,
                    "points": points,
                    "timestamp": timestamp,
                }
            )
            return "", 200
        else:
            return "Missing required field in request body.", 400
    except Exception as e:
        print(e)
        return "", 500

@app.route("/spend", methods=['POST'])
def spend_points():
    try:
        data = request.get_json()
        points = data.get("points", False)

        if points:
            related_user_id = user_id ## using a generic user_id for this assignment

            # Related balance for the user
            user_balance = get_user_balance(related_user_id)
            if not user_balance:
                return "User not found", 404
            
            # Check if the user has enough points to spend
            if (sum(user_balance.values()) < points):
                return "User doesnt't have enough points to spend.", 400

            User = Query()

            # Related transactions for the user
            points_data = db.search((User.user_id == related_user_id) & (where("points") > 0)) ## transactions with 0 points have already been spent
            points_data = sorted(points_data, key=lambda x: datetime.fromisoformat(x.get("timestamp"))) ## Sorting transactions by timestamp
            
            payer_points = {} ## keeps track of the points spent by each payer
            # spend points from transactions in user account till points are 0
            while points > 0:
                for transaction in points_data:
                    payer = transaction.get("payer")
                    transaction_points = transaction.get("points")
                    if transaction_points > 0:
                        if transaction_points >= points:
                            payer_points[payer] = payer_points.get(payer, 0) - points
                            db.update({"points": transaction_points - points}, (User.user_id == related_user_id) & (User.payer == payer) & (User.timestamp == transaction.get("timestamp")))
                            points = 0
                            break
                        else:
                            payer_points[payer] = payer_points.get(payer, 0) - transaction_points
                            db.update({"points": 0}, (User.user_id == related_user_id) & (User.payer == payer) & (User.timestamp == transaction.get("timestamp")))
                            points -= transaction_points
                            transaction["points"] = 0
                    else:
                        continue

            # Transform the response data to the required format
            reponse_data = []
            for payer, points in payer_points.items():
                reponse_data.append({"payer": payer, "points": points})
            return reponse_data, 200
            
        else:
            return "Missing required field in request body.", 400
    except Exception as e:
        print(e)
        return "", 500
    
@app.route("/balance", methods=['GET'])
def get_balance():
    try:
        related_user_id = user_id ## using a generic user_id for this assignment

        # Get the balance of the user
        user_balance = get_user_balance(related_user_id)

        # If the user does not have a balance record, return 404
        if not user_balance:
            return "User not found", 404

        return jsonify(user_balance), 200

    except Exception as e:
        print(e)
        return "", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)