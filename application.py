from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
import requests
from urllib.request import urlopen as uReq
import logging
import pymongo
import os
import shutil
import re
import csv


# Get the base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up a logging file in the base directory
logging.basicConfig(filename=os.path.join(BASE_DIR, "scrapper.log"), level=logging.INFO)

# Create the Flask app
app = Flask(__name__)

# This function renders the homepage
@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

# This function handles POST and GET requests to the '/review' endpoint
@app.route("/review", methods=['POST', 'GET'])
def index():
    # Handle POST requests
    if request.method == 'POST':
        try:
            # Get the search query from the form input
            search_query = request.form['content'].replace(" ", "")
            
            # Set the user agent to a fake one to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            # Fetch the search results page from YouTube
            response = requests.get(f"https://www.youtube.com/@{search_query}/videos", headers=headers)
            response_text = response.text

            # Extract relevant information from the HTML response using regex
            video_ids = re.findall('"videoRenderer":{"videoId":".*?"', response_text)
            thumbnails = re.findall('"thumbnail":{"thumbnails":\[{"url":".*?"', response_text)
            titles = re.findall('"title":{"runs":\[{"text":".*?"', response_text)
            views = re.findall('"shortViewCountText":{"accessibility":{"accessibilityData":{"label":".*?"', response_text)
            published_times = re.findall('"publishedTimeText":{"simpleText":".*?"', response_text)
            
            # Create a report list to hold all of the relevant video data
            report_list = [
                ['S No', 'Video url', 'Thumbnail', 'Title', 'Views', 'Published Time']
            ]
            
            # Iterate through the video data and append it to the report list
            for i in range(5):
                video_url = 'https://www.youtube.com/watch?v=' + video_ids[i].split('"')[-2]
                thumbnail_url = thumbnails[i].split('"')[-2]
                title = titles[i].split('"')[-2]
                view_count = views[i].split('"')[-2]
                published_time = published_times[i].split('"')[-2]
                
                temp = [i+1, video_url, thumbnail_url, title, view_count, published_time]
                report_list.append(temp)
                
            # Write the report list to a CSV file
            csv_file_name = os.path.join(BASE_DIR, search_query+'.csv')
            with open(csv_file_name, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in report_list:
                    csvwriter.writerow(row)

            client = pymongo.MongoClient("mongodb+srv://reddysandeep0904:Sandeep@0588@cluster0.x3niyyi.mongodb.net/?retryWrites=true&w=majority")
            db = client['youtube_scrap']
            review_col = db['youtube_data']
            review_col.insert_many(report_list)
            
            # Render the result template with the report list and search query
            return render_template('result.html', report_list=report_list, channel=search_query)
        
        # Catch any exceptions and log them to the log file
        except Exception as e:
            logging.info(e)
            return render_template('error.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)