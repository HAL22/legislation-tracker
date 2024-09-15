class Legislation:
    def __init__(self, title, description, summary, region, status, type_, index, date):
        self.title = title
        self.description = description
        self.summary = summary
        self.region = region
        self.status = status
        self.type = type_
        self.index = index
        self.date = date

    def to_tuple(self):
        return (self.title, self.description, self.summary, self.region, self.status, self.type, self.index, self.date)
