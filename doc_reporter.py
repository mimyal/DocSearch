import string
import boto3

class DocReporter:
    # Given a list of words and a list of local documents find the document with the highest tf-score per word.
    # Returns a dictionary where each input word is a key and
    # the value is a tuple with two elements listing the document scoring highest for the word, and the corresponding tf-score
    # it also prints out a report
    # @Comment: I left this method separate from #create...s3... because I intended this function not part of a search program,
    #   as the documents are better stored not locally. Not using S3 would allow line-by-line read, but I did not implement it here.
    def create_report_from_local_documents(self, docs, words):
        report = []
        for doc in docs:
            with open(doc) as file:
                text = file.read()
                results = self.calculate_tf_score(doc, text, words)
                for result in results:
                    report.append(result)
        final_report = self.compare_score(report)

        self.print_scores(final_report)

        return final_report


    # Given a list of words, use S3 to locate the document with the highest tf-score per word.
    # Prints out a report for each of the words.
    # Returns a dictionary where each input word is a key and
    # the value is a tuple with two elements listing the document scoring highest for the word, and corresponding tf-score
    # it also prints out a report
    def create_report_from_s3_documents(self, s3_key, words):
        self.s3_client = boto3.resource('s3')
        self.s3_bucket = s3_key  # arn:aws:s3:::assignment-doc-search
        report = []

        for obj in self.s3_client.Bucket(self.s3_bucket).objects.all():
            text = obj.get()['Body'].read()  # S3 only reads the full file
            results = self.calculate_tf_score(obj.key, text, words)
            for result in results:
                report.append(result)
        final_report = self.compare_score(report)

        self.print_scores(final_report)

        return final_report


    # Given a list of tuples where each tuple: (word, doc, score).
    # Returns a list where each word (key) follows a value with the document and highest TF score as a tuple:
    # {'word1': (docx, score), ...} where doc is str and score is a float.
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
        words[:] = [w.lower() for w in words]
        words_count_list = {x: 0 for x in words}
        results = []
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
            results.append((word, doc_name, tf_score))
        return results


    # Prints the highest tf-score of each word, given a full_report
    def print_scores(self, final_report):
        header_row = "Word".ljust(25) + "Document".ljust(25) + "Score"
        print()
        print(header_row)
        print('------------------------------------------------------------')

        for word, result in final_report.iteritems():
            print(word.ljust(25) + result[0].ljust(25) + str(result[1]))


