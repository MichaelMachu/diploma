import random
from copy import deepcopy

class TestCA:
    """final private long randomSeed;
    final private int neighborhoodSize;
    final private int numberOfStates;
    final private boolean isIsotropic;
    final private boolean isWrapped;
    final private int worldSize;

    private byte[] rule;
    private int[] lambdaPath;
    private int rulesUsed;
    private boolean[] ruleIsUsed;
    private int generationNumber;
    private int[] currentWorld;
    private int[] nextWorld;

   
    private static Random randomMaster = new Random();"""


    #def __init__(self) -> None:
    #    self(5,4,640,True,True)

    #def __init__(self, neighborhoodSize: int, numberOfStates: int, worldSize: int,
    #    isIsotropic: bool, isWrapped: bool) -> None:
    #    self(neighborhoodSize,numberOfStates,worldSize,isIsotropic,isWrapped,random.randint(0, 2147483647))

    def __init__(self, neighborhoodSize: int, numberOfStates: int, worldSize: int,
        isIsotropic: bool, isWrapped: bool, randomSeed: int) -> None:
        self.generationNumber = 0
        self.randomSeed = randomSeed
        self.neighborhoodSize = neighborhoodSize
        self.numberOfStates = numberOfStates
        self.worldSize = worldSize
        self.isIsotropic = isIsotropic
        self.isWrapped = isWrapped
        random.seed(self.randomSeed) #Random random = new Random(randomSeed)
        ruleCt = self.numberOfStates**self.neighborhoodSize
        self.rule = [0 for _ in range(ruleCt)] #new byte[ruleCt]
        self.ruleIsUsed = [False for _ in range(ruleCt)] #new boolean[ruleCt]
        self.rule[0] = 0
        #for (int i = 1; i < ruleCt; i++) {
        for i in range(1, ruleCt):
            #self.rule[i] = (1 + abs(random.randint(-2147483648, 2147483647)) % (self.numberOfStates-1)).to_bytes(10, "big")
            self.rule[i] = (1 + abs(random.randint(-2147483648, 2147483647)) % (self.numberOfStates-1))
            if self.isIsotropic:
                self.rule[self.__isotropicMate(i)] = self.rule[i]

        lambdaCt = 0
        if self.isIsotropic:
            lambdaCt = int(((self.numberOfStates**self.neighborhoodSize + self.numberOfStates**((self.neighborhoodSize+1)/2)) / 2) - 1)
        else:
            lambdaCt = int(ruleCt - 1)
        
        self.lambdaPath = [0 for _ in range(lambdaCt)] #new int[lambdaCt]
        ct = 0
        #for (int i = 1; i < ruleCt; i++) {
        for i in range(1, ruleCt):
            if (not self.ruleIsUsed[i]):
                self.lambdaPath[ct] = i
                ct += 1
                self.ruleIsUsed[i] = True
                if (self.isIsotropic):
                    self.ruleIsUsed[self.__isotropicMate(i)] = True
            
        
        if (ct != lambdaCt):  # for debugging
            raise Exception("Bad programming; wrong lambdaCt???")
        #for (int i = 0; i < lambdaCt; i++) {
        for i in range(lambdaCt):
            r = abs(random.randint(-2147483648, 2147483647)) % lambdaCt
            temp = self.lambdaPath[i]
            self.lambdaPath[i] = self.lambdaPath[r]
            self.lambdaPath[r] = temp
        
        self.currentWorld = [0 for _ in range(self.worldSize)]    #new int[worldSize]
        #for (int i = 0; i < worldSize; i++):
        for i in range(self.worldSize):
            self.currentWorld[i] = (abs(random.randint(-2147483648, 2147483647)) % self.numberOfStates)
        self.nextWorld = [0 for _ in range(self.worldSize)] # new int[worldSize]
        self.setRulesUsed((int)(0.333*len(self.lambdaPath)))  # NB: this resets the rulesUsed[] array.
   
   
    def nextGeneration(self) -> None:
        #for (int i = 0; i < worldSize; i++) {
        for i in range(self.worldSize):
            code = self.__neighborhoodCode(i)
            if self.ruleIsUsed[code]:
                #self.nextWorld[i] = int.from_bytes((self.rule[code], "big"))
                self.nextWorld[i] = self.rule[code]
            else:
                self.nextWorld[i] = 0
            if (self.rulesUsed == 0 and self.nextWorld[i] != 0):
                print("boo")
        
        temp = deepcopy(self.currentWorld)
        self.currentWorld = self.nextWorld
        self.nextWorld = temp
        self.generationNumber += 1
   
    def getRandomSeed(self) -> int:
        return self.randomSeed
   
    def getNeighborhoodSize(self) -> int:
        return self.neighborhoodSize
   
    def getNumberOfStates(self) -> int:
        return self.numberOfStates
   
    def isIsotropic(self) -> bool:
        return self.isIsotropic

    def isWrapped(self) -> bool:
        return self.isWrapped

    def getWorldSize(self) -> int:
        return self.worldSize
   
    def setWorld(self, newWorld: list) -> None:
        if (newWorld.length == self.currentWorld.length):
            self.generationNumber = 0
            #for (int i = 0; i < newWorld.length; i++)
            for i in range(len(newWorld)):
                self.currentWorld[i] = newWorld[i]
        else:
            raise ValueError("Incorrect size for world data array in World.setWorld().")
    
    def getWorld(self) -> list:
        return deepcopy(self.currentWorld)  # return a COPY
   
    def getGenerationNumber(self) -> int:
        return self.generationNumber
   
    def zeroGenerationNumber(self) -> None:
        self.generationNumber = 0
   
    def getLambda(self) -> float:
        return self.rulesUsed / len(self.lambdaPath)

    def getRulesUsed(self) -> int:
        return self.rulesUsed
   
    def getRuleCount(self) -> int:
        return len(self.lambdaPath)
   
    def setRulesUsed(self, ct: int) -> None:
        self.rulesUsed = ct
        if self.rulesUsed < 0:
            self.rulesUsed = 0
        elif self.rulesUsed > len(self.lambdaPath):
            self.rulesUsed = len(self.lambdaPath)
        
        if self.isIsotropic:
            #for (int i = 0; i < rulesUsed; i++)
            for i in range(self.rulesUsed):
                r = self.lambdaPath[i]
                self.ruleIsUsed[r] = True
                self.ruleIsUsed[self.__isotropicMate(r)] = True
            
            #for (int i = rulesUsed; i < lambdaPath.length; i++)
            for i in range(self.rulesUsed, len(self.lambdaPath)):
                r = self.lambdaPath[i]
                self.ruleIsUsed[r] = False
                self.ruleIsUsed[self.__isotropicMate(r)] = False
        else:
            #for (int i = 0; i < rulesUsed; i++)
            for i in range(self.rulesUsed):
                self.ruleIsUsed[self.lambdaPath[i]] = True
            #for (int i = rulesUsed; i < lambdaPath.length; i++)
            for i in range(self.rulesUsed, len(self.lambdaPath)):
                self.ruleIsUsed[self.lambdaPath[i]] = False
    
    def __isotropicMate(self, n: int) -> int:
        partner = 0
        s = self.numberOfStates
        #for (int i = 0; i < neighborhoodSize; i++)
        for i in range(self.neighborhoodSize):
            partner = int(partner*s + (n % s))
            n /= s
        
        return partner
        
    def __getState(self, n: int) -> int:
        if n < 0:
            if self.isWrapped:
                n += self.worldSize
            else:
                return 0
        elif n >= self.worldSize:
            if self.isWrapped:
                n -= self.worldSize
            else:
                return 0
        
        return self.currentWorld[int(n)]
   
    def __neighborhoodCode(self, n: int) -> int:
        code = 0
        #for (int i = 0; i < neighborhoodSize; i++)
        for i in range(self.neighborhoodSize):
            code = code*self.numberOfStates + self.__getState(n+i-(self.neighborhoodSize/2))
        return code