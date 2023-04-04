import re
from prettytable import PrettyTable

dataTypes = [
    'int',
    'double',
    'char',
    'string'
]

identifiers = []
keyWords = []
variables = []
literals = []
operands = []
punctuation = []

codeCopy = []
codeCopy_line = " "

systemBracket_flag = False


def ReadFile():
    file_code = open("D:\Labs\MATRAN\Eror.txt", "r")
    return file_code.read()


def AnalyzeLibrary(line):
    using_flag = False
    global codeCopy_line
    for match in re.finditer(r'\w+|;',line):
        word = match.group()
        if(word == ";"):
            break
        if(using_flag):
            if(identifiers.count(word)<1):
                identifiers.append(word)
            codeCopy_line= re.sub(r'{}'.format(word),'',codeCopy_line)
        if(word == "using" and not systemBracket_flag):
            using_flag = True
            
def AnalyzeKeyWords(line): #ALL KEYWORDS
    global codeCopy_line
    for match in re.finditer(r'\bcase\b|\bchar\b|\bclass\b|\bcontinue\b|\belse\b|\bfloat\b|\bint\b|\bnamespace\b|\bprivate\b|\bpublic\b|\bstatic\b|\bthis\b|\busing\b|\btrue\b|\bvoid\b|\bdouble\b|\bfalse\b|\bif\b|\bfor\b|\bnew\b|\breturn\b|\bstring\b|\bwhile\b|\bdo\b|;',line):
        word = match.group()
        if (word != ';'):
            if(keyWords.count(word)<1):
                keyWords.append(word)
            codeCopy_line = re.sub(r'\b{}\b'.format(word),'',codeCopy_line)
        else:
            break

def AnalyzeMethodsClassesTypes(line):
    global codeCopy_line
    for match in re.finditer(r'(\bclass\b|\bvoid\b|\bnew\b|\bnamespace\b)\W(\w+)',line):
        word = match.groups()
        if(identifiers.count(word[1])<1):
            identifiers.append(word[1])
        if(word[0]=="class" or word[0]=="new"):#Find additional dataTypes
            if(dataTypes.count(word[1])<1):
                dataTypes.append(word[1])
        codeCopy_line = re.sub(r'{}'.format(word[1]),'',codeCopy_line)
        
def AnalyzeConstructors(line):
    global codeCopy_line
    for match in re.finditer(r'(\bpublic\b|\bprivate\b|\binternal\b) +([^\bint\b|\bdouble\b|\bvoid\b]\w+)\W',line):
        word = match.groups()
        if(identifiers.count(word[1])<1):
            identifiers.append(word[1])
        codeCopy_line = re.sub(r'{}'.format(word[1]),'',codeCopy_line)

def FindVariables(line):
    for type in dataTypes:
        for match in re.finditer(r'(\b{}\b) +(\w+)'.format(type),line):
            word = match.groups()
            if(variables.count(word[1])<1):
                variables.append(word[1])

def FindAdditionalMethodsClasses(line):
    global codeCopy_line
    for match in re.finditer(r'(\b[A-Z]\w+\b)\.(\w+)\(',line):
        word = match.groups()
        if(identifiers.count(word[0])<1):
            identifiers.append(word[0])
        if(identifiers.count(word[1])<1):
            identifiers.append(word[1])
        codeCopy_line = re.sub(r'\b{}\b|\b{}\b'.format(word[0],word[1]),' ',codeCopy_line)
    
    for match in re.finditer(r'(\b[a-z]\w+\b)\.(\w+)\(',line):
        word = match.groups()
        if(identifiers.count(word[1])<1):
            identifiers.append(word[1])
        codeCopy_line = re.sub(r'\b{}\b'.format(word[1]),' ',codeCopy_line)
        


def AnalyzeVariables(line):
    global codeCopy_line
    for variable in variables:
        for variableEror in variables:
            for match in re.finditer(rf'(\b{variable}\b +\b{variableEror}\b)|(\b{variable}\b)|(;)',line):
                temp = match.groups()
                if(temp[1]!=None):
                    if(identifiers.count(temp[1])<1):
                        identifiers.append(temp[1])
                    codeCopy_line = re.sub(r'\b{}\b'.format(match.group()),' ',codeCopy_line)
                if(temp[0]!=None):
                     codeCopy.append(temp[0])
                else:
                    break


def AnalyzeLiterals(line):
    global codeCopy_line
    for match in re.finditer(r'\"([\w\s\d=]+)\"|\b\d\b|;',line): #"text" and numbers
        word = match.group()
        if(word != ';'):
            if(literals.count(word)<1):
                literals.append(word)
            codeCopy_line = re.sub(r'\"([\w\s\d=]+)\"|\b\d\b',' ',codeCopy_line)
        else:
            break

def FindOperators(line):
    global codeCopy_line
    for match in re.finditer(r'[\w\s()\"](\+=|-=|\*=|\/=|%=|\|\||&&|!=|\||&|\^|>|<|==|=|>=|<=|!|\+\+|--|\*|\/|>>|<<|~|\+|-)[\w\s()\";]',line):
        word = match.groups()
        if(operands.count(word[0])<1):
            operands.append(word[0])
        codeCopy_line = re.sub(r'[\w\s()\"](\+=|-=|\*=|\/=|%=|\|\||&&|!=|\||&|\^|>|<|==|=|>=|<=|!|\+\+|--|\*|\/|>>|<<|~|\+|-)[\w\s()\";]',' ',codeCopy_line)#Bug error


def FindPunctuation(line):
    global codeCopy_line
    for match in re.finditer(r';|\.|:|,|\)|\(|]|}|{|\[',line):
        word = match.group()
        if(punctuation.count(word)<1):
            punctuation.append(word)
        codeCopy_line = re.sub(r';|\.|:|,|\)|\(|]|}|{|\[','',codeCopy_line)




def Main():
    global codeCopy_line
    code_splitted = ReadFile().split('\n')
    lineCounter=0
    errorFlag = False
    for line in code_splitted:
        codeCopy_line = line
        lineCounter+=1
        AnalyzeLibrary(line)
        AnalyzeKeyWords(line)
        AnalyzeMethodsClassesTypes(line)
        FindVariables(line)
        AnalyzeLiterals(line)
        AnalyzeVariables(line)
        FindAdditionalMethodsClasses(line)
        AnalyzeConstructors(line)
        FindOperators(line)
        FindPunctuation(line)

        for error in re.finditer(r'(\w+|[^ ]\W+[^ ])',codeCopy_line):
            if(len(error[0])>0):
                codeCopy.append(error[0])
                
        if(len(codeCopy)>0):
            errorFlag = True
            for error in codeCopy:
                print(f"Line {lineCounter}: Error - \"{error}\"")
            codeCopy.clear()

    if(errorFlag == True):
        raise SystemExit
    
    tableIdentifiers = PrettyTable()
    tableKeywords = PrettyTable()
    tableLiterals = PrettyTable()
    tableOperands = PrettyTable()
    tablePunctuation = PrettyTable()

    tableIdentifiers.add_column("IDENTIFIERS",identifiers)
    tableKeywords.add_column("KEYWORDS",keyWords)
    tableLiterals.add_column("LITERALS",literals)
    tableOperands.add_column("OPERANDS",operands)
    tablePunctuation.add_column("PUNCTUATION",punctuation)
    print(tableIdentifiers)
    print(tableKeywords)
    print(tableLiterals)
    print(tableOperands)
    print(tablePunctuation)

Main()