from __future__ import print_function

import string
import boto3

print('Loading function')

def lambda_handler(event, context):

    class DocReporter:
        # Given a list of words, use S3 to locate the document with the highest tf-score per word.
        # Returns a dictionary where each input word is a key and
        # the value is a tuple with two elements listing the document scoring highest for the word, and the corresponding tf-score
        # Hardcoded s3 resource
        def create_report(self, words):
            self.s3_client = boto3.resource('s3')
            self.s3_bucket = 'assignment-doc-search' # arn:aws:s3:::assignment-doc-search
            report = []

            for obj in self.s3_client.Bucket(self.s3_bucket).objects.all():
                text = obj.get()['Body'].read()
                results = self.calculate_tf_score(obj.key, text, words)
                for result in results:
                    report.append(result)
            final_report = self.compare_score(report)

            self.print_scores(final_report)

            return final_report


        # Given a list of tuples where each tuple: (word, doc, score).
        # Returns a list where each word (key) follows a value with the document and highest TF score as a tuple:
        # {'word': (doc, score), ...} where doc is str and score is a float.
        def compare_score(self, list):
            highest_scoring = {}

            for result in list:
                if result[0] not in highest_scoring or highest_scoring[result[0]][1] < result[2]:
                    highest_scoring[result[0]] = (result[1], result[2])
            return highest_scoring


        # Given a text and a list of words, return the score for each word and
        # return their score in a tuple list:
        # [(word, doc, score), ....]
        def calculate_tf_score(self, doc_name, text, words):
            words_count_list = {x: 0 for x in words}
            report = []
            # Remove all non-alphabetic characters, then split text to an array
            ary = text.strip().translate(None, string.punctuation).lower().split()
            word_count = len(ary)
            # Count each of the words in parameter words in the text
            for word in ary:
                if word in words:
                    words_count_list[word] += 1
            # Calculate the tf-score for each word in words
            for word, count in words_count_list.iteritems():
                if count == 0:
                    tf_score = 0.0
                else:
                    tf_score = (float(count)/float(word_count))
                report.append((word, doc_name, tf_score))
            return report


        # Prints the highest tf-score of each word, given a full_report
        def print_scores(self, final_report):
            header_row = "Word".ljust(25) + "Document".ljust(25) + "Score"
            print()
            print(header_row)
            print('------------------------------------------------------------')

            for word, result in final_report.iteritems():
                print(word.ljust(25) + result[0].ljust(25) + str(result[1]))


    words = event['words']
    reporter = DocReporter()
    reporter.create_report(words)

