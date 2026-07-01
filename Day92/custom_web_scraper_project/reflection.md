# Reflection

For this project, I approached the task by choosing a website that was safe and appropriate for web scraping practice. Instead of using a large commercial website with complicated JavaScript or strict scraping rules, I used Books to Scrape because it is designed for scraping projects.

The easiest part was deciding what data should go into the CSV file. A book listing naturally has useful fields like title, price, rating, availability, and links. These fields also make the final CSV easy to understand.

The harder part was making the scraper reliable. I had to think about pagination, missing HTML elements, relative URLs, request errors, and how to save clean data into a CSV file. I also added a delay between requests so the scraper behaves more politely.

My biggest learning was that web scraping is not just about grabbing text from a page. A good scraper should handle errors, clean the data, respect the website, and create output that someone can actually use.

If I were to improve this project later, I would add charts to summarize the results, such as average price by rating or number of books in each category. I could also add more advanced filtering so the user can scrape only books within a certain price range or rating.
