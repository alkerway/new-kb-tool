class CSVParser():
    def __init__(self):
        super(CSVParser, self).__init__()
        print('ayyyy')

    def parseCsv(self, csvFileName):
        with open(csvFileName, 'r') as contents:
            print(contents)