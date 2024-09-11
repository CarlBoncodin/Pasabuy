import pandas as pd #Pandas is a CSV file reader, This module can do wh a csv Can't
import sys
#Stores is used for Stores choice
pd.set_option('mode.chained_assignment', None)
header = ['Shop','Product','Price','Stock']
cartdf = pd.DataFrame(columns= header)
cartdf = cartdf[header]
cartdf.index += 1

#First function used in the PasaBuy application
def stores():
    x = 0 #User Input
    decision = [1,2,3,4,5,6,7]
    while x != 9:
        print('==================================\nWelcome to Pasabuy!\n==================================''\nChoose a category:\n''[1] Food \n''[2] Medicine \n''[3] Grocery \n''[4] School Supply \n''[5] View Cart\n''[6] Check out\n''[7] Exit\n')
        while x not in decision: #This is for checking the input if int or not
         try:
            x = int(input('\nChoice: '))
         except ValueError:
            print('\nInvalid Choice')
            pass
        if x not in decision:
            print('\nInvalid Choice')
            continue
        if x == decision[0]:
            print('\nChoose Food store')
            productsview('Food Stores.csv')
        if x == decision[1]:
            print('\nChoose Pharmacy Store')
            productsview('Pharmacy Stores.csv')
        if x == decision[2]:
            print('\nChoose Grocery Store')
            productsview('Grocery Stores.csv')
        if x == decision[3]:
            print('\nChoose School supplies Store')
            productsview('School supplies Stores.csv')
        if x == decision[4]:
            cart()
            x = -1
        if x == decision[5]:
            print('\nCheck out')
            checkout()
            x = -1
        if x == decision[6]:
            print('\nThank you for visiting Pasabuy!')
            return

#Showing the list of shops
def productsview(list):
    x = "NaN" #User Input
    y = [0] #Shops array
    data_list = ['Shop','Product','Price','Stock']
    Data = pd.read_csv(list,usecols=['Shop'])#Reading only the Prod no. and Shop column
    data2 = pd.read_csv(list,usecols=data_list)
    df = Data.head(len(Data))
    df_shops = df.drop_duplicates(subset= ['Shop'])#Use to clear the duplicates
    df_shops = df_shops.reset_index(drop=True)#The index are disorganized when the dupes are removed, this will reset the index
    df_shops.index += 1
    df_shopslist = df_shops['Shop'].tolist()
    while x not in df_shopslist: #Choice Loop
        print('\n==================================\nSelect a store\n==================================')   
        print(df_shops) 
        print("[9] Search Item\n[0] Return")
        try:
            x = int(input("\nEnter Shop No.: "))
            if x == 0:
                print("\n")
                stores()
            elif x == 9:
                print('\n')
                searchproduct(data2)
            else:
                x = x-1
                try:
                    shop = df_shops.iloc[x,0]
                    shopname = str(shop)
                    product(data2,shopname)
                except:
                    print("\nInvalid Shop No. " + e)
        except:
            print("\nInvalid Input")

        
       
#Product Function, Used to Select a product that is found within the shop's name.
def product(data, x):
    global cartdf
    y = 0
    list = ['Shop','Product', 'Price', 'Stock']
    print('\n==================================\nProducts\n==================================')
    chosen = data[data["Shop"] == x]
    chosen = chosen[list]
    chosen.reset_index(drop= True ,inplace= True)
    chosen.index += 1
    chosenlist = chosen.columns.tolist()
    itemfound = chosen['Product']
    itemfound2 = chosen[list]
    print(chosen)
    print('\n[0] Return')
    while x not in chosen:
        try:
            x = int(input("\nEnter Prod No.:  "))
        except:
            print('\nInvalid No.')
        if x == 0:
            print('\n')
            return
        x = x-1
        item = itemfound.iloc[x]
        item2 = itemfound2.iloc[[x]]
        while y == 0:
            try:
                y = int(input('\nHow many?: '))
                if y == 0:
                    return
                if y > int(item2['Stock']):
                    print('Over the stock!')
                    return
                cartdf = cartdf.append(item2, ignore_index= True)
                if cartdf['Product'].duplicated().any():
                    cartdf.at[len(cartdf.index) -1,'Stock'] = y
                    cartdf['Stock'] = cartdf.groupby(['Product'])['Stock'].transform('sum')
                    return
                cartdf.at[len(cartdf.index) -1,'Stock'] = y
            except:
                print('\nItem is in Cart!')
                return
        if y > 0:
            print('\n' + item + ' Added to Cart\n')
        return

#Search function
def searchproduct(data):    
    global cartdf
    x = 0
    y = 0
    target= 'NaN'
    list = ['Shop','Product','Price','Stock']
    datax = data['Product'].str.lower()
    datay = data
    datay.index += 1
    datalist = datay[list]
    datax.index += 1
    while target != "0":
        try:
            print('\n==================================\nSearch Products\n==================================')
            print(datay)
            print('\n[0] Return')
            target= input('Name of Product: ')
            if target == "0":
                return
            datafound= datax[datax.str.contains(target, case= False)] #datafound is the list the system is using, datafound2 is for menu design              
            datafound2= datay.iloc[datafound.index - 1]
            datafound.reset_index(drop= True ,inplace= True)
            datafound2.reset_index(drop= True ,inplace= True)
            datafound.index += 1
            datafound2.index += 1
            print('\n==================================\n'+ 'Results for ' + target + '\n==================================')
            print(datafound2)
            print('\n[0] Return')
            while x == 0:
                try:
                    x = int(input("Select product: "))
                    if x == 0:
                        print('\n')
                        break
                    x = x-1
                    item = datafound.iloc[x]
                    item2 = datafound2.iloc[x]
                    while y == 0:
                        try:
                            y = int(input('\nHow many?: '))
                            if y == 0:
                                return
                            if y > int(item2['Stock']):
                                print('Over the stock!')
                                return
                            cartdf = cartdf.append(item2, ignore_index= True)
                            if cartdf['Product'].duplicated().any(): #Add to stock
                                cartdf.at[len(cartdf.index) -1,'Stock'] = y
                                cartdf['Stock'] = cartdf.groupby(['Product'])['Stock'].transform('sum')
                                return
                            cartdf.at[len(cartdf.index) - 1,'Stock'] = y
                        except:
                            print('\nItem is in Cart!')
                            return
                        if y > 0:
                            print('\n' + item + ' Added to Cart\n')
                            return
                    print('\n' + item + ' Added to Cart\n')
                except:
                    print('\nInvalid Index')

        except:
            print('\n404 Error')
            continue

#Viewing/Removing Item Function
def cart():
    global cartdf
    x = None
    itemselected = None
    headery = ['Shop','Product','Price','Stock']
    cartdflist = cartdf['Product'].dropna()
    cartdf = cartdf.drop_duplicates(subset= ['Product'])
    cartdf.reset_index(drop= True, inplace= True)
    cartdf.index += 1
    while x != "0":
        print('\n==================================\nCart\n==================================')
        if cartdf.empty:
            print("\nCart is Empty!")
            print('\n[0] Return')
        else:
            print(cartdf[headery])
            print('\n[0] Return')
            print('\n[1] Remove Item')
        x = input('Input: ')
        if x == "1" and ~cartdf.empty:
            print('\n==================================\nRemoving Item\n==================================')      
            print(cartdf[headery])
            print('\n[0] Return')
            x = input('\nSelect an item: ')
            if x == "0":
                return
            x = int(x) - 1
            itemselected = cartdf.iloc[x]
            y = 0
            while y <= 0:
                try:
                    y = int(input('How many?: '))
                    reduction = int(itemselected['Stock'])
                    result = reduction - y
                    cartdf.at[x + 1,'Stock'] = result 
                    if int(itemselected['Stock']) == 0:
                        cartdf = cartdf.drop([x+1])
                        print("dropped")
                    cartdf.reset_index(drop= True, inplace= True)
                    cartdf.index += 1
                except:
                    print("\nInput Error")
                
    return

#Calculation and Receipt output
def checkout():
    global cartdf
    cartdf = cartdf.drop_duplicates(subset= ['Product'])
    cartdf.reset_index(drop= True, inplace= True)
    x = 0 #User Input
    print('\n==================================\nCheckout\n==================================') 
    print('\n\nDo you have a senior citizen ID?\n[1] Yes\n[2] No\n')
    while x == 0: #This is for checking the input if int or not
        try:
            x = int(input('\nChoice: '))
        except ValueError:
            print('\nInvalid Choice')
            pass
    if x == 1: #Senior Citizen Discount True
        if cartdf.empty:
            print('\n==================================\nCheckout\n==================================') 
            print('\nCart is Empty!')
        else:
            print('\n==================================\nCheckout\n==================================')
            print(cartdf)
        print('\nAre you sure of your order?\n[1] Yes\n[0] No')
        x = input('\nInput: ')
        if x == '0':
            return
        elif x == '1':
            checkout2(True)
    elif x == 2: #No Discount
        if cartdf.empty:
            print('\n==================================\nCheckout\n==================================') 
            print('\nCart is Empty!')
        else:
            print('\n==================================\nCheckout\n==================================')
            print(cartdf)
        print('\nAre you sure of your order?\n[1] Yes\n[0] No')
        print('*Delivery fee will be applied')
        x = input('\nInput: ')
        if x == '0':
            return
        elif x == '1':
            checkout2(False)

def checkout2(bool):
    global cartdf
    categorylist = ['Food Stores.csv','Pharmacy Stores.csv','Grocery Stores.csv','School supplies Stores.csv']
    reducedstock = 0
    try:
        for category in categorylist:
            listx= pd.read_csv(category)
            baselist = listx[header]
            cartlist = cartdf[header].values.tolist()
            for item in cartlist:   
                itemname = item[1]
                x = baselist.loc[baselist['Product'].str.contains(itemname, case= False)]
                try:
                    reducedstock = int(x['Stock']) - int(item[3])
                except:
                    pass
                baselist.at[x['Stock'].index, 'Stock'] = reducedstock
            baselist.to_csv(category)
        if bool == False:
            sum = cartdf['Price'] * cartdf['Stock']
            cartdf['Total'] = sum
            cartdf.loc['Total'] = pd.Series(cartdf['Total'].sum(),index= ['Total'])
        elif bool == True:
            sum = cartdf['Price'] * cartdf['Stock']
            discount =  (cartdf['Price'] * 0.2) * cartdf['Stock']
            cartdf['Total'] = sum - discount
            cartdf.loc['Total'] = pd.Series(cartdf['Total'].sum(),index= ['Total'])
        cartdf.to_csv('Reciept.csv')
        print("\n==================================\nReciept\n==================================")
        print(cartdf)   
        print("\nReceipt.csv has been printed\nThank you for Shopping at Pasabuy!\n")
        cartdf.drop(cartdf.index, inplace= True)
        cartdf.drop(['Total'], axis = 1)

    except Exception as e:
        print(e)
        print('error 2')
    
        
       

