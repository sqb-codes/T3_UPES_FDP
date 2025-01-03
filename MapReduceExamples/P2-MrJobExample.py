from mrjob.job import MRJob

class WordCount(MRJob):
    def mapper(self, _, line):
        for word in line.split():
            yield word.lower(), 1
    
    def reducer(self, word, counts):
        yield word, sum(counts)

WordCount.run()