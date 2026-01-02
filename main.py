import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, select
from datetime import datetime

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

engine = create_engine(
    #To be filled later,
    echo = True
)

Base = declarative_base()

#Database Model
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(Text)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    moods = relationship("Mood", secondary="movie_moods", back_populates="movies")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete")

class Mood(Base):
    __tablename__ = "moods"

    id = Column(Integer, primary_key=True)
    mood_name = Column(String(255), unique=True, nullable=False)

    movies = relationship("Movie", secondary="movie_moods", back_populates="moods")

class MovieMood(Base):
    __tablename__ = "movie_moods"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    mood_id = Column(Integer, ForeignKey("moods.id", ondelete="CASCADE"), primary_key=True)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    review = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie", back_populates="reviews")

# Pydantic models for request validation
class ReviewCreate(BaseModel):
    review: str

class MovieRecommendationRequest(BaseModel):
    moods: list[str]
    preference: str
    personalNotes: str
    timestamp: str


#Code that does the web scapping here


