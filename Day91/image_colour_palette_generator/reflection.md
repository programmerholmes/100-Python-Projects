# Reflection

For this project, I approached the assignment by breaking it into two main parts: the web application and the image-processing logic. First, I created a Flask app that allows the user to upload an image. Then I wrote a separate Python module to open the image, convert it into RGB values, and calculate the most common colours.

The easiest part was building the basic Flask routes and the upload form because it followed the same pattern as other web apps. The harder part was deciding how to calculate the "top colours" in a useful way. If the program counts every exact pixel colour, the results can be messy because photos often have thousands of slightly different shades. I solved this by grouping similar RGB values into buckets before counting them.

My biggest learning was that image processing is not just about getting data from an image. It is also about making that data useful for the user. A raw list of exact pixel colours is technically correct, but a grouped palette is better for design work.

If I tackled this project again, I would add more advanced features such as letting the user choose how many colours to generate, exporting the palette as a CSS file, and deleting old uploaded images automatically.
