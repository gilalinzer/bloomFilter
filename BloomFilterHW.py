from BitHash import *
import cityhash
from BitVector import *

class BloomFilter(object):
    
    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        # proportion of bits set would be:
        proportion = (1-(maxFalsePositive**(1/numHashes)))
        # therefore we can calculate length we need by doing:
        return int(numHashes/(1-(proportion**(1/numKeys))))
        
    def __init__(self,numKeys,hashes, maxFalsePositive):
        # bit vector object that sets the bits 
        self.__BloomVector = BitVector(size = self.__bitsNeeded(numKeys,hashes,maxFalsePositive))
        self.numKeys = numKeys
        self.hashes = hashes
        self.__length = self.__bitsNeeded(numKeys,hashes,maxFalsePositive)
        # keeps track of how many bits have been set 
        self.__bitsSet = 0
        
    
    # hashes the inputted string into the bit vector 
    def insert(self,string):
        # we want to hash hash times 
        for i in range(self.hashes):
            # hash the string
            hashNum = BitHash(string,i+1) % len(self.__BloomVector)
            # if the bit is not already set 
            if self.__BloomVector[hashNum] != 1:
                # set and increment our counter 
                self.__BloomVector[hashNum]= 1
                self.__bitsSet+=1
    
    # accessor method that returns the number of bits set in the vector
    def bitsSet(self):
        return self.__bitsSet
    
    # accessor method that checks to see if a given string is in a bloom filter. 
    # returns false if it is not and true if it is (however there may 
    # be a false positive)
    def find(self, string): 
        for i in range(self.hashes):
            # hash the string
            hashNum = BitHash(string,i+1) % len(self.__BloomVector)
            
            # if we encounter any zeros it's not possible the word was inserted
            if not self.__BloomVector[hashNum]: return False 
        # no zeros were encountered so return true 
        return True
    
    def falsePositiveRate(self):
        # bits still zero is the length - bits actually set / length 
        proportion = (self.__length-self.bitsSet())/self.__length
        # using equation
        return (1-proportion)**self.hashes
    
def __main():
    
    
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
        
    b = BloomFilter(numKeys,numHashes,maxFalse)
    data =open("wordlist.txt")
    
    # insert first 100,000 words 
    for i in range(100000):
        line = data.readline()
        b.insert(line)
    data.close()

    
    print("False positive rate estimate: "+"{:.2%}".format(b.falsePositiveRate()))
    
    # now let's open the list again and make sure we can find the first 100000 words
    data =open("wordlist.txt")
    
    for i in range(100000):
        line = data.readline()
        if not b.find(line): print( "error not found")
        
    
    # now let's read the next 100,000 words and find them 
    count = 0
    for i in range(100000):
        line = data.readline()
        if b.find(line): count+=1
    
    data.close()
    # now lets calculate the actual number of false positives which is the 
    # number of positives divided by 100,000 words we tried to find 
    actual = count/100000
    
    print("Actual false positives: "+"{:.2%}".format(actual))
    
    
    
    
    
    
if __name__ == '__main__':
    __main()  
    
    
    
    
    
    
        
        
        
        
    
    