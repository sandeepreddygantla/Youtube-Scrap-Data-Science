# YouTube Scraper Flask Application

## Introduction
This Flask application serves as a YouTube Scraper, allowing users to extract video information from YouTube channels. The information includes video URLs, thumbnails, titles, views, and published times.

## Features
- Web interface for inputting YouTube channel names.
- Scrapes the top 5 videos from the specified YouTube channel.
- Extracts details such as video URL, thumbnail, title, view count, and published time.
- Generates and downloads a CSV report with the scraped data.
- Implements basic error handling and logging.

## Requirements
- Flask
- Flask-CORS
- requests
- Python's standard libraries: `os`, `shutil`, `re`, `csv`, `logging`, `urllib`

## Installation
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Navigate to the project directory.

## Usage
1. Start the server with `python app.py`.
2. Open a web browser and go to `http://localhost:8000/`.
3. Enter a YouTube channel name and submit.
4. The application will display the scraped data and provide a CSV download link.

## Endpoints
- `GET /`: Displays the homepage where you can input a YouTube channel name.
- `POST /review`: Processes the channel name, scrapes data, and displays results.

## Configuration
- Set the Flask app and debug mode in the main block.
- Configure logging in the `scrapper.log` file.
- Modify BASE_DIR for different directory structures.

## Notes
- The scraper uses a fake user agent to avoid being blocked by Google.
- Currently configured to scrape only the top 5 videos from a channel.
- Error handling is basic; customize as per requirements.
- CORS is enabled for cross-origin requests, adjust it based on deployment needs.

## Disclaimer
This scraper is for educational purposes only. Scraping YouTube can be against their terms of service. Use responsibly and ethically.
