import datetime
import requests

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    # getting current date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Displaying a form to the user to choose base and target currencies
    return render_template("index.html", date=date)


@app.route('/show', methods=['POST'])
def show():
    # Getting date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Getting base and target currency from user as provided in the form
    base = request.form.get("base-currency")
    target = request.form.get("target-currency")

    # Getting currency exchange rates from fixer.io using base and target currencies
    # provided by the user.
    res = requests.get(f"http://data.fixer.io/api/latest?access_key=b2629cd82138d62e6a275755508257f7&base={base}&symbols={target}&format=1")

    # Making sure the request is successful
    if res.status_code != 200:
        raise Exception("Error: API request unsuccessful")

    # Jsonifying the data returned
    data = res.json()

    # Getting exchange rate of the target currency
    rate = data["rates"][f"{target}"]

    # Displaying the conversion rate to the user
    return render_template("success.html", rate=rate, date=date, target=target)


if __name__ == '__main__':
    app.run()
