# Reflection

I approached this project by first checking the structure of the SQLite database. The database already had useful fields such as cafe name, location, image URL, map URL, WiFi, sockets, toilets, seats, and coffee price, so I designed the website around those columns.

The easiest part was displaying the cafe information once the database query worked. The homepage uses cards so each cafe is easy to read, and the search and filters make it easier for users to find a cafe that matches what they need.

The harder part was connecting the forms to the database safely. I had to make sure the app could add, edit, and delete rows without breaking the database. I also handled missing required fields and duplicate cafe names.

My biggest learning was how the same Flask app can serve both normal HTML pages and JSON API responses. The route receives the request, the database returns the data, and the template or API response displays it to the user.

If I tackled this project again, I would add user accounts or an admin-only delete button so that not everyone can remove cafes. I would also improve validation for image links and map URLs.
