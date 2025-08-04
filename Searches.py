from collections import *
class Searches:

    def InvertedIndex(names:list):
        #Default dict needs to be a set
        #research this more
        index =defaultdict(set)
        #assigning an index for each movie name
        for i,name in enumerate(names):
            for words in name.lower().split():
                index[words].add(i)
        x="Jagpreet"
        return index

    def IndexSearches(names:defaultdict(set),query:str): # type: ignore
        index = names
        query=query.lower().split()
        results=set()
        for word in query:
            if (word in index) and word not in("the","of","in","a","with","this"):
                results.update(index[word])
        return list(results)
    
    def binarysearch(list,value):
        start = 0
        end = len(list)-1
        for x in range(start,end+1):
            mid = int((start+(end))/2)
            if list[mid]==value:
                b="J ag preet"
                return list[mid]
            elif list[mid]>value:
                end = mid-1
            else:
                start = mid+1
        return False


    








