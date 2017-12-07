import math
import random

def closedConcept(attributes, context, numberOfAttributes):
    objects = []
    attributes_closed = attributes[:]

    for obj in context.keys():
        flag = True
        for attr in attributes:
            if context[obj][attr] == 0:
                flag = False
                break
        if flag:
            objects.append(obj)

    for attr in set(range(numberOfAttributes)) - set(attributes):
        flag = True
        for obj in objects:
            if context[obj][attr] == 0:
                flag = False
                break
        if flag:
            attributes_closed.append(attr)

    return objects[:], attributes_closed[:]

def closeByOne(context, numberOfAttributes):

    lattice = {}
    attributes = []
    formal_notion = closedConcept(attributes, context, numberOfAttributes)
    attributes = formal_notion[1][:]
    lattice[0] = formal_notion

    index_current_concept = 0
    while len(attributes) < numberOfAttributes:
        for attr in range(numberOfAttributes - 1, -1, -1):
            if attr in set(attributes):
                attributes.remove(attr)
            else:
                attributes.append(attr)
                formal_notion = closedConcept(attributes, context, numberOfAttributes)
                shouldAdd = True
                for new_attr in set(formal_notion[1])-set(attributes):
                    #non-canonic generation
                    if new_attr < attr:
                        attributes.remove(attr)
                        shouldAdd = False
                        break

                if shouldAdd:
                    index_current_concept += 1
                    lattice[index_current_concept] = formal_notion
                    attributes = formal_notion[1][:]
                    break

    return lattice


def generateHypothesis(positiveTrainingSamples, negativeTrainingSamples, positiveConceptLattice, negativeConceptLattice, intersectionPercentage, numberOfAttributes):


    #concept[0] - objects, concept[1] - attributes
    positiveHypothesis = {}
    c = 0
    for key, concept in positiveConceptLattice.items():
        numberOfContradictions = 0
        for key2, row in negativeTrainingSamples.items():
            row_attr = [i for i in range(numberOfAttributes) if row[i] == 1]
            if set(concept[1]).issubset(set(row_attr)):
                numberOfContradictions += 1

        if numberOfContradictions < intersectionPercentage*len(concept[0]):
            positiveHypothesis[c] = concept
            c += 1

    negativeHyp = {}
    c = 0
    for key, concept in negativeConceptLattice.items():
        numberOfContradictions = 0
        for key2, row in positiveTrainingSamples.items():
            row_attr = [i for i in range(numberOfAttributes) if row[i] == 1]
            if set(concept[1]).issubset(set(row_attr)):
                numberOfContradictions += 1

        if numberOfContradictions < intersectionPercentage*len(concept[0]):
            negativeHyp[c] = concept
            c += 1

    return positiveHypothesis, negativeHyp

def classifyByInclusion(testData, positiveHyp, negativeHyp, thresh,numberOfAttributes):

    predictedPositive = []
    predictedNegative = []

    for key, row in testData.items():
        gIm = set([i for i in range(numberOfAttributes) if row[i] == 1])

        positiveIndicies = set()

        for idx, concept in positiveHyp.items():
            if len(concept[1]) < 1:
                continue
            if set(concept[1]).issubset(gIm):
                positiveIndicies.add(idx)

        negativeIndicies = set()
        for idx, concept in negativeHyp.items():
            if len(concept[1]) < 1:
                continue
            if set(concept[1]).issubset(gIm):
                negativeIndicies.add(idx)

        numOfPositiveMatched = len(positiveIndicies)
        numOfNegativeMatched = len(negativeIndicies)

        if numOfPositiveMatched < thresh*numOfNegativeMatched:
            predictedNegative.append(key)
        elif numOfNegativeMatched < thresh*numOfPositiveMatched:
            predictedPositive.append(key)

    return predictedPositive, predictedNegative


def classify(trainPositive, trainNegative, testPositive, testNegative, numberOfAttributes):

    positiveLattice = closeByOne(trainPositive, numberOfAttributes)
    negativeLattice = closeByOne(trainNegative, numberOfAttributes)

    testData = {**testPositive,**testNegative}
    h_p, h_n = generateHypothesis(trainPositive, trainNegative, positiveLattice, negativeLattice, 0.1,numberOfAttributes)

    pos, neg = classifyByInclusion(testData, h_p, h_n, 0.1, numberOfAttributes)

    posKeys = list(testPositive.keys())
    negKeys = list(testNegative.keys())

    numOfPos = len(posKeys)
    numOfNeg = len(negKeys)

    for p in posKeys:
        if p not in pos:
            numOfPos = numOfPos-1

    for p in negKeys:
        if p not in neg:
            numOfNeg = numOfNeg - 1


    print((numOfPos+numOfNeg)/len(testData.keys()))
    #print('scheme1')
    #return scheme1_a(test_data, h_p, h_n, 0.8)

def loadData():
    f=open('cleveland.data','r')
    fileContent=f.readlines()
    f.close()
    i=0
    attrributes = {"age":[],"trestbps":[],"chol":[],
                   "thalch":[],"oldpeak":[]}

    dataPositive = {}
    dataNegative = {}
    c=0
    for line in fileContent:
        parts = line.split(",")
        if "?" in line:
            continue
        i=i+1

        t = int(float(parts[13]))

        data = []

        for j in range(0,12):

            if j == 0:
                t = int(float(parts[j]))
                res = [0,0,0,0]

                if t < 20:
                    res[0] = 1
                    res[1] = 1
                    res[2] = 1
                    res[3] = 1
                elif t < 40 and t >=20:
                    res[0] = 0
                    res[1] = 1
                    res[2] = 1
                    res[3] = 1
                elif t < 60 and t >=40:
                    res[0] = 0
                    res[1] = 0
                    res[2] = 1
                    res[3] = 1
                elif t < 80 and t >=60:
                    res[0] = 0
                    res[1] = 0
                    res[2] = 0
                    res[3] = 1

                data = data + res
#continue
            elif j == 3:
#attrributes["trestbps"].append(float(parts[j]))
                continue
            elif j == 4:
#attrributes["chol"].append(float(parts[j]))
                continue
            elif j == 7:
#attrributes["thalch"].append(float(parts[j]))
                continue
            elif j == 9:
#attrributes["oldpeak"].append(float(parts[j]))
                continue
            elif j == 1:
                data.append(int(float(parts[j])))
            elif j == 2:
                res = [0, 0, 0, 0]
                t = int(float(parts[j]))-1
                res[t] = 1
                data = data+res
            elif j == 5:
                data.append(int(float(parts[j])))
            elif j == 6:
                res = [0, 0, 0]
                t = int(float(parts[j]))
                res[t] = 1
                data = data + res
            elif j == 8:
                data.append(int(float(parts[j])))
            elif j == 10:
                res = [0, 0, 0]
                t = int(float(parts[j]))-1
                res[t] = 1
                data = data+res
            elif j == 11:
                res = [0, 0, 0, 0]
                t = int(float(parts[j]))
                res[t] = 1
                data = data+res
            elif j == 12:
                res = [0, 0, 0]
                t = int(float(parts[j]))
                if t == 3:
                    t = 0
                elif t == 6:
                    t = 1
                elif t == 7:
                    t = 2
                res[t] = 1
                data = data+ res
            elif j == 13:
                data.append(int(float(parts[j])))
        if t > 0:
            dataPositive[i] = data
        else:
            dataNegative[i] = data

    return dataPositive, dataNegative



if __name__ == '__main__':
    positive, negative = loadData()
    numAttributes = 0
    print(numAttributes)
    for i in positive:
        numAttributes = len(positive[i])
        break


    totalLen = len(positive)+len(negative)

    numberFromEach = int(math.floor((0.2*totalLen)/2))

    testPositive = {}
    testNegative = {}

    posKeys = list(positive.keys())
    negKeys = list(negative.keys())


    t = random.sample(range(0,len(positive)), numberFromEach)
    for i in t:
        key = posKeys[i]
        testPositive[key] = positive[key]
        del positive[key]

    t = random.sample(range(0, len(negative)), numberFromEach)

    for i in t:
        key = negKeys[i]
        testNegative[key] = negative[key]
        del negative[key]

    classify(positive,negative,testPositive,testNegative,numAttributes)



