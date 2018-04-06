from ultrasonic import steph
distanceFromStart=0
possibleDogLocations=[True, True, True, False]
oldDistances=[]
def moveForward(distance):
  global distanceFromStart
  global moved
  moved=True
  distanceFromStart+=distance
  input()
  print(distanceFromStart)

#this is the value that will be returned when added to the overall program that is the estimated start position of the robot
#current location, direction, original location
ret=[0,0,0]
def findLocation():
  import pickle
  from array import array
  print("start")
  
  distanceTable=array("i")
  with open("noDog.txt", 'rb') as pickleFile:
    distanceTable = pickle.load(pickleFile)
  
  def getDistances():
    #return the distances in the order: up, upright, right...
    #the distances must also be corrected to be as if they were coming from the center of the robot(that should be simple addition)
    '''
    y=80
    x=180
    start=y*1952+x*8
    a=[80, 0, 10, 20, 0, 55, 0]
    '''
    global moved
    if(moved):
        global oldDistances
        oldDistances=steph()
        moved=False
    return oldDistances
  print(getDistances())
  
  #this is the acceptable uncertainty for exactly where the robot is in cm. This should be greater than or equal to ERRORTHRESHOLD
  ACCEPTABLEUNCERTAINTY=20
  
  #this is the distance which the robot moves per check. Please note the program does not deal with turns but this can be added with a few hours work
  MOVEDISTANCE=10
  
  #this value is the cumalative error threshold for the ultrasonics
  #with the ignore a single direction thing, this needs to be less than 10 to work well
  #I will be working on removing the remove a wall thing today (Apr 3)
  ERRORTHRESHOLD=20

  
  dogTop=array("i")
  with open("dogTop.txt", 'rb') as pickleFile:
    dogTop = pickle.load(pickleFile)
  
  dogRight=array("i")
  with open("dogRight.txt", 'rb') as pickleFile:
    dogRight = pickle.load(pickleFile)
  
  dogBottom=array("i")
  with open("dogBottom.txt", 'rb') as pickleFile:
    dogBottom = pickle.load(pickleFile)
    
  dogDifsBottom=array("i")
  with open("dogDifsBottom.txt", 'rb') as pickleFile:
    dogDifsBottom = pickle.load(pickleFile)
    
  print(len(distanceTable))
  
  walls=array("i")
  with open("noDogWalls.txt", 'rb') as pickleFile:
    walls = pickle.load(pickleFile)
  
  dogDifs=array("i")
  with open("dogDifs.txt", 'rb') as pickleFile:
    dogDifs = pickle.load(pickleFile)
  
  dogDifsRight=array("i")
  with open("dogDifsRight.txt", 'rb') as pickleFile:
    dogDifsRight = pickle.load(pickleFile)
  #this checks whether the given position is fits with the given distance array
  def checkPosition(position, dirdis, distanceTable):
    skip=[3,5]
    dif=0
    for i in [0,2,4,6]:
        dif+=abs(distanceTable[position*8+i]-dirdis[i])
        if(dif>ERRORTHRESHOLD):
          return False
    return True
  def checkPositionWithDog(position, dirdis):
    walls=checkPosition(position, dirdis, distanceTable)
    '''
    global possibleDogLocations
    if(not possibleDogLocations[3]):
      if(dogDifs[position]!=0):
        top=False
        right=False
        bottom=False
        if(dogDifs==1):
          top=checkPosition(position, dirdis, dogTop)
        if(dogDifsRight==1):
          right=checkPosition(position, dirdis, dogRight)
        if(dogDifsBottom==1):
          right=checkPosition(position, dirdis, dogBottom)
        if(not walls):
          if(top^right^bottom):
            if(top):
              possibleDogLocations=[True, False, False, True]
            if(right):
              possibleDogLocations=[False, True, False, True]
            if(bottom):
              possibleDogLocations=[False, False, True, True]
        else:
          if(not top):
             possibleDogLocations[0]=False
          if(not right):
            possibleDogLocations[1]=False
          if(not bottom):
            possibleDogLocations[2]=False
          if(possibleDogLocations[0]^possibleDogLocations[1]^possibleDogLocations[2]):
            possibleDogLocations[3]=True
            '''
    return walls
  print(distanceTable[201919])
  print(checkPositionWithDog(20919, getDistances()))
  #this class stores and handles each individual location
  class Location:
    def __init__(self, position, dirdis):
      self.position=position
      if(checkPositionWithDog(position,dirdis)):
        self.up=[position]
      else:
        self.up=None
        
      #these lines cycle the location array by 90 degrees
      dirdis=dirdis[-2:]+dirdis[:-2]
      if(checkPositionWithDog(position,dirdis)):
        self.right=[position]
      else:
        self.right=None
        
      
      dirdis=dirdis[-2:]+dirdis[:-2]
      if(checkPositionWithDog(position,dirdis)):
        self.down=[position]
      else:
        self.down=None
        
        
      dirdis=dirdis[-2:]+dirdis[:-2]
      if(checkPositionWithDog(position,dirdis)):
        self.left=[position]
      else:
        self.left=None
        
        
    def update(self, dirdis):
      global distanceFromStart
      position=self.position
      if(self.up!=None):
        position-=244*distanceFromStart
        if(position>0 and checkPositionWithDog(position, dirdis)):
          self.up.append(position)
        else:
          self.up=None
          
      dirdis=dirdis[-2:]+dirdis[:-2]
      position=self.position
      if(self.right!=None):
        position+=distanceFromStart
        if(position<59536-8 and checkPositionWithDog(position, dirdis)):
          self.right.append(position)
        else:
          self.right=None
          
      dirdis=dirdis[-2:]+dirdis[:-2]
      position=self.position
      if(self.down!=None):
        position+=244*distanceFromStart
        if(position<59536-8 and checkPositionWithDog(position, dirdis)):
          self.down.append(position)
        else:
          self.down=None
          
      dirdis=dirdis[-2:]+dirdis[:-2]
      position=self.position
      if(self.left!=None):
        position-=8*distanceFromStart
        if(position>0 and checkPositionWithDog(position, dirdis)):
          self.left.append(position)
        else:
          self.left=None
          
    
    #sorry guys, as mainly a java programmer I got to have my encapsulation
    #It wasn't at all because I couldn't figure out how to do it any other way
    def getUp(self):
      return self.up
    
    def getRight(self):
      return self.right
    
    def getDown(self):
      return self.down
    
    def getLeft(self):
      return self.left
      
    def getPosition(self):
      return self.position
  
  possibleLocations=[]
  
  #this loops through all the locations in the maze and picks out the ones that are possible and adds them to possible locations
  for i in range(0, 59536):
    #the if skips the walls. This is no longer strictly necessary, but it was useful in debugging and makes everything run just a little bit faster
    if(walls[i]==0):
      loc=Location(i, getDistances())
      if(loc.getUp() != None or loc.getRight() != None or loc.getDown() != None or loc.getLeft() != None):
        possibleLocations.append(loc)
  
  #this checks if the current possible locations are all in a ACCEPTABLEUNCERTAINTY by ACCEPTABLEUNCERTAINTY square
  def checkIfDone(currentArray):
    xPositions=[]
    yPositions=[]
    up=currentArray[0].getUp()!=None
    right=currentArray[0].getRight()!=None
    down=currentArray[0].getDown()!=None
    left=currentArray[0].getLeft()!=None
    for i in range(0, len(currentArray)):
      if((currentArray[i].getUp()!=None)!=up or (currentArray[i].getRight()!=None)!=right or (currentArray[i].getDown()!=None)!=down or (currentArray[i].getLeft()!=None)!=left):
        return False
      xPositions.append(currentArray[i].getPosition()%244)
      yPositions.append(currentArray[i].getPosition()//244)
    if(max(xPositions)-min(xPositions)<ACCEPTABLEUNCERTAINTY and max(yPositions)-min(yPositions)<ACCEPTABLEUNCERTAINTY):
      global ret
      #this means we are done, so we are now preparing the return value.
      xAvg=0
      yAvg=0
      for i in range(0, len(xPositions)):
        xAvg+=xPositions[i]
        yAvg+=yPositions[i]
      xAvg/=len(xPositions)
      yAvg/=len(yPositions)
      ret[2]=yAvg*244+xAvg
      
      
      #preparing the currentLocation and direction
      print(up)
      if(up):
        ret[1]=0
        length=len(currentArray[0].getUp())
        xAvg=0
        yAvg=0
        for i in range(0, length):
          xAvg+=currentArray[i].getUp()[length-1]%244
          yAvg+=currentArray[i].getUp()[length-1]//244
        xAvg/length
        yAvg/length
        ret[0]=yAvg*244+xAvg
      elif(right):
        ret[1]=1
        length=len(currentArray[0].getRight())
        xAvg=0
        yAvg=0
        for i in range(0, length):
          xAvg+=currentArray[i].getRight()[length-1]%244
          yAvg+=currentArray[i].getRight()[length-1]//244
        xAvg/length
        yAvg/length
        ret[0]=yAvg*244+xAvg
      elif(down):
        ret[1]=2
        length=len(currentArray[0].getDown())
        xAvg=0
        yAvg=0
        for i in range(0, length):
          xAvg+=currentArray[i].getDown()[length-1]%244
          yAvg+=currentArray[i].getDown()[length-1]//244
        xAvg/length
        yAvg/length
        ret[0]=yAvg*244+xAvg
      else:
        ret[1]=3
        length=len(currentArray[0].getLeft())
        xAvg=0
        yAvg=0
        for i in range(0, length):
          xAvg+=currentArray[i].getLeft()[length-1]%244
          yAvg+=currentArray[i].getLeft()[length-1]//244
        xAvg/length
        yAvg/length
        ret[0]=yAvg*244+xAvg
      xAvg=0
      yAvg=0
      return True
    return False
  print(len(possibleLocations))
  #this removes the locations that aren't possible from possible locations until we are left with only positions in an ACCEPTABLEUNCERTAINTY by ACCEPTABLEUNCERTAINTY square
  while(not checkIfDone(possibleLocations)):
    print("\n\n\nnew")
    moveForward(MOVEDISTANCE)
    for i in range(0, len(possibleLocations)):
        print(possibleLocations[i].getPosition()) 
    for location in possibleLocations:
      location.update(getDistances())
      #I may or may not have accidently copy pasted the if above and been frustrated as to why update was not working
      if(location.getUp() == None and location.getRight() == None and location.getDown() == None and location.getLeft() == None):
        possibleLocations.remove(location)
  return ret
moved=True
a=findLocation()
print(a)
