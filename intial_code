from bs4 import BeautifulSoup
import requests
import time

# Set the User-Agent header to mimic a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}

# Define the total number of pages you want to scrape
total_pages = 13  # This example is for 13 pages (0 to 12)

# Loop through the search result pages
for i in range(total_pages):
    # Calculate the offset to navigate to the next page
    offset = i * 30
    url = f'https://www.tripadvisor.com/Hotels-g60713-oa{offset}-San_Francisco_California-Hotels.html'
    
    req = requests.get(url, headers=headers)
    
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')

        # Save the HTML content to a file
        with open(f"trip_advisor_search_pg{i}.html", "w", encoding="utf-8") as file:
            file.write(str(soup))

        print(f"Page {i} saved.")
    else:
        print(f"Failed to retrieve page {i}. Status code: {req.status_code}")

    time.sleep(5)  # Add a delay to avoid overloading the server
