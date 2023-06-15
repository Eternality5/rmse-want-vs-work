import csv

def readInCSV(filename):
    results = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            rowContainsData = False
    
            for element in row:
                if element != '' and element != 'NA':
                    rowContainsData = True
                    break
                if element == 'NA':
                    element = ''
        
            if rowContainsData == True:
                results.append(row)

    return results

def tallySemiColonDividedList(dataset, columnNumber):
    excludedTech = {'css', 'html', 'na', 'sql', 'vb.net', 'groovy', 'android', 'arduino / raspberry pi', 'angularjs',
                    'cassandra', 'cordova', 'cloud (aws, gae, azure, etc.)', 'lamp', 'reactjs', 'windows phone',
                    'wordpress', 'sharepoint', 'sql server', 'ios', 'html/css', 'mongodb', 'node.js', 'salesforce',
                    'redis', 'spark', '', 'other(s)', 'bash/shell/powershell', 'hadoop', 'other(s):', 'bash/shell',
                    'powershell'}
    insufficientData = {'solidity', 'sas', 'webassembly', 'hack', 'delphi/object pascal', 'fortran', 'visual basic 6',
                        'visual basic', 'lisp', 'ocaml', 'delphi', 'apl', 'crystal', 'coffeescript', 'lua'}
    excludedTech.update(insufficientData)      

    titleColumns = {'tech_do', 'tech_want'}
    dict = {}
    for row in dataset:
        if row[columnNumber] in titleColumns:
            continue

        technologies = row[columnNumber].split(';')
        
        for technology in technologies:
            technology = technology.strip().lower()
            if technology in excludedTech:
                continue
            if (technology in dict):
                dict[technology] = dict[technology] + 1
            else:
                dict[technology] = 1

    return dict

def listOfLanguages(datasets):
    languages = set({})
    for dataset in datasets:
        keys = dataset.keys()
        for language in keys:
            languages.add(language.lower())
    return (languages)

def createTable(data):
    listOfLanguages = sorted({'elixir', 'kotlin', 'haskell', 'objective-c', 'go', 'perl', 'typescript', 
                       'vba', 'r', 'rust', 'javascript', 'f#', 'julia', 'python', 'swift', 'cobol', 
                       'ruby', 'dart', 'matlab', 'java', 'clojure', 'c++', 'assembly', 'php', 'c', 
                       'erlang', 'c#', 'scala'})
    table = []

    header = ['language', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
    table.append(header)
    for language in listOfLanguages:
        row = []
        row.append(language)
        for yearData in data:
            if language in yearData:
                row.append(yearData[language])
            else:
                row.append('')
        table.append(row)
    return table
            
years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
datasets = []
for year in years:
    filename = year + '.csv'
    datasets.append(readInCSV(filename))

want_tech = []
for dataset in datasets:
    technologyCount = tallySemiColonDividedList(dataset, 4)
    want_tech.append(technologyCount)

work_tech = []
for dataset in datasets:
    technologyCount = tallySemiColonDividedList(dataset, 3)
    work_tech.append(technologyCount)

work_tech_table = createTable(work_tech)
want_tech_table = createTable(want_tech)

with open('work_tech.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(work_tech_table)

with open('want_tech.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(want_tech_table)

