import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz



destinations = { #Hier sind alle Inseln mit ihrem Planquadrat in einem Dictionary untergebracht
    "Ancient Spire Outpost": "Q17",
    "Dagger Tooth Outpost": "M8",
    "Galleon's Grave Outpost": "R8",
    "Golden Sands Outpost": "D10",
    "Morrow's Peak Outpost": "V17",
    "Plunder Outpost": "J18",
    "Sanctuary Outpost": "F7",
    "Brian's Bazaar": "Y12",
    "Roaring Traders":"U20",
    "Stephen's Spoils":"L15",
    "The Finest Trading Post":"F17",
    "The North Star Seapost":"H10",
    "The Spoils of Plenty Store":"B7",
    "The Wild Treasures Store":"O4",
    "Three Paces East Seapost":"S9",
    "Barnacle Cay":"O15",
    "Black Sand Atoll":"O3",
    "Black Water Enclave":"R5",
    "Blind Man's Lagoon":"N6",
    "Booty Isle":"K20",
    "Brimstone Rock":"X18",
    "Castaway Isle":"K14",
    "Chicken Isle":"I16",
    "Cinder Islet":"U14",
    "Cursewater Shores":"Y13",
    "Cutlass Cay":"M18",
    "Flame's End": "V19",
    "Fools Lagoon": "I14",
    "Glowstone Cay": "Z18",
    "Isle of Last Words": "O9",
    "Lagoon of Whispers": "D12",
    "Liar's Backbone": "S11",
    "Lonely Isle": "G8",
    "Lookout Point": "I20",
    "Magma's Tide": "Y20",
    "Mutineer Rock": "N19",
    "Old Salts Atoll": "F18",
    "Paradise Spring": "L17",
    "Picaroon Palms": "I4",
    "Plunderer's Plight": "Q6",
    "Rapier Cay": "D8",
    "Roaring Sands": "U21",
    "Rum Runner Isle": "H9",
    "Salty Sands": "G3",
    "Sandy Shallows": "D5",
    "Schored Pass": "X11",
    "Scurvy Isley": "K4",
    "Sea Dog's Rest": "C11",
    "Shark Tooth Key": "P13",
    "Shiver Retreat": "Q11",
    "The Forsaken Brink": "U16",
    "Tribute Peak": "Y2",
    "Tri-Rock Isle": "R10",
    "Twin Groves": "H11",
    "Ashen Reaches": "V23",
    "Cannon Cove": "G10",
    "Crescent Isle": "B9",
    "Crook's Hollow": "M16",
    "Devil's Ridge": "P19",
    "Discovery Ridge": "E17",
    "Fetcher's Rest": "V12",
    "Flintlock Peninsula": "W14",
    "Kraken's Fall": "R12",
    "Lone Cove": "H6",
    "Marauder's Arch": "Q3",
    "Mermaid's Hideaway": "B13",
    "Old Faithful Isle": "M4",
    "Plunder Valley": "G16",
    "Ruby's Fall": "Y16",
    "Sailor's Bounty": "C4",
    "Shark Bait Cove": "H19",
    "Shipwreck Bay": "M10",
    "Smugglers' Bay": "F3",
    "Snake Island": "K16",
    "The Crooked Masts": "O11",
    "The Devil's Thirst": "W21",
    "The Sunken Grove": "P7",
    "Thieves' Haven": "L20",
    "Wanderers Refuge": "F12",
    "Hidden Spring Keep": "I8",
    "Keel Haul Fort": "C6",
    "Kraken Watchtower": "L6",
    "Lost Gold Fort": "H17",
    "Molten Sands Fortress": "Z11",
    "Old Boot Fort": "L14",
    "Sailor's Knot Stronghold": "E14",
    "Shark Fin Camp": "P5",
    "Skull Keep": "P9",
    "The Crow's Nest Fortress": "O17",
    "The Reaper's Hideout": "I12",
    "Fort Of The Damned": "L14"
}

def distanceBetweenPoints(a,b):
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2) #Es ist der Pythagoras zweier Tuples

def convertPositionToCartesian(input): #Konvertiert die Planquadrate (e.g A12) zu einem Tuple mit zwei Zahlen, wobei A=1, B=2 usw.
    return (ord(input[0])-64,int(input[1:])) #Offset ist -64, dann ist der Unicode für A=1

def convertStringOfDestinationsToCleanedList(destinationString): #Input: Mit Kommata geteilte Inseln. Daraus wird eine Liste aus den genauen Inselnamen.
    destinationsFuzzy = destinationString.split(",") #Die einzelnen Inseln werden nun getrennt in eine Liste geschrieben
    destinationList = []
    for fuzzyDest in destinationsFuzzy: #Für jede Insel wird nun der genaue Inselname aus den "destinations" gezogen
        value = 0
        matchingDestination = ""
        for dest in destinations:   #Für jede Destination wird geprüft wie groß die Genauigkeit ist.
            newValue = fuzz.ratio(dest,fuzzyDest)
            if(newValue > value):   #Wenn dest genauer ist, wird dest die neue matchingDestination
                matchingDestination = dest
                value = newValue
        destinationList.append(matchingDestination)
    
    return destinationList

def destinationsToCoordinates(cleanedDestinationList):
    coordinateList = []
    for destination in cleanedDestinationList: #Für jeden Eintrag wird das Planquadrat zu Kartesischen Koordinaten umgewandelt.
        coordinateList.append(convertPositionToCartesian(destinations[destination]))
    return coordinateList


def TSP_nearestNeighbor(destList,pcleanInput): #Nimmt eine Liste aus Koordinaten Tuples und sortiert sie so, dass sie die Route mit der kleinsten Distanz anzeigt
    route = []
    routeByName = []    #Die gleiche Liste, nur diesmal mit den Namen anstelle der Koordinaten
    route.append(destList[0]) #Der Start der Route ist der erste Punkt der Liste
    routeByName.append(pcleanInput[0])
    pointnumber = 0
    for _p in destList:          #Für jeden Punkt in de rListe soll ein (ggf anderer) Punkt ausgewählt werden, der am nächsten in Relation zum vorherigen steht.
        candidate = ()          #Die Variable der Koordinate welche die kleinste Distanz zu Punkt p hat.
        minLength = np.inf      #Die kleinste Distanz ist zunächst "Unendllich"
        pointIteration = 0
        candidateIteration = 0
        for point in destList:  #Jeder Punkt wird nun geprüft
            if(point != route[pointnumber] and point not in route): #Der Punkt soll nicht der selbe sein, und nicht schon in der Route verbaut sein.
                if(distanceBetweenPoints(route[pointnumber],point) < minLength):    #Wenn die Distanz kleiner als die kleinste Länge ist wird point der neue "Candidate"
                    candidate = point
                    candidateIteration = pointIteration
                    minLength  = distanceBetweenPoints(route[pointnumber],point)
            pointIteration += 1
        if(candidate != ()) :
            route.append(candidate) #Wenn der "Candidate" nicht nix ist, dann wird dieser schlussendlich angehängt
            routeByName.append(pcleanInput[candidateIteration])
        pointnumber += 1
    return route,routeByName

def build_plot(pfinal_route,pfinalRouteByName):
    x, y = zip(*pfinal_route)

    x = np.asarray(x)
    y = np.asarray(y)
    #x = x + 0.5 #Offset, damit die Punkte in der Mitte sind
    #y = y + 0.5
    plt.axis([1,27,1,27]) #Die "Karte" soll immer 26*26 PLanquadrate groß sein.


    

    plt.gca().invert_yaxis()    #In Sea of Thieves sind die großen Zahlen unten :P
    plt.gca().set_aspect("equal")
    
    plt.plot(x, y, color="blue", zorder=2)  #Die Seewege zwischen den Punkten
    plt.scatter(x, y, color="black", zorder=3)  #Die Inseln als größere Punkte

    for i,txt in enumerate(pfinalRouteByName):
       plt.annotate(txt + "(" + destinations[txt] + ")",(x[i],y[i]))   #Text an den Punkten, die zeigen sollen welche Insel das ist

    plt.xticks(np.arange(1, 27), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    

    plt.plot(x[0],y[0],"o",color="red",zorder=4)    #Der Anfang soll hervorgehoben werden.
    
    
    #plt.style.use("seaborn")            
    plt.gca().set_xticks(np.arange(1, 27, 1)) #Jedes Planquadrat soll auch ein Quadrat sein!
    plt.gca().set_yticks(np.arange(1, 27, 1))
    plt.grid(zorder=1)
    plt.show()


def seaOfThievesNav(inputText):
    inputString = inputText
    cleanInput = convertStringOfDestinationsToCleanedList(inputString)
    coordinateInput = destinationsToCoordinates(cleanInput)
    final_route, finalRouteByName = TSP_nearestNeighbor(coordinateInput,cleanInput)
    print("Shortest Route: " + str(finalRouteByName))
    build_plot(final_route,finalRouteByName)