import csv


class CrossmodDB:
    def __init__(self, output_file = 'crossmoddb.csv'):
        self.output_file_name = output_file
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
        self.csv_reader = csv.DictReader(self.csv_file)
        
        ### Write column names to CSV file
        #self.csv_writer.writeheader()
    
        self.crossmod_details = {'timestamp_arr': [],
                                 'comment_id_arr': [],
                                 'comment_arr': [],
                                 'toxicity_score_arr': [],
                                 'crossmod_action_arr': []}

    def write(self, timestamp, comment_id, comment_body, toxicity_score, crossmod_action):
        row = {'timestamp': timestamp,
               'comment_id': comment_id,
               'comment_body': comment_body,
               'toxicity_score': toxicity_score,
               'crossmod_action': crossmod_action}

        #[timestamp, comment_id, comment, toxicity_score, crossmod_action]
        self.csv_writer.writerow(row)

    def write_dict(self, **kwargs):
        row = [kwargs["timestamp"], kwargs["comment_id"], kwargs["comment_body"], kwargs["toxicity_score"], kwargs["crossmod_action"]]

        self.csv_writer.writerow(row)

    def read(self):
        for row in self.csv_reader:
            self.crossmod_details['timestamp_arr'].append(row['timestamp'])
            self.crossmod_details['comment_id_arr'].append(row['comment_id'])
            self.crossmod_details['comment_arr'].append(row['comment_body'])
            self.crossmod_details['toxicity_score_arr'].append(row['toxicity_score'])
            self.crossmod_details['crossmod_action_arr'].append(row['crossmod_action'])
            print(row['timestamp'], row['comment_id'], row['comment'], row['toxicity_score'], row['crossmod_action'])
        
        print(self.crossmod_details['timestamp_arr'])
        print(self.crossmod_details['comment_id_arr'])
        print(self.crossmod_details['comment_arr'])
        print(self.crossmod_details['toxicity_score_arr'])
        print(self.crossmod_details['crossmod_action_arr'])
            

def main():
    db = CrossmodDB()
    db.write('a', 'b', 'c', 'd', 'e')
    
if __name__ == "__main__":
    main()
