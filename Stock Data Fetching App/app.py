from flask import Flask, request, render_template, redirect, url_for
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        enctoken = request.form['enctoken']
        token = request.form['token']
        sdt = datetime.strptime(request.form['sdt'], '%Y-%m-%d')
        edt = datetime.strptime(request.form['edt'], '%Y-%m-%d')

        header = {
            "Authorization": f"enctoken {enctoken}"
        }

        url = f"https://kite.zerodha.com/oms/instruments/historical/{token}/week"
        param = {
            "oi": 1,
            "from": sdt.strftime('%Y-%m-%d'),
            "to": edt.strftime('%Y-%m-%d')
        }

        session = requests.session()
        response = session.get(url, params=param, headers=header)

        if response.status_code == 200:
            data = response.json()["data"]["candles"]
            if data:
                # Determine the number of columns dynamically
                num_columns = len(data[0])
                columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'oi'][:num_columns]
                df = pd.DataFrame(data, columns=columns)
                table = df.to_html(classes='table table-striped', index=False)
                return render_template('index.html', table=table)
            else:
                return render_template('index.html', error="No data available")
        else:
            error = response.json().get('message', 'Failed to fetch data')
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
