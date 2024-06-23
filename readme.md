# Deck AI Crawler POC

This project is a Proof of Concept (POC) for the Deck AI Crawler.

## Prerequisites

Make sure you have the following installed on your system:

- Node.js (with npm)
- Python (with pip)

## Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/VictorHadziristic/Deck.git
   ```

2. Install Node Dependencies:

   ```sh
   npm install
   ```

3. Install Python Dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Install Chrome Canary (From the following page)

    ```sh
    https://www.google.com/intl/en_ca/chrome/canary/
    ```

5. (OPTIONAL) Change path to Chrome Canary and Chrome User in screenshot.js
    ```javascript
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary', //MODIFY AS NEEDED
        userDataDir: './Default', //REPLACE WITH YOUR OWN CHROME USER DATA DIRECTORY
    });
    ```

6. Change the url of the page you'd like to scrape
    ```python
    webpage = capture_webpage("https://doctors.cpso.on.ca/DoctorDetails/Gillian-Mary-Brakel/0181571-76088") ## supply your url here.
    ```

7. Run the scraper
    ```sh
    python scrape.py
    ```