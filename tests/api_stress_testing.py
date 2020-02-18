from datetime import datetime
import csv
import requests
import statistics
import time

from multiprocessing import Process, Pool

## Config Variables ##
API_ENDPOINT = "http://crossmod.ml/api/v1/get-prediction-scores"
API_KEY = "ABCDEFG"

## Single Endpoint Testing
#Tests number of comments able to be handled by a single comment_to_file
'''
with open('../stress_tests/single_endpoint.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["num_of_comments", "time_elapsed"])
    for i in range(1, 2000, 100):
        num_of_comments = i
        comments = []
        for i in range(0, num_of_comments):
            comments.append("ADJSLKFJLKSDJKLSDJFKLHLKEJS")

        data = {"comments": comments,
                    "key": API_KEY}

        ## Get request
        startTime = datetime.now()
        r = requests.post(url= API_ENDPOINT, json = data)
        endTime = datetime.now()
        writer.writerow([i, endTime - startTime])

        print("Time elapsed (", i, "comments ): ", (endTime - startTime))

file.close()
'''

## Multiple Endpoint Testing
def make_call(endpoints):
    startTime = datetime.now()
    r = requests.post(url= API_ENDPOINT, json = data)
    endTime = datetime.now()

    timeElapsed = (endTime-startTime).microseconds / 1e6
    return timeElapsed

# Prepare data to be called
num_comments = 100
comments = []
for i in range(0, num_comments):
    comments.append("ADJSLKFJLKSDJKLSDJFKLHLKEJS")
data = {"comments": comments,
            "key": API_KEY}

# Record CSV file with rows(num_endpoints, longest response time (seconds))
'''
f = open("../stress_tests/multiple_endpoints.csv", "w")
num_endpoints = 150
for i in range(1, num_endpoints):
    print(i, "Endpoints")
    pool = Pool(processes=i)
    output = pool.map(make_call, range(i))
    pool.close()
    pool.join()
    f.write(str(i) + "," + str(max(output)) + "\n")
    print(max(output))

f.close()
'''
def run_tests():
    num_endpoints = 200
    print(num_endpoints, "Endpoints")
    pool = Pool(processes=num_endpoints)
    output = pool.map(make_call, range(num_endpoints))
    pool.close()
    pool.join()
    print(statistics.mean(output))

for i in range(1, 11):
    print("Second ", i)
    run_tests()
    time.sleep(1)
