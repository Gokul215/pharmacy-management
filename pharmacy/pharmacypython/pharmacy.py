class Pharmacy:
    id=1
    transactionid=1
    def __init__(self):
        self.branches=[]
        self.customers=[]
        self.transactions=[]
        self.alternateproducts={}
        self.stocks=[]
        
    def addbranch(self,branchid,branchlocation,branchphone):
        branchmap={}
        branchmap['branchid']=branchid
        branchmap['branchlocation']=branchlocation
        branchmap['branchphone']=branchphone
        
        self.branches.append(branchmap)
        self.printbranch()
    def printbranch(self):
        print("Branch ID      Branch Location       Phone number")
        print("--------------------------------------------------")
        
        for branch in self.branches:
            # print(branch)
            # print (branch['branchid'],"           |           ", branch['branchlocation'],"           |           ", branch['branchphone'])
             print(f"{branch['branchid']:<15} | {branch['branchlocation']:<20} | {branch['branchphone']:<15}")
             print("--------------------------------------------------")
        
    def addstock(self,branchid,medicine,quantity,price,oneproductprice):
        stockmap={}
        stockmap['branchid']=branchid
        stockmap ['medicine']=medicine
        stockmap['quantity']=quantity
        stockmap['price']=price
        stockmap['oneproductprice']=oneproductprice
        
        self.stocks.append(stockmap)
        self.printstock()
    
    def printstock(self):
        print("Branch ID         Medicine         Availableqty     Price")
        print("--------------------------------------------------")
        
        for branch in self.branches:
            for st in self.stocks:
                if branch['branchid']==st['branchid']:
                    print(f"{st['branchid']:<15} | {st['medicine']:<20} | {st['quantity']:<10} | {st['price']:<15}")
                    print("--------------------------------------------------")
                    
    def addalternate(self,medicine,alternate):
        self.alternateproducts[medicine]=alternate
        self.printalternate()
        
    def printalternate(self):
        print("Medicine         Alternate")
        print("--------------------------------------------------")
       
        for medicine,alternates in self.alternateproducts.items():
            print(f"{medicine:<15}| {alternates:<15}")
            print("--------------------------------------------------")
                
    def addcustomer(self,customername,customerphone):
        customermap={}
        customermap ['customerid']=Pharmacy.id
        customermap['customername']=customername
        customermap['customerphone']=customerphone
        
        self.customers.append(customermap)
        Pharmacy.id+=1
        
        self.printcustomer()
        
    def printcustomer(self):
        print("CustomerId         Customer name          Phone")
        print("--------------------------------------------------")
        for customer in self.customers:
            
                print(f"{customer['customerid']:<15} |{customer['customername']:<15} | {customer['customerphone']:<15}")
                print("--------------------------------------------------")
                
    def purchaseproduct(self):
        customerid=input("enter the customer id: ")
        branchid=input("enter the branch id: ")
        transactionid=Pharmacy.transactionid
        while True:
            product=input("enter the product: ")
            quantity=int(input("enter the quantity: "))
            if self.isstockavailable(branchid,product,quantity):
                print("product available")
                # Pharmacy.transactionid+=1
                totalprice=self.getprice(branchid,product,quantity)
                transactionmap={}
                transactionmap['transactionid']=transactionid
                transactionmap['customerid']=customerid
                transactionmap['branchid']=branchid
                transactionmap['product']=product
                transactionmap['quantity']=quantity
                transactionmap['totalprice']=totalprice
                
                self.transactions.append(transactionmap)
                
                ch=input("Do you want to coninue(yes/no) :")
                if ch!='yes':
                    break
                
                
            elif product in self.alternateproducts and self.isstockavailable(branchid,self.alternateproducts[product],quantity) :
                print("Quantity not  available")
                
                
                ch=input(f"Do you want to purchase {self.alternateproducts[product]} :")
                if ch=='yes':
                    # Pharmacy.transactionid+=1
                    
                    totalprice=self.getprice(branchid,self.alternateproducts[product],quantity)
                    transactionmap={}
                    transactionmap['transactionid']=transactionid
                    transactionmap['customerid']=customerid
                    transactionmap['branchid']=branchid
                    transactionmap['product']=self.alternateproducts[product]
                    transactionmap['quantity']=quantity
                    transactionmap['totalprice']=totalprice
                    
                    self.transactions.append(transactionmap)
                    print(f'purcahsed {quantity} {self.alternateproducts[product]} price:{totalprice} ')
                    
                else:
                    break
                
            elif self.isstockavailableinanybranch(product,quantity) :
                
                for stock in self.stocks:
                    if stock['medicine']==product and stock['quantity'] >=quantity:
                        stock['quantity']-=quantity
                        anybranchid=stock['branchid']
                        break
                print(f"quantity not available in this branch. Available in {anybranchid} ")
                ch=input(" Do you want to continue(yes/no): ")
                if ch=='yes':
                    # Pharmacy.transactionid+=1
                    
                    totalprice=self.getprice(branchid,self.alternateproducts[product],quantity)
                    transactionmap={}
                    transactionmap['transactionid']=transactionid
                    transactionmap['customerid']=customerid
                    transactionmap['branchid']=anybranchid
                    transactionmap['product']=product
                    transactionmap['quantity']=quantity
                    transactionmap['totalprice']=totalprice
                    
                    self.transactions.append(transactionmap)
                else:
                    break
            else:
                print("no products")
                ch=input(f"Do you want to coninue(yes/no) :")
                if ch!='yes':
                    break
        Pharmacy.transactionid+=1
        self.printcustomersummary(customerid)
        
    def printcustomersummary(self,customerid):
        print("BranchId       TransactionnId     Customerid         product         quantity            price")
        print("-------------------------------------------------------------------------------------------------")
        for transaction in self.transactions:
            if transaction['customerid']==customerid:
                print(f" {transaction['branchid']:<15} | {transaction['transactionid']:<15} | {transaction['customerid']:<15} | {transaction['product']:<15} | {transaction['quantity']:<15} |  {transaction['totalprice']:<15}   ")
                print("-------------------------------------------------------------------------------------------------")
                
        
            
    def isstockavailable(self,branch,product,quantity):
        for stock in self.stocks:
            if stock['branchid'] ==branch and stock['medicine']==product and stock['quantity'] >=quantity:
                stock['quantity']-=quantity
                return True
        return False
    
    def getprice(self,branch,product,quantity):
        for  stock in self.stocks:
            if  stock['branchid'] ==branch and stock['medicine']==product :
                price= stock['oneproductprice']*quantity
                return price
        return 0
            
    def isstockavailableinanybranch(self,product,quantity):
        for stock in self.stocks:
            if stock['medicine']==product and stock['quantity'] >=quantity:
                return True
        return False
        
                
    def printsummary(self,customerid):
        print("BranchId       TransactionnId          product            quantity          price")
        print("------------------------------------------------------------------------------------")
        
        for transaction in self.transactions:
            if transaction['customerid']==customerid:
                print(f" {transaction['branchid']:<15} | {transaction['transactionid']:<15} | {transaction['product']:<15} | {transaction['quantity']:<15} |  {transaction['totalprice']:<15}   ")
                print("------------------------------------------------------------------------------------")
                    
        
                
        
        
        

pharmacy=Pharmacy()
while True:
    print(" 1. Add Branch \n 2. Add Stock \n 3. Associate Alternate Products \n 4. Add Customer \n 5. Purchase Products \n 6. Print Summary \n 7. Exit")
    choice = int(input("enter your choice: "))
    match(choice):
        case 1:
            branchid=input("enter the branch id: ")
            branchlocation=input("enter the branch location: ")
            branchphone=input("enter the branch phone: ")
            pharmacy.addbranch(branchid,branchlocation,branchphone)
        case 2:
            branchid=input("enter the branch id: ")
            medicine=input("enter the medicine: ")
            quantity=int(input("enter the quantity: "))
            price=int(input("enter the price: "))
            oneproductprice=price/quantity
            
            pharmacy.addstock(branchid,medicine,quantity,price,oneproductprice)
            
        case 3:
            medicine=input("enter the medicine:")
            alternate=input("enter the alternate name: ")
            
            pharmacy.addalternate(medicine,alternate)
        case 4:
            customername=input("enter the customer name: ")
            customerphone=input("enter the phone number: ")
            
            pharmacy.addcustomer(customername,customerphone)
        case 5:
            pharmacy.purchaseproduct()
        case 6 :
            customerid=input("enter the customer id: ")
            pharmacy.printsummary(customerid)
        case _:
            break
            