from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from datetime import datetime, timedelta
import os
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

cooldown_ips = {}

class AddressForm(FlaskForm):
    address = StringField('Wallet Address', validators=[DataRequired(), Regexp('^celestia', message='Address must start with "celestia"')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    ip = request.remote_addr
    remaining_time = None
    if ip in cooldown_ips and datetime.now() < cooldown_ips[ip]:
        remaining_time = cooldown_ips[ip] - datetime.now()
    if form.validate_on_submit():
        if remaining_time is None:
            walletto = form.address.data
            result = send_celestia_tokens(walletto)
            if result:
                flash(f'Tokens sent successfully! Tx hash: {result}', 'success')
                cooldown_ips[ip] = datetime.now() + timedelta(hours=24)
            else:
                flash('An error occurred while sending tokens.', 'error')
        else:
            flash(f'You must wait {remaining_time} before requesting tokens again.', 'error')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, remaining_time=remaining_time)

def send_celestia_tokens(walletto):
    command = f'celestia-appd tx bank send wallet {walletto} --chain-id blockspacerace-0 100000utia --gas-prices 0.1utia --gas-adjustment 1.5 --gas auto -y --keyring-backend=test --node http://3.145.65.141:26657/'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        tx_hash = extract_tx_hash(process.stdout)
        return tx_hash
    else:
        return None

def extract_tx_hash(stdout):
    for line in stdout.split('\n'):
        if 'txhash' in line:
            return line.split()[-1]
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
