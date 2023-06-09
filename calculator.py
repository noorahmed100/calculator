import sys

def checkIfValid(inputexp):
    brackOpenCount = 0
    brackCloseCount = 0
    isValid = 1
    for i in inputexp:
        if i not in validNum:  # To check valid numbers and special characters
            print("invalid Expression")
            isValid = 0
            break
        if i == '(':
            brackOpenCount += 1
        if i == ')':
            brackCloseCount += 1
    if brackCloseCount != brackOpenCount:  # To check if the brackets are correctly entered
        print("Invalid number of brackets")
        isValid = 0
    for i in range(len(inputexp)):
        if inputexp[i] in validOp and inputexp[i + 1] in validOp:  # To check if two operators are entered next to exh other
            print("Two operators can't be entered next to each other")
            isValid = 0
        if inputexp[i] == '(' and inputexp[i + 1] in ['*', '/', '%', '^']:  # To check if a operator is entered after a open bracket, except '-'
            print("invalid expression")
            isValid = 0
    return isValid
# End of checkIfValid function

def fixNegative(explist):# For the sake of simplicity while calculating long expressions we will convert a-b to a+(-b)
    if explist[0] == '-':
        explist[1] = 0 - explist[1]
        explist.pop(0)
    length = len(explist)
    for j in range(1, length):
        if explist[j] == '-' and explist[j - 1] == '(':
            explist[j + 1] = 0 - explist[j + 1]
            explist.pop(j)
            length = len(explist)
        if explist[j] == '-' and explist[j + 1] not in validSplchar:
            explist[j + 1] = 0 - explist[j + 1]
            explist[j] = '+'
        if explist[j] == '(' and (explist[j + 1] == '*' or explist[j + 1] == '/' or explist[j + 1] == '+' or explist[j + 1] == '^' or explist[j + 1] == '%'):
            explist.pop(j + 1)
            length = len(explist)
        if j >= length - 1:
            break
    return explist
# End of fixNegative function

def simplify(inputexp):
    explist = [y for x, y in enumerate(inputexp)]  # Split the input expression string into list of individual character,1+(23*4) will become ['1','+','(','2','3','*','4',')']
    length = len(explist)
    for i in range(1, length - 1):  # Put * before a opening bracket for simplicity, a(a+b) will become a*(a+b)
        if explist[i] == '(' and explist[i - 1] not in validOp:
            explist.insert(i, '*')
        if explist[i] == ')' and explist[i + 1] not in validOp:
            explist.insert(i + 1, '*')
    length = len(explist)
    k = 0
    temp = list()
    temp.append(explist[0])
    for j in range(1,length):  # Adjust the list grouping multiple digit numbers, 1+(23*4) will become ['1','+','(','23','*','4',')']
        if explist[j - 1] in validOp or explist[j] in validOp or explist[j - 1] == '(' or explist[j] == ')':
            temp.append(explist[j])
            k = k + 1
        elif explist[j] not in validOp:
            temp[k] = temp[k] + explist[j]
    explist = temp
    length = len(explist)
    for i in range(0, length):  # convert the numbers which are in form of string to float
        if explist[i] == ')' or explist[i] == '(' or explist[i] in validOp:
            continue
        else:
            explist[i] = float(explist[i])
    explist = fixNegative(explist)
    return explist
# end of simplify function

def opSolve(temp, k):  # Perform operation between two numbers at a time and replace them by answer
    if temp[k] == '^':
        temp[k - 1] = float(temp[k - 1]) ** float(temp[k + 1])
    elif temp[k] == '*':
        temp[k - 1] = float(temp[k - 1]) * float(temp[k + 1])
    elif temp[k] == '/':
        temp[k - 1] = float(temp[k - 1]) / float(temp[k + 1])
    elif temp[k] == '%':
        temp[k - 1] = float(temp[k - 1]) % float(temp[k + 1])
    elif temp[k] == '+':
        temp[k - 1] = float(temp[k - 1]) + float(temp[k + 1])
    elif temp[k] == '-':
        temp[k - 1] = float(temp[k - 1]) - float(temp[k + 1])
    temp.pop(k)
    temp.pop(k)
    len2 = len(temp)
    return temp, len2
# End of opSolve function

def solveExp(explist):
    length = len(explist)
    newlist = list()
    i = length - 1
    while True:  # Loop through the list till the expression simplifies to a single value, This code will follow BODMAS rule
        if i < 0:
            break
        explist = fixNegative(explist)
        if (explist[i] == '('):  # Will take out and solve innermost brackets first
            for j in range(i + 1, length):
                if explist[j] != ')':
                    newlist.append(explist[j])
                else:
                    closeB = j - i
                    break
            temp = newlist
            len2 = len(temp)
            k = 0
            while True:  # First solve all '^' operations inside brackets
                if temp[k] == '^':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            k = 0
            while True:  # Then Solve all '/' operations inside brackets
                if temp[k] == '/':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            k = 0
            while True:  # Then Solve all '*' operations inside brackets
                if temp[k] == '*':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            k = 0
            while True:  # Then Solve all '%' operations inside brackets
                if temp[k] == '%':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            k = 0
            while True:  # Then Solve all '+' operations inside brackets
                if temp[k] == '+':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            k = 0
            while True:  # Then Solve all '-' operations inside brackets
                if temp[k] == '-':
                    temp, len2 = opSolve(temp, k)
                    k = 1
                else:
                    k = k + 1
                if k >= len2 - 1:
                    break
            explist[i] = temp[0]
            for j in range(closeB):  # After solving each bracket, replace it by answer
                explist.pop(i + 1)
            newlist.clear()
            temp.clear()
        i = i - 1
    length = len(explist)
    k = 0
    while True:  # Now solve the expression without brackets
        if explist[k] == '^':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    k = 0
    while True:
        if explist[k] == '/':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    k = 0
    while True:
        if explist[k] == '*':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    k = 0
    while True:
        if explist[k] == '%':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    k = 0
    while True:
        if explist[k] == '+':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    k = 0
    while True:
        if explist[k] == '-':
            explist, length = opSolve(explist, k)
            k = 1
        else:
            k = k + 1
        if k >= length - 1:
            break
    num = explist[0]
    return num
# End of solveExp function

# main body
validNum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%', '^', '*', '-', '+', '/', '(', ')', '.']
validOp = ['%', '^', '*', '-', '+', '/']
validSplchar = ['%', '^', '*', '-', '+', '/', '(', ')', '.']
memory=0
history = {}  # Dictionary data type will be used for storing history as combination of - {'expression1':'answer1','expression2':'answer2', etc}
print('''
\n1) INSERT EXPRESSION
2) VIEW HISTORY
3) EXPRESSION FROM FILE
4) HELP
5) EXIT\n
''')
while True:
    memory_plus_flag = False
    memory_minus_flag = False
    memory_set_flag = False
    userOption = str(input("Please Enter Option: "))
    try:
        if userOption == '1':
            inputexp = input("Enter an equation: ")
            inputExp = inputexp.replace(" ", "")
            if 'MC' in inputExp:
                memory=0
                memory_set_flag=False
                print('Memory Cleared')
            else:
                if 'MS' in inputExp:
                    memory_set_flag = True
                    inputExp = inputExp.replace('MS', '')
                elif 'M+' in inputExp:
                    memory_plus_flag = True
                    inputExp = inputExp.replace('M+', '')
                elif 'M-' in inputExp:
                    memory_minus_flag = True
                    inputExp = inputExp.replace('M-', '')
                if 'MR' in inputExp:
                    inputExp = inputExp.replace('MR', '('+str(memory)+')')
            if (checkIfValid(inputExp) == 0):
                continue
            expList = simplify(inputExp)
            answer = round(solveExp(expList), 7)
            if answer < -2147483647 or answer > 2147483647:
                print("Error! Out of range")
                continue
            if memory_set_flag:
                memory = answer
                print('Memory: ',memory)
            if memory_plus_flag:
                memory += answer
                print('Memory: ',memory)
            if memory_minus_flag:
                memory -= answer
                print('Memory: ',memory)
            print(inputExp, " = ", answer)
            history[inputExp] = answer
        elif userOption == '2':
            print("\n========== HISTORY ==========")
            for key, value in history.items():
                print(key, ' = ', value)
            print()
        elif userOption == '3':
            try:
                file1 = open('myexpressions.txt', 'r')
            except FileNotFoundError:
                print("File myexpressions.txt not found to read the expressions")
                continue
            linesExp = file1.readlines()
            for line in linesExp:
                inputexp = line.strip()
                inputExp = inputexp.replace(" ", "")
                if 'MC' in inputExp:
                    memory=0
                    memory_set_flag=False
                    print('Memory Cleared')
                else:
                    if 'MS' in inputExp:
                        memory_set_flag = True
                        inputExp = inputExp.replace('MS', '')
                    elif 'M+' in inputExp:
                        memory_plus_flag = True
                        inputExp = inputExp.replace('M+', '')
                    elif 'M-' in inputExp:
                        memory_minus_flag = True
                        inputExp = inputExp.replace('M-', '')
                    if 'MR' in inputExp:
                        inputExp = inputExp.replace('('+str(memory)+')')
                if (checkIfValid(inputExp) == 0):
                    continue
                expList = simplify(inputExp)
                answer = round(solveExp(expList), 7)
                if answer < -2147483647 or answer > 2147483647:
                    print("Error! Out of range")
                    continue
                if memory_set_flag:
                    memory = answer
                if memory_plus_flag:
                    memory += answer
                if memory_minus_flag:
                    memory -= answer
                print(inputExp, " = ", answer)
                history[inputExp] = answer
            file1.close()
        elif userOption == '4':
            print('''
1. Operators that can be used:
    a. + : Addition
    b. - : Subtraction
    c. * : Multiplication
    d. / : Division
    e. ^ : Exponentiation
    f. % : Modulus
    g. MS : Store the Answer to Register
    h. MR : Recall stored Memory Register Value
    i.  M+ : Add Answer to stored Memory Register Value
    j.  M- : Subtract Answer from Memory register Value
    k. MC: Clear Memory Register Value
2. Only '(' and ')' special characters can be used.
3. If user choses 3 from option menu, expressions would be taken from 'myexpressions.txt'.
4. 'myexpressions.txt should be in the same path as this code
''')
        elif userOption == '5':
            print("\n\nThank You!\n\n")
            sys.exit()
        else:
            print("\nPlease enter valid option\n")
    except Exception as e:
        print("Invalid Expression")
        continue
