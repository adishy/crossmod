import csv
import fcntl
import os.path

class CrossmodDB:
    def __init__(self, output_file = 'db_crossmod.csv'):
        self.output_file_name = output_file
        
        ### Check if file had previously been created
        file_existed = os.path.isfile(self.output_file_name)

        self.csv_file_write = open(self.output_file_name, 'a')
        self.csv_file_read = open(self.output_file_name, 'r')

        '''
            Schema:
                * Moderated At Timestamp  (column name: moderated_at)       (Timestamp in UTC at which the comment was posted)
                * Comment ID              (column name: comment_id)         (Reddit Comment ID)
                * Comment Body            (column name: comment_body)
                * Toxicity Score          (column name: toxicity_score)
                * Crossmod Action         (column name: crossmod_action)
                * Author                  (column name: author)             (Reddit username of comment author)
                * Subreddit               (column name: subreddit)          (Subreddit name where the moderated Reddit comment was posted in)
                * Banned By               (column name: banned_by)          (The name of the moderator who removed the comment)
                * Banned At               (column name: banned_at)          (Timestamp in UTC at which the comment was moderated on)
        '''
        self.schema = ['moderated_at', 
                       'comment_id', 
                       'comment_body', 
                       'toxicity_score', 
                       'crossmod_action', 
                       'author', 
                       'subreddit',
                       'banned_by', 
                       'banned_at']

        ### Open CSV file for reading/writing
        self.csv_writer = csv.DictWriter(self.csv_file_write, fieldnames = self.schema)
        self.csv_reader = csv.DictReader(self.csv_file_read, fieldnames = self.schema)
        
        ### Write column names to CSV file if the file did not exist previously
        if not file_existed:
            self.csv_writer.writeheader()
    
        self.crossmod_details = {}

        for column_name in self.schema:
            self.crossmod_details[column_name] = []

    ### Used to ensure the CSV file cannot be written to by any other instance 
    ### of CrossmodDB after it has been locked  
    def lock_file(self):
        fcntl.flock(self.csv_file_write, fcntl.LOCK_EX)

    ### Used to ensure the lock for the CSV file is released so any instance of
    ### CrossmodDB can also write to the file
    def unlock_file(self):
        fcntl.flock(self.csv_file_write, fcntl.LOCK_UN)

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
        self.crossmod_details = {}

        self.lock_file()
        header_row = False

        for row in self.csv_reader:
            if not header_row:
                header_row = True
                continue

            for column_name in self.schema:
                self.crossmod_details[column_name].append(row[column_name])
        self.unlock_file()
    
    def exit(self):
        self.csv_file_write.close()
        self.csv_file_read.close()

def main():
    db = CrossmodDB()
    db.write_args('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
    db.write(moderated_at = 'a',
             comment_id = 'b',
             comment_body = 'c',
             toxicity_score = 'e',
             crossmod_action = 'e',
             author='f',
             subreddit='g',
             banned_by='h',
             banned_at='i',)
    db.read()
    db.exit()
    
if __name__ == "__main__":
    main()
