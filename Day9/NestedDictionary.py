# Nesting Dictionary into a Dictionary

travel_log = {
     "France": {"cities_visited": ["Paris", "Lille", "Dijon"], "total_visits": 4},
     "Germany": {"cities_visited": ["Berlin", "Hamburg", "Stuttgart"], "total_visits": 1}

}

# Nesting Dictionary into a List

travel_log = [
     {"country": "France",
     "cities_visited": ["Paris", "Lille", "Dijon"],
      "total_visits": 4
      },

     {"Country": "Germany",
      "cities_visited": ["Berlin", "Hamburg", "Stuttgart"],
      "total_visits": 1
     }
]

print(travel_log["France"])
print(travel_log["Germany"])