class Pair(object):
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)) and (self.p1 == other.getP1()) and (self.p2 == other.getP2())
    
    def __hash__(self):
        return hash(self.p1)^hash(self.p2)
    
    def getP1(self):
        return self.p1
    
    def getP2(self):
        return self.p2
    
    def printPair(self):
        print(str(self.p1) + ' : ' + str(self.p2))
    
    def toString(self):
        return str(self.p1) + ',' + str(self.p2) + ' '