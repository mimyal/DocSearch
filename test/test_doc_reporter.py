from doc_reporter import DocReporter

def test_compare_score_should_return_highest_score_list():
    reporter = DocReporter()
    input = [
        ('word1', 'doc1', 5),
        ('word2', 'doc1', 3),
        ('word1', 'doc2', 6),
        ('word2', 'doc2', 8)
    ]
    expected_output = {
        'word1': ('doc2', 6),
        'word2': ('doc2', 8)
    }
    output = reporter.compare_score(input)
    assert output == expected_output


def test_compare_score_should_return_first_document_for_same_score():
    reporter = DocReporter()
    input = [
        ('word1', 'doc1', 5),
        ('word2', 'doc1', 5),
        ('word1', 'doc2', 5),
        ('word2', 'doc2', 5)
    ]
    expected_output = {
        'word1': ('doc1', 5),
        'word2': ('doc1', 5)
    }
    output = reporter.compare_score(input)
    assert output == expected_output


def test_compare_score_should_return_highest_score_when_score_is_close_to_zero():
    reporter = DocReporter()
    input = [
        ('word1', 'doc1', 0.0),
        ('word2', 'doc1', 0.000001),
        ('word3', 'doc1', 0.0),
        ('word1', 'doc2', 0.0),
        ('word2', 'doc2', 0.0),
        ('word3', 'doc2', 0.000001)
    ]
    expected_output = {
        'word1': ('doc1', 0.0),
        'word2': ('doc1', 0.000001),
        'word3': ('doc2', 0.000001)
    }
    output = reporter.compare_score(input)
    assert output == expected_output


def test_calculate_tf_score_should_return_the_correct_score_list_of_one_word():
    reporter = DocReporter()
    doc = 'doc1'
    input = 'Once upon a time, far, far away'  # length = 7
    words = ['time']
    expected_output = [('time', 'doc1', 1.0/7.0)]
    output = reporter.calculate_tf_score(doc, input, words)
    assert output == expected_output


def test_calculate_tf_score_should_return_the_correct_score_for_list_of_words():
    reporter = DocReporter()
    doc = 'doc1'
    input = 'Once upon a time, far, far away' # length = 7
    words = ['time', 'far']
    expected_outputs = [('time', 'doc1', 1.0/7.0), ('far', 'doc1', 2.0/7.0)]
    outputs = reporter.calculate_tf_score(doc, input, words)
    for expected in expected_outputs:
        for output in outputs:
            if output[0] == expected[0]:
                assert output[2] == expected[2]


def test_calculate_tf_score_should_score_all_words():
    count = 0
    reporter = DocReporter()
    doc = 'doc1'
    input = 'Once upon a time, far, far away'  # Length is 7
    words = ['once', 'upon', 'a', 'time', 'far', 'away']
    expected_outputs = [('once', 'doc1', 1.0/7.0),
                        ('upon', 'doc1', 1.0/7.0),
                        ('a', 'doc1', 1.0/7.0),
                        ('time', 'doc1', 1.0/7.0),
                        ('far', 'doc1', 2.0/7.0),
                        ('away', 'doc1', 1.0/7.0)]
    outputs = reporter.calculate_tf_score(doc, input, words)
    for expected in expected_outputs:
        for output in outputs:
            if output[0] == expected[0]:
                count += 1
    if count != len(words):
        assert False


def test_calculate_tf_score_should_handle_uppercase_search_words():
    count = 0
    reporter = DocReporter()
    doc = 'doc1'
    input = 'Once upon a time, far, far away, I found myself at NASA'  # Length is 12
    words = ['I', 'NASA']
    expected_outputs = [('i', 'doc1', 1.0/12.0), ('nasa', 'doc1', 1.0/12.0)]
    outputs = reporter.calculate_tf_score(doc, input, words)
    for expected in expected_outputs:
        for output in outputs:
            if output[0] == expected[0]:
                assert output[2] == expected[2]
                count += 1
    if count != len(words):
        assert False

# # @todo I wanted to learn to mock things in Python, but decided to leave it for next time.
# # This is the S3-file word count per word
# # {'the': 124, 'hot': 0, 'ocean': 2} mobydick-chapter1.txt  # 2215 total words
# # {'the': 99, 'hot': 0, 'ocean': 0} mobydick-chapter2.txt  # 1431 total words
# # {'the': 298, 'hot': 2, 'ocean': 0} mobydick-chapter3.txt  # 5836 total words
# # {'the': 79, 'hot': 0, 'ocean': 0} mobydick-chapter4.txt  # 1658 total words
# # {'the': 36, 'hot': 1, 'ocean': 0} mobydick-chapter5.txt  # 742 total words
# # # This is the result of printed score for S3 documents and list of words:
# # Word                     Document                 Score
# # ------------------------------------------------------------
# # the                      mobydick-chapter2.txt    0.0691823899371
# # hot                      mobydick-chapter5.txt    0.00134770889488
# # ocean                    mobydick-chapter1.txt    0.000902934537246
# def test_create_report_from_s3_documents_should_return_highest_scoring_document_for_a_list_of_words():
#     reporter = DocReporter()
#     s3_key = 'assignment-doc-search'
#     words = ['ocean', 'the', 'hot']
#     expected_results = {
#         'the': (u'mobydick-chapter2.txt', float(99)/float(1431)),
#         'ocean': (u'mobydick-chapter1.txt', float(2)/float(2215)),
#         'hot': (u'mobydick-chapter5.txt', float(1)/float(742))
#     }
#     results = reporter.create_report_from_s3_documents(s3_key, words)
#     for word, result in results.iteritems():
#         for expected_word, expected in expected_results.iteritems():
#             if word == expected_word:
#                 assert result == expected
#
#
# def test_create_report_from_local_documents_should_return_highest_scoring_document_for_a_list_of_words():
#     reporter = DocReporter()
#     docs = ['../mobydick-chapter1.txt', '../mobydick-chapter2.txt', '../mobydick-chapter3.txt', '../mobydick-chapter4.txt', '../mobydick-chapter5.txt']
#     words = ['ocean', 'the', 'hot']
#     expected_results = {
#         'the': ('../mobydick-chapter2.txt', float(99)/float(1431)),
#         'ocean': ('../mobydick-chapter1.txt', float(2)/float(2215)),
#         'hot': ('../mobydick-chapter5.txt', float(1)/float(742))
#     }
#     results = reporter.create_report_from_local_documents(docs, words)
#     for word, result in results.iteritems():
#         for expected_word, expected in expected_results.iteritems():
#             if word == expected_word:
#                 assert result == expected
#
