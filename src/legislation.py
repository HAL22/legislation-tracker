class Legislation:
    def __init__(self, title, description, summary, region, status, type_, index_pn, date,link):
        self.title = title
        self.description = description
        self.summary = summary
        self.region = region
        self.status = status
        self.type = type_
        self.index_pn = index_pn
        self.date = date
        self.link = link
    def to_tuple(self):
        return (self.title, self.description, self.summary, self.region, self.status, self.type, self.index_pn, self.date, self.link)
