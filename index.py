import numpy as np 
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math

def testDots(arr, min, max):
    fig,ax = plt.subplots()
    ax.hist(arr, bins=100, range=(-0.5, 1.5))
    plt.show()

class DataGenerator:
    def __init__(self, option):
        self.data = []
        self.max = 7
        self.min = 1
        self.dirtyData = 0.1
        self.amount = option['amount']
        self.dict = {}

    def __generateIndependent(self, option):
        tempList = np.random.randn(self.amount)
        res = tempList * option['sig'] + option['mean']
        return res

    def __generateDependent(self, dependOnList):
        res = np.array([[1] * self.amount])
        lastLength = len(res)
        for i in dependOnList:
            temp = []
            numList = self.__getData(i['name']) * i['ratio']
            for preList in res:
                temp.append(preList * numList)
            res = np.append(res, temp, axis = 0)
        # TODO 根据mean调整一哈
        res = np.delete(res, 0, 0);
        randomList = np.random.rand(self.amount) * 0.3 - 0.15
        res = np.append(res, [randomList], axis = 0)
        return np.sum(res, axis = 0)

    def __getData(self, key):
        return self.dict[key]

    def setIndependent(self, list):
        for item in list:
            self.dict[item['name']] = self.__generateIndependent(item)
        return self

    def setDependent(self, item):
        self.dict[item['name']] = self.__generateDependent(item['dependOn'])
        return self

    def writeFromDict(self, fileName):
        table = pd.DataFrame.from_dict(self.dict);
        table.to_csv(fileName, sep=',', encoding='utf-8')
        # table = table.cumsum()
        plt.figure()
        table.plot()
        plt.legend(loc='best')
        plt.show()
        return self
    
    def write(self, fileName):
        self.df.to_csv(fileName, sep=',', encoding='utf-8')
        return self

    def getRamdomList(self, sig):
        amount = self.amount
        return 1 - sig + np.random.rand(amount) * 2 * sig;

    def generateData(self, amountArray):
        res = pd.DataFrame()
        for item in amountArray:
            for i in range(item['amount']):
                res[item['name'] + str(i + 1)] = self.normalize(self.dict[item['name']] * self.getRamdomList(0.3), 7)
        self.df = res
        return self

    def normalize(self, data, maxScore):
        # m = np.mean(data)
        mx = max(data)
        mn = min(data)
        return [math.ceil(((i - mn) / (mx - mn)) * maxScore) for i in data]



dg = DataGenerator({'amount': 1000})

dg.setIndependent(
    [
        {
            'name': 'B',
            'mean': 0.4,
            'sig': 0.2
        },
        {
            'name': 'C',
            'mean': 0.5,
            'sig': 0.2
        }
    ]).setDependent({
        'name': 'D',
        'dependOn': [
            {
                'name': 'B',
                'ratio': 1
            },
            {
                'name': 'C',
                'ratio': 0.1
            }
        ],
        'mean': 0.6
    }).setDependent({
        'name': 'E',
        'dependOn': [{
            'name': 'D',
            'ratio': 0.9
        }],
        'mean': 0.6
    }).setDependent({
        'name': 'F',
        'dependOn': [{
            'name': 'E',
            'ratio': 1.1
        }],
        'mean': 0.7
    }).setDependent({
        'name': 'G',
        'dependOn': [{
            'name': 'E',
            'ratio': 1.02
        }],
        'mean': 0.6
    }).generateData([
        {
            'name': 'B',
            'amount': 18
        },
        {
            'name': 'C',
            'amount': 5
        },
        {
            'name': 'D',
            'amount': 5
        },
        {
            'name': 'E',
            'amount': 5
        },
        {
            'name': 'F',
            'amount': 5
        },
        {
            'name': 'G',
            'amount': 1
        }
    ]).write('result.csv')