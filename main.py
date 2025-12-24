import requests
import sqlalchemy

def apimoviecall(title, year=None):
    
    try: 
        apikey = "2c6bd367"
        plot = "full"

        #Sending requesting for the data
        params = {
            "t" : title,
            "apikey" : apikey,
            "plot" : plot,
            "y" : year,
        }

        response = requests.get("https://www.omdbapi.com/", params=params)
        data = response.json()

        return data
    
    except Exception as e:

        return print(f"An unexpected error occurred: {e}")

def moviedatadisplay(data):
    print()
    print(data['Title'])
    print(data['Plot'])
    print()

#Block of code that  retrieved data of the movie inputed
title = None
while title == None:
    title= str(input("Name of the movie: "))
    print("Input Title is: " + title)
    data = apimoviecall(title)

check = False
while check != True:
    moviedatadisplay(data)
    print("Input y if movie retrieved in correct")
    print("Input n if movie retrieved is not the correct one")
    answer = str(input("Input: "))

    if answer.lower() == "y":
        print("Confirmed that movie retrieve is correct.")
        check = True

    else:
        year = input("What year is it released? Input: ")
        data = apimoviecall(title, year)
            

#Store Data in the dataset code here 
print("Sending data to database")


#Code that does the web scapping here


