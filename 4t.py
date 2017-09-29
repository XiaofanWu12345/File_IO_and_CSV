# Xiaofan Wu 903152422

import xml.etree.ElementTree as et

def read_tree(filename):
    """This function will read in the existing xml file and return a dictionary.
    The keys to the dictionary will be the sectors found in the xml file
    The value of each key will be another dictionary!
    This dictionary's keys will be the industries that make up that particular sector.
    The value of each key will be a list of the xml elements in the original tree for the stocks 
    that make up that industry.
    
    Parameters: 
    filename: str - name of the existing xml file
    
    Return: dict which will be in the format above. 
    """
    f = et.parse(filename)
    symbols = f.getroot()
    iedict = {}
    for symbol in symbols:
        if symbol.attrib["industry"] not in iedict.keys():
            iedict[symbol.attrib["industry"]]=[symbol]
        else:
            iedict[symbol.attrib["industry"]].append(symbol)
    sidict = {}
    for symbol in symbols:
        if symbol.attrib["sector"] not in sidict.keys():
            sidict[symbol.attrib["sector"]] = [symbol.attrib["industry"]]
        else:
            sidict[symbol.attrib["sector"]].append(symbol.attrib["industry"])
    fdict = {}
    for s in sidict.keys():
        fdict[s]={i:iedict[i] for i in sidict[s]}
    return fdict

def create_tree(xml_dict):
    """This function takes in the dictionary you created in read_tree
    Iterate through the dictionary, and create an xml tree in the format described in the assignment
    Write that tree to a file called "output.xml"
    
    Parameters:
    xml_dict: dict - the dictionary you created in read_tree
    
    Return: none
    """
    sp500 = et.Element('SP500')
    for s in xml_dict.keys():
        sector = et.Element('Sector',name=s)
        sp500.append(sector)
        for i in xml_dict[s].keys():
            industry = et.Element('Industry',name=i)
            sector.append(industry)
            for st in xml_dict[s][i]:
                stock = et.Element('Stock',ticker=st.attrib["ticker"])
                stock.text = st.attrib["name"]
                industry.append(stock)
    outTree = et.ElementTree(sp500)
    outTree.write("output.xml")


import csv
def read_CSV(filename):
    """This function will read in the csv file, and return a list of lists. 
    Each list will be in the following format:[date, ticker, open, high, low, close, volume]. 
    The date should be in the form of a datetime object - (hint: look at datetime.datetime.strptime). 
    The ticker should be a string. The five numbers should be floats.
    
    Parameters:
    filename: str - csv file to be read
    
    Return: a nested list in the format specified above
    """
    with open(filename,'r') as f:
        rows = csv.reader(f)
        alist = [row for row in rows]
        alist = alist[1:]
    import datetime as dt
    for row in alist:
        row[0] = dt.datetime.strptime(row[0],'%Y%m%d')
        row[2] = float(row[2])
        row[3] = float(row[3])
        row[4] = float(row[4])
        row[5] = float(row[5])
        row[6] = float(row[6])
    return alist

def stock_dictionary(csv_list):
    """This function will take in the list of lists created in read_CSV and return a dictionary. 
    Each key will be a stock ticker. Each value will be a list of lists, with each list in the format 
    [dateObj, open, high, low, close, volume]. Each value should only contain information pertinent to 
    the corresponding key.
    
    Parameters:
    csv_list: list - nested list that was created in read_CSV
    
    Return: a dictionary with the information of the nested list

    Usage Examples:
    >>> alist = [[(2010,4,26,0,0),'ZMH',12,12,12,11.1,1.1],[(2011,4,26,0,0),'ZMH',12,12.3,12,11.1,1.1]]
    >>> stock_dictionary(alist)
    {'ZMH': [[(2010, 4, 26, 0, 0), 12, 12, 12, 11.1, 1.1], [(2011, 4, 26, 0, 0), 12, 12.3, 12, 11.1, 1.1]]}
    """
    adict = {}
    for item in csv_list:
        if item[1] not in adict.keys():
            adict[item[1]]= [item[:1] + item[2:]]
        else:
            adict[item[1]].append(item[:1] + item[2:])
    return adict

def calc_avg_open(stock_dict, ticker):
    """This function takes in the dictionary you created in stock_dictionary and a ticker.  
    Return the average opening price for the stock as a float.
    
    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock
    
    Return: float which is the average opening price of the stock

    Usage Examples:
    >>> adict = {'ZMH': [[(2010, 4, 26, 0, 0), 12, 12, 12, 11.1, 1.1], [(2011, 4, 26, 0, 0), 13, 12.3, 12, 11.1, 1.1]]}
    >>> calc_avg_open(adict, 'ZMH')
    12.5
    """
    alist = stock_dict[ticker]
    blist = [item[1] for item in alist]
    avg = sum(blist)/len(blist)
    return avg

def find_return(stock_dict, ticker, start, end):
    """This function takes in the stock dictionary, a ticker, and two tuples.  The tuples
    represent dates, where each item in the tuple is an int.  
    It calculates the return of the stock between the two dates.  Calculate the return using
    the formula: (endPrice - startPrice)/startPrice. 
    Use the opening price on the starting date, and the closing price on the ending date. 
    Return this value as a float.
    In the event that there is no data for either of the two dates, print a message notifying user and
    return None.
    
    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock
    start: tuple - represents the start date in the format (Month,Date,Year)
    end: tuple - represents the end date in the format (Month,Date,Year)
    
    Return: float of the mathematical return
    """
    import datetime as dt
    s = dt.datetime.strptime(str(start),'(%m,%d,%Y)')
    e = dt.datetime.strptime(str(end),'(%m,%d,%Y)')
    try:
        for item in stock_dict[ticker]:
            if item[0] == s:
                startPrice = item[1]
            if item[0] == e:
                endPrice = item[-2]
        r = (endPrice - startPrice)/startPrice
        return r
    except:
        print("No data found for the start or the end date.")
        return None

def vwap(stock_dict, ticker):
    """This function takes in the stock dictionary and a ticker.  Return the volume weighted average
    price (VWAP) of the stock.  In order to do this, first find the average price of the stock on
    each day.  Then, multiply that price with the volume on that day.  Take the sum of these values.  
    Finally, divide that value by the sum of all the volumes.  
    (hint: average price for each day = (high + low + close)/3)
    
    Parameters:
    stock_dict: dict - created in the stock_dictionary function
    ticker: str - refers to a specific stock
    
    Return: float which is the VWAP of the stock
    """
    num_total = 0
    num_volume = 0
    for item in stock_dict[ticker]:
        num_total = num_total + (sum(item[2:5])/3)*item[-1]
        num_volume += item[-1]
    vwap = num_total/num_volume
    return vwap

def ticker_find(tree_dict, info):
    """This function takes in the dictionary created in read_tree and a tuple that contains a
    sector and an industry that belongs to that sector.  Return a list of tickers of the stocks that belong
    to that industry.
    
    Parameters:
    tree_dict: dict - created in the read_tree function
    info: tuple - in the format (sector, industry)
    
    Return: list of tickers that belong to that industry
    """
    info_list = list(info)
    stock_list = tree_dict[info_list[0]][info_list[1]]
    tickers_list = [item.attrib["ticker"] for item in stock_list]
    return tickers_list

def main(args):
    """This function should have perform all of the tasks outlined above.
    
    Parameters:
    first: str - filename of given xml file ~ (SP_500.xml for us)
    second: str - filename of given csv file ~ (SP500_ind.csv for us)
    third: str - sector name
    fourth: str - industry name
    fifth: str - name of output csv file (OPTIONAL)
    
    Return: none
    """
    try:
        tree_dict = read_tree(args[1])
        csv_list = read_CSV(args[2])
        create_tree(tree_dict)
        ticker_info_dict = stock_dictionary(csv_list)
        tickerlist = ticker_find(tree_dict,(args[3],args[4]))
    except:
        print("Error! The arguments entered are invalid.")
        return
    try:
        with open(args[5],'wt',newline='') as f:
            fin = csv.writer(f)
            for t in tickerlist:
                if t in ticker_info_dict.keys():
                    v = vwap(ticker_info_dict,t)
                    ao = calc_avg_open(ticker_info_dict,t)
                    fin.writerow([t,v,ao])
    except:
        for t in tickerlist:
            if t in ticker_info_dict.keys():
                v = vwap(ticker_info_dict,t)
                ao = calc_avg_open(ticker_info_dict,t)
                print(t+" "+str(v)+" "+str(ao))
    
        


if __name__ == "__main__":
    import sys
    main(sys.argv)



            


        


