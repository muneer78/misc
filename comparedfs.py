import pandas as pd

dfolddataset1 = pd.read_excel('File1.xlsx', sheet_name = 1)
dfolddataset1errors = pd.read_excel('File1.xlsx', sheet_name = 2)
dfolddataset2 = pd.read_excel('File1.xlsx', sheet_name = 3)
dfolddataset2errors = pd.read_excel('File1.xlsx', sheet_name = 4)
dfoldreassignopps = pd.read_excel('File1.xlsx', sheet_name = 5)

dfnewdataset1 = pd.read_excel('File2.xlsx', sheet_name = 1)
dfnewdataset1errors = pd.read_excel('File2.xlsx', sheet_name = 2)
dfdataset2 = pd.read_excel('File2.xlsx', sheet_name = 3)
dfdataset2errors = pd.read_excel('File2.xlsx', sheet_name = 4)
dfdataset3 = pd.read_excel('File2.xlsx', sheet_name = 5)

dfolddataset1list = dfolddataset1.columns.values.tolist()
dfolddataset1errorslist = dfolddataset1errors.columns.values.tolist()
dfolddataset2list = dfolddataset2.columns.values.tolist()
dfolddataset2errorslist = dfolddataset2errors.columns.values.tolist()
dfoldreassignoppslist = dfoldreassignopps.columns.values.tolist()

dfnewdataset1list = dfnewdataset1.columns.values.tolist()
dfnewdataset1errorslist = dfnewdataset1errors.columns.values.tolist()
dfdataset2list = dfdataset2.columns.values.tolist()
dfdataset2errorslist = dfdataset2errors.columns.values.tolist()
dfdataset3list = dfdataset3.columns.values.tolist()

if dfolddataset1list == dfnewdataset1list:
    print("The dataset1 lists are identical")
else:
    print("The dataset1 lists are not identical")

if dfolddataset1errorslist == dfnewdataset1errorslist:
    print("The dataset1errors lists are identical")
else:
    print("The dataset1errors lists are not identical")

if dfolddataset2list == dfdataset2list:
    print("The dataset2 lists are identical")
else:
    print("The dataset2 lists are not identical")

if dfolddataset2errorslist == dfdataset2errorslist:
    print("The dataset2serrors lists are identical")
else:
    print("The dataset2serrors lists are not identical")

if dfoldreassignoppslist == dfdataset3list:
    print("The dataset3 lists are identical")
else:
    print("The dataset3 lists are not identical")
