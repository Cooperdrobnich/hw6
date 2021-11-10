import json
import unittest
import os
import requests

#
# Your name: Cooper Drobnich
# Who you worked with: Adam Brenner
#

# generating personal API key is not requested here

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    When you write cache into JSON format, you need to unpack the second item of your dictionary, which is 
    the actual content of your item. For example: 

    {'resultCount': 2, 'results': [{*INFORMATION ABOUT EACH ITEM*},{*INFORMATION ABOUT EACH ITEM*}]}

    In the above case, the resultCount is 2 because we set the limit number to be 2. For this assignment, we set resultCount to be 1. 
"""
    with open(CACHE_FNAME, "w") as file:

        json.dump(CACHE_DICT, file)

    

    
    
    


def create_request_url(term, number=1):
    """
    This function prepares and returns the request url for the API call.  
    The documentation of the API parameters is at  
    https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

    See more details in the instructions file.

    """
    base = 'https://itunes.apple.com/search?term={}&limit={}'
    request_url = base.format(term, number)
    return request_url
    
def get_data_with_caching(term, CACHE_FNAME): 
    """
    This function uses the passed term (e.g., Billie+Eilish) to first generate a request_url (using the create_request_url function).
    It then checks if this url is in the dictionary returned by the function read_cache.
    If the request_url exists as a key in the dictionary, it should print "Using cache for <term>"
    and return the results for that request_url.

    If the request_url does not exist in the dictionary, the function should print "Fetching data for <term>"
    and make a call to the Search API to get the data for that specific term.

    If data is found for the term, it should add them to a dictionary (key is the request_url, and value is part of the results)
    and write out the dictionary to a file using write_cache.

    If the request_url is not generated correctly (e.g., for some reason the limit number is not 1) and thus returns zero or multiple items, 
    do not write this data into the cache file. Instead, print “Request not set correctly” and return None.

    If there was an exception during the search (for reasons such as no network connection, no results are returned), 
    it should print out “Exception” and return None.
    """
    
    request_url = create_request_url(term, 1)
    dic = read_cache(CACHE_FNAME)
    if request_url in dic:
        print(f"Using cache for {term} ")
        return dic
    else:
        print(f"Fetching data for {term}")
        r = requests.get(request_url).text
        new_dic = json.loads(r)
        try:
            dic[request_url] = new_dic['results'][0]
            write_cache(CACHE_FNAME, dic)
            if len(dic['results']) != 1:
                print("Request not set correctly")
                return None
        except:
            print("Exception")
            return None

        





def sort_collectionid (CACHE_FNAME):
    """
     This function sorts a list of items based on collectionId in ascending order and 
     returns the collection price for the item with the smallest collectionId.

    """
    collections = read_cache(CACHE_FNAME)
    lst = []
    for i in collections:
        id = collections[i]['collectionId']
        lst.append(id)
    x = sorted(lst)[0]

    dic = dict(sorted(collections.items(), key=lambda t: t[0]))
    for i in dic:
        if dic[i]['collectionId'] == x:
            price = dic[i]['collectionPrice']
    return price

    
    

    
    
    
    
        


#######################################
############ EXTRA CREDIT #############
#######################################
def itunes_list():
    """
    The function calls read_cache() to get the iTunes data stored in extra_credit.json. 
    It analyzes the dictionary returned by read_cache(). 
    This function returns a tuple with two items: the first is a new dictionary with the primaryGenreName as the key and number of items with that genre as the value; 
    the second is the genre name with most items. 

    Expected results should be: 
    ({'Electronic': 1, 'Pop': 6, 'Hip-Hop/Rap': 1, 'Rock': 2, 'Alternative': 3, 'Country': 1, 'Drama': 1, 'Hip-Hop': 1, 'Biographies & Memoirs': 1, 'Dance': 1}, “Pop”)

    """
    





#######################################
#### DO NOT CHANGE AFTER THIS LINE ####
#######################################

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.CACHE_FNAME = dir_path + '/' + "cache_itunes.json"
        self.term_list = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
        self.cache = read_cache(self.CACHE_FNAME)

    def test_write_cache(self):
        write_cache(self.CACHE_FNAME, self.cache)
        dict1 = read_cache(self.CACHE_FNAME)
        self.assertEqual(dict1, self.cache)

    def test_create_request_url(self):
        for m in self.term_list:
            self.assertIn("term={}".format(m),create_request_url(m))
            self.assertIn("limit=1",create_request_url(m))
            self.assertNotIn("r=json",create_request_url(m))
            

    def test_get_data_with_caching(self):
        for m in self.term_list:
            dict_returned = get_data_with_caching(m, self.CACHE_FNAME)
            if dict_returned:
                self.assertEqual(type(dict_returned), type({}))
                self.assertIn(create_request_url(m),read_cache(self.CACHE_FNAME))
            else:
                self.assertIsNone(dict_returned)       
        self.assertEqual(json.loads(requests.get(create_request_url(self.term_list[0])).text)["results"][0],read_cache(self.CACHE_FNAME)[create_request_url(self.term_list[0])])

    def test_sort_collectionid(self):
        self.assertEqual(sort_collectionid(self.CACHE_FNAME), 3.99)
        

'''
    ######## EXTRA CREDIT #########
    # Keep this commented out if you do not attempt the extra credit
    # Writing test case for the extra credit is not required but highly recommended.
    def test_itunes_list(self):
        pass 

'''

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_itunes.json"

    terms = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
    [get_data_with_caching(term, CACHE_FNAME) for term in terms]
    print("________________________")
    # Fetch the data for ColdPlay!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('cold+play', CACHE_FNAME)
    data2 = get_data_with_caching('cold+play', CACHE_FNAME)
    print("________________________")

    # Getting the data for Post Malone!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('post+malone', CACHE_FNAME)
    data2 = get_data_with_caching('post+malone', CACHE_FNAME)
    print("________________________")

    # Getting the data for The Beatles
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('the+beatles', CACHE_FNAME)
    data2 = get_data_with_caching('the+beatles', CACHE_FNAME)
    print("________________________")

    print("Get CollectionPrice for first 5 items")
    print(sort_collectionid(CACHE_FNAME))
    print("________________________")


    # Extra Credit
    # Keep the statements commented out if you do not attempt the extra credit
    #print("EXTRA CREDIT!")
    #print("Analyzing the distribution of item genres")
    # itunes_list() function does not take any parameters.
    #print(itunes_list())
    #print("________________________")
    
 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    unittest.main(verbosity=2)
