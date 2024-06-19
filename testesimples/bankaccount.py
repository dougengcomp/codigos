class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.balance=balance
        print (f"created a new bank account for {self.owner} with balance {self.balance}")

    def deposit (self, amount):
        self.balance+=amount
        print (f"new balance after deposit is {self.balance}")

    def withdrawal (self, amount):
        if amount>self.balance:
            print ("not enough funds")
        else:    
            self.balance-=amount
            print (f"new balance after withdrawal is {self.balance}")
    def __str__(self):
        return f'Account owner:   {self.owner}\nAccount balance: ${self.balance}'

conta1=BankAccount("Pareto", 1000)
conta1.deposit (100)
conta1.withdrawal (200)
conta1.withdrawal(2000)
print (conta1)
    