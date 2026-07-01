from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY_HERE'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL(require_tld= True)])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[("☕" * i) if i > 0 else ("✘") for i in range(6)], validators=[DataRequired()])
    wifi_rating = SelectField('WIFI Rating', choices=[("💪" * i) if i > 0 else ("✘") for i in range(6)], validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Rating', choices=[("🔌" * i) if i > 0 else ("✘") for i in range(6)], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_row = f"\n{form.cafe.data}," \
                  f"{form.location.data}," \
                  f"{form.open_time.data}," \
                  f"{form.closing_time.data}," \
                  f"{form.coffee_rating.data}," \
                  f"{form.wifi_rating.data}," \
                  f"{form.power_outlet_rating.data}"

        with open('cafe-data.csv', mode="a", encoding='utf-8') as csv_file:
            csv_file.write(new_row)

        return redirect(url_for('cafes'))  # Send user to the list to see their new cafe!
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
