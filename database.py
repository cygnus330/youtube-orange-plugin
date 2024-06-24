class videoDB:
    def __init__(self):
        self.db = {}

    def push(self, v, info):


        self.db[v] = info

    def get(self, v):
        if v not in self.db:
            return []
        return self.db[v]

    def isOn(self, v):
        return (v in self.db)

    def closest(self, v, res):
        if not self.isOn(v):
            return None
        return min(self.db[v]['res'], key=lambda x: abs(x - res))

class downDB:
    def __init__(self):
        self.db = {}

    def add(self, v, res, act):
        # 0: 다운로드 중, 1: 다운로드 완료, -1: 없음
        self.db[v, res] = act

    def get(self, v, res):
        if (v, res) in self.db:
            return self.db[v, res]
        else:
            return -1