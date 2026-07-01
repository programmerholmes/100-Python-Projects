# 100 Python Projects

One hundred days of Python — a project-per-day journey covering everything from
basic syntax to games, GUIs, web scraping, APIs, automation, Flask web apps, data science and machine learning.

Each `DayN/` folder is a self-contained project. Highlights:

| Days | Theme |
|---|---|
| 1–15 | Python fundamentals — logic, functions, dictionaries, OOP basics |
| 16–23 | OOP & games — Snake, Pong, Turtle Crossing (turtle graphics) |
| 24–31 | Files & GUIs — mail merge, flash cards, password manager (tkinter) |
| 32–40 | APIs & automation — email (SMTP), ISS tracker, weather/rain alerts, stock news, habit tracking, flight deals |
| 41–58 | Web development & scraping — HTML/CSS, Beautiful Soup, Selenium bots (Spotify playlists, price alerts, social automation) |
| 59–69 | Flask — blogs, forms, authentication, REST APIs, SQLAlchemy |
| 71–83 | Data science & capstones — pandas, matplotlib, portfolio projects |
| 84–100 | Advanced projects — image watermarking, typing test, games, GUI apps, data analysis & regression |

## Running the projects

Most projects need only Python 3.11+ and a `pip install` of the imports at the
top of each file (`requests`, `flask`, `selenium`, `beautifulsoup4`, `pandas`,
`spotipy`, `twilio`, etc.).

```bash
cd Day35
pip install requests twilio
python rain_alert.py
```

## API keys & credentials

**No real credentials are included in this repository.** Anywhere a project
needs a key, token, email, or password you will find a placeholder such as
`YOUR_OPENWEATHERMAP_API_KEY`, `your_email@example.com`, or `YOUR_PASSWORD` —
swap in your own values. Free keys/accounts for the services used:

- [OpenWeatherMap](https://openweathermap.org/api) — weather (Day 35)
- [Twilio](https://www.twilio.com/) — SMS alerts (Days 35–36)
- [Alpha Vantage](https://www.alphavantage.co/) & [NewsAPI](https://newsapi.org/) — stock news (Day 36)
- [Pixela](https://pixe.la/) — habit tracking (Day 37)
- [Nutritionix](https://www.nutritionix.com/business/api) & [Sheety](https://sheety.co/) — exercise tracking (Day 38)
- Flight search APIs & [Sheety](https://sheety.co/) — flight deals (Days 39–40)
- [Spotify for Developers](https://developer.spotify.com/dashboard) — playlist automation (Day 46)
- Gmail — use an [app password](https://support.google.com/accounts/answer/185833) for any SMTP project (Days 32, 47, 60+)

For Flask projects, set your own `SECRET_KEY` where you see
`YOUR_SECRET_KEY_HERE`. Databases (`*.db`) that the apps need are created
automatically on first run.

## Credits

Projects built while following Angela Yu's
[100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/).
Course starter files remain the property of the course author.
