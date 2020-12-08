import csv
import random

# precondition: rows_sampled < out_file.length (in rows)
def random_sample(in_file, out_file, rows_sampled):
    print("Sampling", rows_sampled, "rows into", in_file, "into", out_file)

    input_size = -1
    with open(in_file, 'r') as data_in:
        csvReader = csv.reader(data_in)
        input_size = (len(list(csvReader)))

    with open(in_file, 'r') as data_in, open(out_file, 'w+') as data_out:
        csvReader = csv.reader(data_in)
        csvWriter = csv.writer(data_out)


        # write header
        header = next(csvReader)
        csvWriter.writerow(header)

        sample_rows = random.sample(range(1, input_size - 1), rows_sampled)
        sample_rows.sort()



        rowNum = 1
        sampleInd = 0
        for row in csvReader:
            if sampleInd >= len(sample_rows):
                break
            if rowNum == sample_rows[sampleInd]:
                csvWriter.writerow(row)
                sampleInd += 1
            rowNum += 1

random_sample("all_FNs.csv", "500_FNs.csv", 500)
random_sample("all_FPs.csv", "500_FPs.csv", 500)
random_sample("all_TNs.csv", "500_TNs.csv", 500)
random_sample("all_TPs.csv", "500_TPs.csv", 500)
