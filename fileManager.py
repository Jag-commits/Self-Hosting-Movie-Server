class fileManager:
    def readInformation(filepath:str):
        names=[""]
        TMDBname={}
        index=1
        movieset=[]
        with open(filepath, encoding="utf-8") as file:
            for line in file:
                title, id = line.strip().split(',')
                names.append(title)
                TMDBname[index]=id
                movieset.append(index)
                index+=1
        return(movieset,names,TMDBname)
filepath="F:\coding and stuff\Html\Movies copy\storage\movies.txt"
print(fileManager.readInformation(filepath))
import os
print("🔍 Current working directory:", os.getcwd())