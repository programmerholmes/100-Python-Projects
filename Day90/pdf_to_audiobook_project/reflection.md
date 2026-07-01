# Reflection

For this project, I approached the task by breaking it into three main parts: reading the PDF, extracting the text, and converting that text into speech. The first part was understanding that a PDF is not just a normal text file. I needed a library that could read the pages and extract the text from each page.

The easiest part was designing the basic workflow: choose a PDF, choose where to save the audiobook, then press a convert button. The harder part was making the program handle problems properly, such as missing files, scanned PDFs with no readable text, or text-to-speech errors.

My biggest learning was that building a useful app is not only about the main feature. It also needs error handling, clear instructions, and a simple interface so the user understands what is happening. I also learned that online and offline text-to-speech have different tradeoffs. Online speech can sound better, but it needs internet. Offline speech is more reliable because it does not need internet, but the voice can sound more robotic.

If I did this project again, I would improve it by adding OCR support for scanned PDFs and maybe adding more voice options. I would also add a progress bar that shows exactly how much of the PDF has been converted.
