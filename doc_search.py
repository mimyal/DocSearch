from doc_reporter import DocReporter

reporter = DocReporter()
docs = ['mobydick-chapter1.txt', 'mobydick-chapter2.txt', 'mobydick-chapter3.txt', 'mobydick-chapter4.txt', 'mobydick-chapter5.txt']
words = ['queequeg', 'whale', 'sea']
reporter.create_report_from_local_documents(docs, words)
