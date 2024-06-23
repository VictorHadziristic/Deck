from openai import OpenAI
import subprocess
import base64
import os
from dotenv import load_dotenv
import json

load_dotenv()

model = OpenAI()
model.timeout = 30

def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

def url2screenshot(url):
    if os.path.exists("screenshot.jpg"):
        os.remove("screenshot.jpg")

    result = subprocess.run(
        ["node", "screenshot.js", url],
        capture_output=True,
        text=True
    )

    exitcode = result.returncode
    output = result.stdout

    if not os.path.exists("screenshot.jpg"):
        print("ERROR")
        return "Failed to scrape the website"
    
    b64_image = image_b64("screenshot.jpg")
    return b64_image

def gpt(messages):
    response = model.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=4096,
        temperature=0
    )
    
    return response.choices[0].message.content

def analyze(b64_image):
    return gpt([
            {
                "role": "system",
                "content": """
                    You a website analyzer, your job is to identify pertinent data fields in a given website, 
                    output json object that outlines available data fields.

                    Only include data fields, not the data itself.

                    DO NOT PROVIDE ANY EXPLANATION. This output will be used by other code. Make sure keys are unique.
                """,
            }
        ] + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "high"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze the website",
                    }
                ]
            }
        ])

def extract(b64_image, data_schema):
    return gpt([
            {
                "role": "system",
                "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction. Output JSON, NO EXPLANATION.",
            }
        ] + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "high"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"Extract data from the website using the following data schema: {data_schema}",
                    }
                ]
            }
        ])

def capture_webpage(url):
    b64_image = url2screenshot(url)
    
    if b64_image == "Failed to scrape the website":
        return "Failed to scrape the website"
    else:
        return b64_image

# NOTE: This implementation is more about AI analysis than addressing all the challenges of Crawling and Scraping.
# This is a multi-agent approach, with analyzer and extractor agents so far. In the future I would also add a web agent
# Allowing for a hybrid AI/Automation solution for navigating and interacting with DOM elements (e.g., logging in).


# NOTE: Analysis and Extraciton are split into two steps, analyze will provide a data schema which could be 
# vetted/managed by the user, and then supplied to many extractions happening in parallel.
# This approach would make extraction output more deterministic and consistent, critical when stiching the outputs together.
# Additionally, in the world of data, there is no guarantee that data fields even exist, supplying a schema would help identify
# missing data. In a productionized version of this app I would use something more robust like a pydantic schema object.

webpage = capture_webpage("https://doctors.cpso.on.ca/DoctorDetails/Gillian-Mary-Brakel/0181571-76088")## supply your url here.
data_schema = analyze(webpage) 

with open('output.json', 'w') as json_file:
    json.dump(json.loads(extract(webpage, data_schema)), json_file, indent=4)