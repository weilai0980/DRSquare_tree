import numpy as np
import sys

import csv

class SyntheticDataGenerator:
    def __init__(self, rows, cols, features, thresh,  outlier, mu_range = 100, sigma = 1, ):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols + 1)] for _ in range(rows)]
        self.generateWeights(features, mu_range, sigma, thresh, outlier)
    
    def printData(self):
        for i in range(self.rows):
            print(str(self.data[i]))
            
    def writeData(self, outputfile):
        with open(outputfile, mode='w') as fo:
            
            csv_writer = csv.writer(fo)
            
            for i in range(self.rows):
                #csv_writer.writerows(self.data[i])
                for j in range(0, self.cols):
                    fo.write(str(self.data[i][j]) + ',')
                fo.write(str(self.data[i][self.cols]) + '\n')
  
                #fo.write(str(self.data[i]) + '\n')   
                
    
    # for each unique combination we generate a weight from a Gaussian with mean uniformly generated from mu_range and standard deviation sigma 
    def generateWeights(self, features, mu_range, sigma, thresh, outlier):
        distr = {}
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = int(np.random.uniform(features))
            if np.random.uniform(0, 1) < thresh:
                
                #
                outlier =  mu_range* outlier
                
                self.data[i][self.cols] = np.random.normal(outlier, 1, 1)[0]
                continue
            if tuple(self.data[i]) in distr:
                params = distr[tuple(self.data[i])]
                self.data[i][self.cols] = np.random.normal(params[0], params[1], 1)[0]
            else:
                params = (int(np.random.uniform(mu_range)), sigma)
                distr[tuple(self.data[i])] = params
                self.data[i][self.cols] = np.random.normal(params[0], params[1], 1)[0]