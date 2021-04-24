#-*-coding: utf-8 -*-
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

def calculation(initial_amount,top_up_amount, return_ratio_annual, duration_m):
    if return_ratio_annual == 0:
        topup_future_value = top_up_amount * duration_m
    else:
        topup_future_value = ((1 + return_ratio_annual/12) ** duration_m - 1)/(return_ratio_annual/12) * top_up_amount
    initial_amount_future_value = initial_amount * (1 + return_ratio_annual/12) ** duration_m
    future_value = round(initial_amount_future_value + topup_future_value, 0)
    return future_value


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calc():
    return render_template('calculate.html')

@app.route('/result', methods=['GET', 'POST'])
def show_result():
    if request.method == 'GET':
        return render_template('result.html')
    else:
        asset = request.form.get('asset_name')
        initial_amount = float(request.form.get('initial_amount'))
        return_ratio_annual = float(request.form.get('return_ratio'))/100
        top_up_amount = float(request.form.get('top_up_amount'))
        duration_m = int(request.form.get('duration_m'))

        future_value = int(calculation(initial_amount, top_up_amount, return_ratio_annual, duration_m))

        return render_template('result.html', asset=asset, future_value=future_value)

if __name__ == '__main__':
    app.run(debug=True)