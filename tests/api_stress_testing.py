from datetime import datetime
import csv
import requests

from multiprocessing import Process

## Config Variables ##
API_ENDPOINT = "http://18.191.72.252:8000/get-prediction-scores"
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

## Multiple Endpoint Testing TODO
def make_call():
    startTime = datetime.now()
    r = requests.post(url= API_ENDPOINT, json = data)
    endTime = datetime.now()
    print("Time elapsed: ", (endTime - startTime))


num_comments = 10
comments = []
for i in range(0, num_comments):
    comments.append("ADJSLKFJLKSDJKLSDJFKLHLKEJS")

data = {"comments": comments,
            "key": API_KEY}


num_endpoints = 1000
print(num_endpoints, "Endpoints")
jobs = []
for j in range(0, num_endpoints):
    p = Process(target=make_call)
#    jobs.append(p)
    p.start()
#for j in jobs:
#    j.join()
