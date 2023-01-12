Q= {"How fast did the fastest spaceship to date go?": "165,000 mph", "What is Microsoft's virtual assistant called?": "Cortana", 'True or False: Diesel engines are less efficient than gasoline engines.': "False" ,"What is the most common car engine?" : "The piston engine" , "How many pounds of thrust does the Space Shuttle consume every second?": "11,000 pounds","True or false: There are only 4 forces of flight.": "True" , "True or false: drones do not need gyroscopes to fly.":"False", "How many Orkney islands are inhabited?" : "20" , "What is the most common coding language?": "Python", "True or false: Google Searches are mostly based of C++ and Python.": "True"}
wrong=0
for n in Q.keys():
    print(n)
    answer=input()
    if answer == Q[n]:
        print("You got it Correct!")
    else:
        print("Sorry, try again! Correct answer:" ,Q[n])
        wrong=wrong+1
print("Your final score is",10-wrong,"out of 10. Good Job!")
