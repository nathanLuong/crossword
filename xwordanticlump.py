
import sys
import re

BLOCKCHAR = "#"
OPENCHAR = "-"
global brdHeight, brdWidth, numBlocks
brdHeight=brdWidth=numBlocks=0
global SEEDSTRINGS
SEEDSTRINGS={}
global BOARD
BOARD = ''
global REACHEDNODES
REACHEDNODES=set()
global AFFECTEDBYSEEDS
AFFECTEDBYSEEDS=set()
global dictFile
dictFile=""
global lengthToWords, wordSet, checked, modLookup
modLookup={}
lengthToWords={}
wordSet = set()
checked = {}
def input():
    global brdHeight, brdWidth, numBlocks, SEEDSTRINGS, dictFile
    for i in sys.argv:
        # height and width
        HxW = re.search(r'^(\d*)x(\d*)$', i, re.I)
        if HxW:
            brdHeight = int(HxW.group(1))
            brdWidth = int(HxW.group(2))
        # number of blocking squares to be placed
        searchBlocks = re.search(r'^(\d*)$', i)
        if searchBlocks: numBlocks = int(searchBlocks.group(1))
        searchdct = re.search(r'(\w*\.txt)', i, re.I)
        if searchdct: dictFile = searchdct.group(1)
        searchSeedString = re.search(r'(h|v)(\d*)x(\d*)((#|\w)*)', i, re.I)
        if searchSeedString:
            # maps word to [orientation, vertical offset, horizontal offset]
            if searchSeedString.group(4) in SEEDSTRINGS:SEEDSTRINGS[searchSeedString.group(4)].append([searchSeedString.group(1), int(searchSeedString.group(2)),int(searchSeedString.group(3))])
            else:SEEDSTRINGS[searchSeedString.group(4)] = [[searchSeedString.group(1), int(searchSeedString.group(2)),int(searchSeedString.group(3))]]
def allReachable(brd, index):
    #adds all of the reachable positions to REACHEDNODES
    global REACHEDNODES
    if brd[index]==BLOCKCHAR or index in REACHEDNODES:return
    REACHEDNODES.add(index)
    if (index%brdWidth)+1<brdWidth:allReachable(brd,index+1)
    if (index%brdWidth)-1>=0:allReachable(brd, index-1)
    if index+brdWidth<len(brd):allReachable(brd, index+brdWidth)
    if index-brdWidth>=0:allReachable(brd, index-brdWidth)
def addSymmetrically(brd, index):
    # returns a brd with the added symbol with 180 degree symmetry
    tbrd = [*brd]
    tbrd[index] = BLOCKCHAR
    tbrd[len(tbrd)-index-1]=BLOCKCHAR
    return tbrd
def canAddBlockSymmetrically(brd, index):
    return index not in AFFECTEDBYSEEDS and len(brd)-index-1 not in AFFECTEDBYSEEDS and brd[index]==OPENCHAR and brd[len(brd)-index-1]==OPENCHAR
def seedIndices():
    #returns a list of all the indices that would be affected by the seed strings
    affectedIndices=set()
    seedToIndices={seed:[] for seed in SEEDSTRINGS}
    for seeds in SEEDSTRINGS:
        for lists in SEEDSTRINGS[seeds]:
            if lists[0].lower()=='h':
                startIndex = (lists[1]*brdWidth)+lists[2]
                for k in range(len(seeds)):
                    affectedIndices.add(startIndex+k)
                    seedToIndices[seeds].append(startIndex+k)
            else:
                startIndex = (lists[1] * brdWidth) + lists[2]
                for j in range(len(seeds)):
                    affectedIndices.add(startIndex+(brdWidth*j))
                    seedToIndices[seeds].append(startIndex+(brdWidth*j))
    return affectedIndices, seedToIndices
def generatePsblChoices(brd):
    #returns all of the possible choices in a set
    global REACHEDNODES
    choices=[]
    runs = findHandVRuns(brd)
    for i in runs:
        if brd[i[1]]==OPENCHAR and canAddBlockSymmetrically(brd, i[1]):
            tmpBrd=addSymmetrically(brd,i[1])
            for i in range(len(tmpBrd)):
                if tmpBrd[i]==OPENCHAR:
                    startIndex=i
                    break
            tmpBrd=findTooShortWords(tmpBrd)
            if tmpBrd:
                allReachable(tmpBrd, startIndex)
                if len(REACHEDNODES)==tmpBrd.count(OPENCHAR):
                    choices.append(''.join(tmpBrd))
                REACHEDNODES=set()
    return choices
def display(brd):
    build=""
    for i in range(brdHeight):
        build+=''.join(brd[brdWidth*i:brdWidth*(i+1)])+'\n'
    print(build)
    print()
def findTooShortWords(brd):
    # retrace everything if it didn't add up to 3
    # go both directions, count until you reach a block, have to add up to 3
    tmpBrd = [*brd]
    for index in range(len(tmpBrd)):
        if tmpBrd[index] == OPENCHAR:
            tempH = [index]
            tempV = [index]
            i=1
            while i<3 and (index % brdWidth) + i < brdWidth and tmpBrd[index+i]==OPENCHAR:
                tempH.append(index+i)
                i+=1
            i=1
            while i<3 and (index % brdWidth) - i >= 0 and tmpBrd[index-i]==OPENCHAR:
                tempH.append(index-i)
                i+=1
            i=1
            while index+(brdWidth*i)<len(brd) and tmpBrd[index+(i*brdWidth)]==OPENCHAR:
                tempV.append(index+(i*brdWidth))
                i+=1
            i=1
            while index - (brdWidth*i) >= 0 and tmpBrd[index-(i*brdWidth)]==OPENCHAR:
                tempV.append(index-(i*brdWidth))
                i+=1
            if len(tempH)<3:
                for h in tempH:
                    if canAddBlockSymmetrically(''.join(tmpBrd), h):
                        tmpBrd=addSymmetrically(tmpBrd, h)
                    else:
                        return ""
            if len(tempV)<3:
                for v in tempV:
                    if canAddBlockSymmetrically(''.join(tmpBrd), v):
                        tmpBrd=addSymmetrically(tmpBrd, v)
                    else:
                        return ""
    return ''.join(tmpBrd)
def findHandVRuns(brd):
    indexToNumber = []
    for index in range(len(brd)):
        if brd[index] != BLOCKCHAR:
            tempH1 = []
            tempH2= []
            tempV1 = []
            tempV2=[]
            i = 1
            while (index % brdWidth) + i < brdWidth and brd[index + i] != BLOCKCHAR:
                tempH1.append(index + i)
                i += 1
            i = 1
            while (index % brdWidth) - i >= 0 and brd[index - i] != BLOCKCHAR:
                tempH2.append(index - i)
                i += 1
            i = 1
            while index + (brdWidth * i) < len(brd) and brd[index + (i * brdWidth)] != BLOCKCHAR:
                tempV1.append(index + (i * brdWidth))
                i += 1
            i = 1
            while index - (brdWidth * i) >= 0 and brd[index - (i * brdWidth)] != BLOCKCHAR:
                tempV2.append(index - (i * brdWidth))
                i += 1
            H=len(tempH1)*len(tempH2)
            V=len(tempV1)*len(tempV2)
            indexToNumber.append((H+V, index))
    indexToNumber.sort(reverse=True)
    return indexToNumber
def generatePuzzle(brd):
    #recursive method that generates the puzzle as a string
    blockCount = brd.count(BLOCKCHAR)
    if blockCount>numBlocks: return ""
    if blockCount==numBlocks:
        return brd
    for possibleChoice in generatePsblChoices(brd):
        subBrd=possibleChoice
        solution = generatePuzzle(subBrd)
        if solution: return solution
    return ""
def applySeeds(brd):
    tmpBrd=[*brd]
    for seed in SEEDSTRINGS:
        stringindex=0
        if seed!=BLOCKCHAR:
            for index in SEEDSTRINGS[seed]:
                tmpBrd[int(index)]=seed[stringindex]
                stringindex+=1
    return ''.join(tmpBrd)
def processDict(dict):
    #returns dictionary {(letter, index of letter, length of word):[words]}
    global lengthToWords, wordSet
    file = open(dict, "r")
    wordSet = set()
    wordDict={}
    for word in file.readlines():
        tmpWord=''.join(word.split()).lower()
        if len(tmpWord)>=3 and tmpWord not in wordSet:
            wordSet.add(tmpWord)
            if len(tmpWord) not in lengthToWords: lengthToWords[len(tmpWord)] = [tmpWord]
            else: lengthToWords[len(tmpWord)].append(tmpWord)
            for letterIndex in range(len(tmpWord)):
                if (tmpWord[letterIndex], letterIndex, len(tmpWord)) not in wordDict: wordDict[(tmpWord[letterIndex], letterIndex, len(tmpWord))] = [tmpWord]
                else: wordDict[(tmpWord[letterIndex], letterIndex, len(tmpWord))].append(tmpWord)
    return wordDict
def placeWords(brd, wordDict,usedWords):
    #if brdWidth==15 and brdHeight==15: display(brd)
    choices = generateSolvedChoices(brd, wordDict,usedWords)
    if not choices:
        return ""
    if OPENCHAR not in brd: return brd
    for (possibleChoice, used) in choices:
        subBrd=possibleChoice
        solution = placeWords(subBrd, wordDict, used)
        if solution: return solution
    return ""
def generateSolvedChoices(brd, wordDict, usedWords):
    checked = {}
    mostConstrainedHorizontalSet = set()
    mostConstrainedVerticalSet = set()
    firstH=True
    firstV=True
    for i in range(len(brd)):
        if brd[i]!=BLOCKCHAR:
            if (modLookup[i]) - 1 < 0 or brd[i-1]==BLOCKCHAR:
                horizontalWord=findConstraints(brd, i, 'h')
                if (OPENCHAR not in horizontalWord and horizontalWord not in wordSet): return ""
                if firstH:
                    mostConstrainedHorizontalSet=set(lengthToWords[len(horizontalWord)])
                    constrainedHIndex=i
                    firstH=False
                if OPENCHAR in horizontalWord:
                    if horizontalWord in checked:
                        hSet = checked[horizontalWord]
                    else:
                        hSet = set(lengthToWords[len(horizontalWord)])
                        for index,letter in enumerate(horizontalWord):
                            if letter!=OPENCHAR:
                                if (letter, index, len(horizontalWord)) not in wordDict: return ""
                                hSet = hSet&set(wordDict[(letter, index, len(horizontalWord))])
                        checked[horizontalWord]=hSet
                    if len(hSet)==0: return ""
                    if len(hSet)<len(mostConstrainedHorizontalSet):
                        mostConstrainedHorizontalSet=hSet
                        constrainedHIndex=i
            if i - (brdWidth) < 0 or brd[i-brdWidth]==BLOCKCHAR:
                verticalWord=findConstraints(brd,i,'v')
                if (OPENCHAR not in verticalWord and verticalWord not in wordSet): return ""
                if firstV:
                    mostConstrainedVerticalSet=set(lengthToWords[len(verticalWord)])
                    constrainedVIndex=i
                    firstV=False
                if OPENCHAR in verticalWord:
                    if verticalWord in checked: vSet = checked[verticalWord]
                    else:
                        vSet = set(lengthToWords[len(verticalWord)])
                        for index,letter in enumerate(verticalWord):
                            if letter!=OPENCHAR:
                                if (letter, index, len(verticalWord)) not in wordDict: return ""
                                vSet = vSet&set(wordDict[(letter, index, len(verticalWord))])
                        checked[verticalWord] = vSet
                    if len(vSet)==0: return ""
                    if len(vSet)<len(mostConstrainedVerticalSet):
                        mostConstrainedVerticalSet=vSet
                        constrainedVIndex=i
    toReturn=[]
    if len(mostConstrainedHorizontalSet)<=len(mostConstrainedVerticalSet):
        for word in mostConstrainedHorizontalSet:
            if word in usedWords: continue
            toReturn.append((applyWord(word, constrainedHIndex, brd, 'h'), usedWords+[word]))
        return toReturn
    if len(mostConstrainedVerticalSet)<len(mostConstrainedHorizontalSet):
        for word in mostConstrainedVerticalSet:
            if word in usedWords: continue
            toReturn.append((applyWord(word, constrainedVIndex, brd,'v'), usedWords+[word]))
        return toReturn
    return ""
def applyWord(word, index, brd, orientation):
    tmpBrd=[*brd]
    startIndex = index
    for letter in word:
        tmpBrd[startIndex] = letter
        if orientation=='v': startIndex+=brdWidth
        else: startIndex+=1
    return ''.join(tmpBrd)
def findConstraints(brd, index, orientation):
    #returns 2 tuples (word formed,startIndex) for horizontal and vertical (in that order)
    tempH = [index]
    tempV = [index]
    if orientation=='h':
        i = 1
        while (modLookup[index]) + i < brdWidth and brd[index + i] != BLOCKCHAR:
            tempH.append(index + i)
            i += 1
        hWord = ''.join([brd[i] for i in tempH])
        return hWord
    if orientation=='v':
        i = 1
        while index + (brdWidth * i) < len(brd) and brd[index + (i * brdWidth)] != BLOCKCHAR:
            tempV.append(index + (i * brdWidth))
            i += 1
        vWord = ''.join([brd[i] for i in tempV])
        return vWord
def main():
    global BOARD, AFFECTEDBYSEEDS, SEEDSTRINGS, OPENCHAR, BLOCKCHAR, hAvail, modLookup
    input()
    BOARD = ''.join([OPENCHAR for i in range(brdHeight*brdWidth)])
    AFFECTEDBYSEEDS, SEEDSTRINGS=seedIndices()
    for i in SEEDSTRINGS:
        if i =='#':
            for indice in SEEDSTRINGS[i]:
                BOARD=addSymmetrically(BOARD, indice)
        elif '#' in i:
            for letter in range(len(i)):
                if i[letter]=='#':
                    BOARD = addSymmetrically(BOARD, SEEDSTRINGS[i][letter])
    if (brdWidth*brdHeight)%2==1 and numBlocks%2==1:
        brd = [*BOARD]
        brd[len(BOARD)//2]=BLOCKCHAR
        BOARD = brd
    display(BOARD)
    if numBlocks==len(BOARD):
        print(''.join('#' for i in range(len(BOARD))))
    else:
        solution = applySeeds(generatePuzzle(BOARD)).lower()
        display(solution)
    for i in range(len(solution)):
        if solution[i]!=BLOCKCHAR:
            modLookup[i]=i%brdWidth
    statToWords = processDict(dictFile)
    '''if brdWidth==15 and brdHeight==15:
        tmpBrd = [*solution]
        used = set()
        for i in range(len(tmpBrd)):
            if tmpBrd[i]==OPENCHAR:
                horizontal = findConstraints(''.join(tmpBrd), i, 'h')
                tmpSet = set(lengthToWords[len(horizontal)])
                if horizontal.count(OPENCHAR)!=len(horizontal):
                    for idx,letter in enumerate(horizontal):
                        if letter!=OPENCHAR:
                            tmpSet=tmpSet&set(statToWords[(letter,idx,len(horizontal))])
                for word in tmpSet:
                    if word not in used: used.add(word)
                    else: continue
                    for index,letter in enumerate(word):
                        tmpBrd[i+index]=letter
                    break
        display(''.join(tmpBrd))
    else:'''
    #display(placeWords('----####--------a-----#--------------#----------#------#----#---#------#---#--------#-----#-------#------###----#----###------#-------#-----#--------#---#------#---#----#------#----------#--------------#--------------####----', statToWords,[]))
    display(placeWords(solution, statToWords, []))
main()