"""
In this script, data on NFTs is requested from the OpenSea API and stored for future use.
"""

import requests
import json
import time
import datetime

def get_fifty(offset):
    
    """
    This function will retrieve 50 NFTs from the opensea api.
    It retrieves the most traded NFTs in descending order, starting at the offset passed.
    """
    
    # URL stem to request assets from the OpenSea API.
    url = 'https://api.opensea.io/api/v1/assets?'

    # Parameters for the API, set to request the most-traded NFTs in descending order 50 at a time (which is the limit).
    parameters = [
        'order_by=sale_count',
        'order_direction=desc',
        f'offset={offset}',
        'limit=50']
    
    # Combine URL stem and parameters to form the full URL.
    for param in parameters:
        url += param+'&'
    url = url[:-1]

    # Request data from API and return the result.
    response = requests.request("GET", url)
    return response

num_requests = 200 # Sets number of API requests to perform.  50 NFTs will be retrieved with each request.

"""
num_requests is limited to 201 due to the API apparently not being able to handle offset larger than 10,000
(When I tried, I got a code 400.)
200 is used for simplicity
"""

t0 = time.time() # Initial time stored to track how long it takes to acquire data.
num_fails = 0 # How many requests fail at least once?

# This process will be completed three times to minimize NFTs being completely missed and see how rapidly sales are occurring.
for data_pass in range(3):
    offset = 0 # Updated with each request to begin where the last request ended.
    request_num = 1 # Iterate with each request to update filenames.
    request_failed = False # Used to track if the last request failed.
    if data_pass == 0: # The passes are labeled a, b, and c instead of 1, 2, and 3 to differentiate from request_num
        which_pass = 'a'
    elif data_pass == 1:
        which_pass = 'b'
    else:
        which_pass = 'c'

    while request_num <= num_requests: # Each loop performs one API request.

        response = get_fifty(offset) # Perform API request.

        if response.status_code == 200: # Check that the request was successful.
            json.dump(response.json(), open(f'./raw_data/request_{request_num}_{which_pass}', 'w')) # Save the data in a json file.
            if request_failed == True:
                print('Success!')
                request_failed = False
            if request_num % 10 == 0: # Update the user after every 10 requests
                print(f'Completed request {request_num} out of {num_requests} on pass {which_pass} of c. '
                      f'{datetime.timedelta(seconds=time.time()-t0)} elapsed.')
            offset += 50
            request_num += 1
    
        elif request_failed == False: # If the request was not successful, warn the user and try again once before continuing.
            print(f'WARNING: Request {request_num} of pass {which_pass} failed with code {response.status_code}. Trying again.')
            num_fails += 1
            request_failed = True
    
        else: # If the request fails twice, tell the user and move on.
            print(f'WARNING: Request {request_num} of pass {which_pass} failed again.  Code {response.status_code}. Moving on.')
            offset += 50
            request_num += 1
            request_failed = False
    
        time.sleep(2) # Wait at least 2 seconds between each request.

print(f'Data acquisition complete.  {num_fails} requests failed at least once.  Please check error messages above.')    

# Load all the data stored in json files into a list of dictionaries.
stored_data = []
for i in range(1, num_requests+1):
    stored_data.append(json.load(open(f'./raw_data/request_{i}_a', 'r')))
for i in range(1, num_requests+1):
    stored_data.append(json.load(open(f'./raw_data/request_{i}_b', 'r')))
for i in range(1, num_requests+1):
    stored_data.append(json.load(open(f'./raw_data/request_{i}_c', 'r')))
    
# Extract the id for each NFT in stored_data
ids = []
for request in stored_data:
    for nft in request['assets']:
        ids.append(nft['id'])

print(f'Unique IDs found: {len(set(ids))}')
