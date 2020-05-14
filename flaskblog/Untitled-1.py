class Cup:
    def _init_(self):
        self.color=None
        self.content=None
        
    def fill(self,beverage):
        self.content=beverage
        
    def empty(self):
        self.content=None
        
    def display(self):
        print("Color: %s \n Content: %s"%(self.color,self.content))
        
cup=Cup()
cup.color="red"
cup.content="tea"
cup.empty()
cup.fill("Coffee")
cup.display()