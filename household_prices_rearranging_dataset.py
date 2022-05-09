import csv
import math
import pandas as pd
from matplotlib.cbook import boxplot_stats
from scipy import stats
import numpy as np

###### Define Patch
csvName = 'train_rearranged'
csvName2 = 'train_rearranged2'
csvPath = f'/Users/kacper/Downloads/house-prices-advanced-regression-techniques/{csvName}.csv'
csvPath2 = f'/Users/kacper/Downloads/house-prices-advanced-regression-techniques/{csvName2}.csv'

###### Select variant of changing Dataset
### 1 - Changing to default data
### 2 - Data with grouped "YearBuild"
operationOnVariable = 2
### Removing Outliers [y/n]? In which category?
removeOutliers = "y"
inCategory = 'SalePrice'

### Grouping
yearsBuildPeriods = 5
newListInVariable = []
with open(csvPath,  newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    for row in csvReader:
            numberOfDataInRow = len(row)
            singleListInRow = []
            if row[0] == "Id":
                searchingItem = row.index("YearBuilt")
                print("Row index: " + str(searchingItem))
            for index in range(0, numberOfDataInRow):

                if operationOnVariable == 1:
                    singleListInRow.append(row[index])
                    print(index)

                if operationOnVariable == 2:
                    if index == searchingItem:
                        if row[0] == "Id":
                            singleListInRow.append(row[index])
                            continue;
                        else:
                            test = math.ceil(int(row[index])/yearsBuildPeriods)
                            test *= yearsBuildPeriods
                            row[index] = "{} - {}".format(test-(yearsBuildPeriods-1), test)

                singleListInRow.append(row[index])
            newListInVariable.append(singleListInRow)


numberOfDataInRow = len(open(csvPath2).readlines())
print("Number of rows after grouping: " + str(numberOfDataInRow))
with open(csvPath2, 'w+', newline='') as csvFile2:
    writer = csv.writer(csvFile2)
    for row in range(0, numberOfDataInRow):
        writer.writerow(newListInVariable[row])

### Removing
if removeOutliers == "y":
    df = pd.read_csv(csvPath2)
    z = stats.zscore(df[inCategory])
    z_abs = np.abs(z)
    rows2Remove = np.where(z_abs > 3)
    print("Rows to Remove: " + str(rows2Remove[0]))
    df.drop(rows2Remove[0], inplace=True)
    print("Number of rows after removal: " + str(df.shape[0]))
    df.to_csv(csvPath2)

