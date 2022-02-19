class Image:

    def __init__(self, content, title, copyright, date):
        self.content = content
        self.title = title
        self.date = date
        pos = copyright.find('(')
        self.info = copyright[0:pos]
        self.copyright = copyright[pos+1:len(copyright)-1]

