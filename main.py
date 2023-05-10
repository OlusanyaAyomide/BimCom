import psycopg2
import random

class ColorAnalyis:
    def __init__(self):
        mondayWears = ['GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'BLUE', 'YELLOW', 'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'GREEN']
        tuesdayWears = ['ARSH', 'BROWN', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLUE', 'PINK', 'PINK', 'ORANGE', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'WHITE', 'BLUE', 'BLUE', 'BLUE']
        wednesdayWears =['GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'RED', 'YELLOW', 'ORANGE', 'RED', 'ORANGE', 'RED', 'BLUE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'WHITE', 'WHITE']
        thursdayWears = ['BLUE', 'BLUE', 'GREEN', 'WHITE', 'BLUE', 'BROWN', 'PINK', 'YELLOW', 'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'GREEN']
        fridayWears  = ['GREEN', 'WHITE', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLACK', 'WHITE', 'ORANGE', 'RED', 'RED', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'WHITE']
        self.numberList = [1,4,5,3,5,6,7,7,4,10,33,9,29,20,9,36,18,89,0,4]

        self.clothingList =[mondayWears,tuesdayWears,thursdayWears,wednesdayWears,thursdayWears,fridayWears]
        
        #Generate a unique number for every color in the list
        self.color_dict ={}
        for days in self.clothingList:
            for color in days:
                if not color in self.color_dict:
                    self.color_dict[color] = len(self.color_dict) + 1

    #Returns the mean color basedon the keys assigned to each string
    def getmeanColor(self) -> str:
        colorList =[]
        for days in self.clothingList:
            for color in days:
                colorList.append(self.color_dict[color])
        meanValue= round(sum(colorList)/len(colorList))
        for key,value in self.color_dict.items():
            if value == meanValue:
                return f'Mean Color is {key}'
            
    #Returns Most worn Color clothe
    def getMostWorn(self):
        frequencyTracker = {}
        for days in self.clothingList:
            for color in days:
                if not color in frequencyTracker:
                    frequencyTracker[color] = 1
                else:
                    frequencyTracker[color] +=1
        mostWorn = max(frequencyTracker, key=frequencyTracker.get)
        self.saveToDatabase(frequencyTracker)
        return f'Most worn clothe color is {mostWorn} with {frequencyTracker[mostWorn]} occurence'

    #Sorts Alphabetically and returns Median Value(s)

    def getColorProbability(self):
        color= "RED"
        count =0
        frequencyTracker = {}
        for days in self.clothingList:
            for color in days:
                count+=1
                if not color in frequencyTracker:
                    frequencyTracker[color] = 1
                else:
                    frequencyTracker[color] +=1     
        return round((frequencyTracker[color]/count),3)


    def getMedianColor(self):
        colorList = []
        for days in self.clothingList:
            for color in days:
                colorList.append(color)
        
        sortedList = sorted(colorList)
        sortedLength = len(sortedList)
        midValue = len(sortedList)//2

        
        if not sortedLength % 2 == 0:
            return f"Median Value is {sortedList[midValue]}" 
        if sortedList[midValue] == sortedList[midValue+1]:
            return f'Median Color is {sortedList[midValue]} ' 
        return f'Median values are {sortedList[midValue]} and {sortedList[midValue+1]}'  

    #using the varuance formula,the variance is returned
    def getVariance(self):
        colorList =[]
        DeviationfromMean = []
        for days in self.clothingList:
            for color in days:
                colorList.append(self.color_dict[color])
        meanValue=(sum(colorList)/len(colorList))
        for numbers in colorList:
            value = (numbers - meanValue)**2
            DeviationfromMean.append(value)
        variance = round(sum(DeviationfromMean)/(len(DeviationfromMean) - 1))
        for key,value in self.color_dict.items():
            if value == variance:
             return f'Variance is {key}'

    def saveToDatabase(self,frequency):
        print("saving to dbb",frequency.items())
        conn = psycopg2.connect(
        host="localhost",
        database="user",
        user="userAyomide",
        password="mypassword"
    )
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS colorCounts (color TEXT PRIMARY KEY, count INTEGER)")


        # Insert the data into the table
        for color, count in frequency:
            cur.execute("INSERT INTO coloCounts (color, count) VALUES (%s, %s) ON CONFLICT DO NOTHING", (color, count))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and database connection
        cur.close()
        conn.close()


    #Generates randum zeros and 1's and convert to base10
    def Base10generator(self):
        randInt = ""
        for i in range(0,4): 
            randInt += str(random.randint(0,1))
        return int(randInt)

    #Search for numbers using recursive function
    def searchNumbers(self):
        usernput = input("Enter Number to Search ")
        try:
            userinput = int(usernput)
        except:
            return("User input Invalid")
        foundIn = []
        def recursive(count):
            if count < len(self.numberList) :
                if not userinput == self.numberList[count]:
                    return recursive(count+1)
                else:
                   foundIn.append(count)
                   return recursive(count+1) 
            if  len(foundIn) == 0:
                return f"Number does not exits in list"
            indices_str = ', '.join(str(i) for i in foundIn)
            return f'{userinput} can b found in index {indices_str}'
        return recursive(0)

    #Generate fibonanci Sequence
    def fibonacci(self,n):
        #initialzize first sequence
        fib = [0, 1] 
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

                



colorObject = ColorAnalyis()
print(colorObject.getMedianColor())
print(colorObject.getMostWorn())
print(colorObject.getColorProbability())
print(colorObject.searchNumbers())
print(colorObject.getVariance())
print(colorObject.getmeanColor())
print(colorObject.Base10generator())
print(colorObject.fibonacci(50))
