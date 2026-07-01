import smtplib
from flask import Flask, render_template, request, flash

app = Flask(__name__)

# This is where you store your project data
PROJECTS = [
    {
        'title': 'AI Movie Success Predictor',
        'description': 'A Machine Learning model built in Google Colab to predict if a movie will lose money.',
        'tech': ['Python', 'Pandas', 'Scikit-Learn'],
        'link': '#'
    },
    {
        'title': 'Real-Time Chat App',
        'description': 'A full-stack web application with WebSockets for instant messaging.',
        'tech': ['Flask', 'SocketIO', 'SQLAlchemy'],
        'link': '#'
    }
]

@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS)


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Logic to send email
        try:
            # For Gmail, you'd use an 'App Password', not your regular login!
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            # server.login("your_email@gmail.com", "your_app_password")

            subject = f"New Portfolio Message from {name}"
            body = f"From: {email}\n\n{message}"
            # server.sendmail("your_email@gmail.com", "recipient_email@gmail.com", f"Subject: {subject}\n\n{body}")

            print(f"Success! Message from {name} received.")  # For testing locally
            return "<h1>Message Sent! I'll get back to you soon.</h1>"

        except Exception as e:
            print(f"Error: {e}")
            return "<h1>Something went wrong. Please try again.</h1>"

if __name__ == '__main__':
    app.run(debug=True)