print "Hello World!"

class people :
    name = ""
    age = 0
    __weight = 0
    def __int__(self, n, a, w) :
        self.name = n
        self.age = a
        self.__weight = w

    def main (self):
        print self.name


#if __name__ == "__main__" : 
print "main!"
dqj = people('dqj',10,20)
dqj.main()
