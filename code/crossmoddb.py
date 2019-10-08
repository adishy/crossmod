import csv
import fcntl
import os.path

class CrossmodDB:
    def __init__(self, output_file = 'db_crossmod.csv'):
        self.output_file_name = output_file
        
        ### Check if file had previously been created
        file_existed = os.path.isfile(self.output_file_name)

        self.csv_file = open(self.output_file_name, 'a')

        '''
            Schema:
                * Timestamp         (column name: timestamp)
                * Comment ID        (column name: comment_id) (Reddit Comment ID)
                * Comment Body        (column name: comment_bidy)
                * Toxicity Score    (column name: toxicity_score)
                * Crossmod Action   (column name: crossmod_action)
        '''
        self.schema = ['timestamp', 'comment_id', 'comment_body', 'toxicity_score', 'crossmod_action']

        ### Open CSV file for reading/writing
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames = self.schema)
        self.csv_reader = csv.DictReader(self.csv_file, fieldnames = self.schema)
        
        ### Write column names to CSV file if the file did not exist previously
        if not file_existed:
            self.csv_writer.writeheader()
    
        self.crossmod_details = {}

        for column_name in self.schema:
            self.crossmod_details[column_name] = []

    def lock_file(self):
        fcntl.flock(self.csv_file, fcntl.LOCK_EX)

    def unlock_file(self):
        fcntl.flock(self.csv_file, fcntl.LOCK_UN)

    def write_args(self, *argv):
        row = {}
        ith_column_name = 0

        for arg in argv:
            column_name = self.schema[ith_column_name]
            row[column_name] = arg
            ith_column_name += 1
        
        self.write(**row)

    def write(self, **kwargs):
        self.lock_file()
        self.csv_writer.writerow(kwargs)
        self.unlock_file()

    def read(self):
        for row in self.csv_reader:
            self.crossmod_details['timestamp'].append(row['timestamp'])
            self.crossmod_details['comment_id'].append(row['comment_id'])
            self.crossmod_details['comment_body'].append(row['comment_body'])
            self.crossmod_details['toxicity_score'].append(row['toxicity_score'])
            self.crossmod_details['crossmod_action'].append(row['crossmod_action'])

            print(row['timestamp'], row['comment_id'], row['comment'], row['toxicity_score'], row['crossmod_action'])
            

    def exit(self):
        self.csv_file.close()

def main():
    db = CrossmodDB()
    db.write_args('a', 'b', 'c', 'd', 'e')
    db.write(timestamp = 'a',
             comment_id = 'b',
             comment_body = 'c',
             toxicity_score = 'e',
             crossmod_action = 'e')
    db.exit()
    
if __name__ == "__main__":
    main()
