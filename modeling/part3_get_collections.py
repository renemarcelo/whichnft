"""
In this script, data on specific NFT collections that have at least one
NFT with at least 20 sales is requested from the OpenSea API and stored for future use.
"""

import pandas as pd
import requests
import json
import time
import datetime

def get_collection(slug):
    
    """
    This function will retrieve the collection with the provided stub from the OpenSea API.
    """
    
    # URL stem to request a single collection from the OpenSea API.
    stem = 'https://api.opensea.io/api/v1/collection/'
    
    # Combine URL stem and slug to form the full URL.
    url = stem + slug

    # Request data from API and return the result.
    response = requests.request("GET", url)
    return response

t0 = time.time() # Initial time stored to track how long it takes to acquire data.
num_fails = 0 # How many requests fail at least once?

slugs_df = pd.read_csv('./top_collections.csv') # Retrieve desired collection slugs from CSV.
slugs = [slug for slug in slugs_df['slug']] # Store slugs in a list for easier indexing.
num_slugs = len(slugs) # Number of collections to be downloaded.
collections_dict = {} # Dictionary to hold all the collections as they are retrieved.
request_num = 0 # Iterate with each request to track progress.
request_failed = False # Used to track if the last request failed.

while request_num < num_slugs: # Each loop performs one API request.

    response = get_collection(slugs[request_num]) # Perform API request.

    if response.status_code == 200: # Check that the request was successful.
        collections_dict[slugs[request_num]] = response.json()
        if request_failed == True:
            print('Success!')
            request_failed = False
        if (request_num+1) % 10 == 0: # Update the user after every 10 requests
            print(f'Completed request {request_num+1} out of {num_slugs}. {datetime.timedelta(seconds=time.time()-t0)} elapsed.')
        request_num += 1
    
    elif request_failed == False: # If the request was not successful, warn the user and try again once before continuing.
        print(f'WARNING: Request for collection {slugs[request_num]} failed with code {response.status_code}. Trying again.')
        num_fails += 1
        request_failed = True
    
    else: # If the request fails twice, tell the user and move on.
        print(f'WARNING: Request for collection {slugs[request_num]} failed again.  Code {response.status_code}. Moving on.')
        request_num += 1
        request_failed = False
    
    time.sleep(2) # Wait at least 2 seconds between each request.

json.dump(collections_dict, open(f'./raw_collections/collections', 'w')) # Save the data in a json file.
    
print(f'Data acquisition complete.  {num_fails} requests failed at least once.  Please check error messages above.')