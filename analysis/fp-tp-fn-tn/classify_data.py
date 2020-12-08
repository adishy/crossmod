import csv

# Takes in reporting_experiment.csv file and creates/truncates 4 separate csvs for FPs, FNs, TPs, TNs
# Excludes filtered comments
reporting_data = "reporting_experiment.csv"

with open(reporting_data, 'r') as reporting_data, open('all_FPs.csv', 'w+') as fps, open('all_FNs.csv', 'w+') as fns, open('all_TPs.csv', 'w+') as tps, open('all_TNs.csv', 'w+') as tns:
    # initialize reader/writers
    csvReader = csv.reader(reporting_data)
    fpWrite = csv.writer(fps)
    tpWrite = csv.writer(tps)
    fnWrite = csv.writer(fns)
    tnWrite = csv.writer(tns)

    #write headers
    header = next(csvReader)
    fpWrite.writerow(header)
    tpWrite.writerow(header)
    fnWrite.writerow(header)
    tnWrite.writerow(header)

    rowNum = 1
    for row in csvReader:
        if (rowNum % 10000 == 0):
            print("Progress", rowNum, "rows")
        # Positives
        if row[4] != "EMPTY" and row[4] != "filtered": # Crossmod marked as toxic (positive)
            # TRUE positive
            if row[7]: # Banned_by is not none, moderator agreed postive
                tpWrite.writerow(row)

            # FALSE postiive
            else: # Banned_by is none, so moderator did not remove/agree positive
                fpWrite.writerow(row)

        # Negatives
        elif row[4] != "filtered": # Crossmod EMPTY, did not mark as toxic (negative)
            # TRUE negative
            if not row[7]: # banned_by is none, moderator agrees negative
                tnWrite.writerow(row)

            # FALSE negative
            else: # banned_by is not none, moderator banned
                fnWrite.writerow(row)

        rowNum += 1
