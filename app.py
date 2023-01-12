from flask import Flask, render_template, request, redirect, flash, send_file
import asyncio
import threading
from collections import Counter
import time
from datetime import date, timedelta
import datetime
file1 = open('/simpleWordleSolver/files/words2.txt', 'r') #
Lines = file1.readlines()

file2 = open('/simpleWordleSolver/files/words.txt', 'r')
answers = file2.readlines()

someDic = {}
app=Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'susVerySomething'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form)
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/waffle', methods=['POST', 'GET']) ##Waffle Page
def waffle():
    if request.method == 'POST':
        print(request.form)
        responses = ['r1', 'r2', 'r3']
        thingsInForm = ['green1', 'green2', 'green3', 'green4', 'green5', 'yellow1', 'yellow2', 'yellow3', 'yellow4',
                        'yellow5']
        for response in responses:
            count=0
            while count < 5:
                count+=1
                try:
                    print(request.form[response+'green'+str(count)])
                except:
                    print('lool unselected')
                else:
                    try:
                        print(request.form[response+'yellow'+str(count)])
                    except:
                        print('lol unselected 4 yellow')
                    else:
                        flash('Please Specify only 1 CheckMark per letter.')
                        break
                        return render_template('waffleRows.html')


            someDic[response] =[['_', '_', '_', "_", "_"], [], [] ] ##3 lists in the list: 1 for position, 1 for the letters that are in word, one for the ones that aren't
            word=request.form[response+'word']
            if word=='':
                flash('Specify a Word. Why didn\'t you specify a word?')
                break
                return render_template('waffleRows.html')
            for thing in thingsInForm:
                flag=0
                try:
                    print(request.form[response+thing])
                except:
                    flag+=1
                else:
                    if flag==0:
                        if 'green' in thing:
                            index=int(thing[5:])-1
                            someDic[response][0][int(index)] = word[index]
                            someDic[response][1].append(word[index])
                        else:
                            index=int(thing[6:])-1
                            someDic[response][1].append(word[index])
            for letter in word:
                if letter not in someDic[response]:
                    someDic[response][2].append(letter) #Part of the NONO Letters


        #Check if it has all info
        #Change it a bit here
        return render_template('waffleColumns.html', rowDictionary=someDic) ##, data = data
    elif request.method == 'GET':
        return render_template('waffleRows.html')


@app.route('/solveWaffle', methods=['POST', 'GET'])  ##Waffle Page
def solveWaffle():
    if request.method == 'POST':
        print(request.form)
        responses = ['c1', 'c2', 'c3']
        thingsInForm = ['green1', 'green2', 'green3', 'green4', 'green5', 'yellow1', 'yellow2', 'yellow3', 'yellow4',
                        'yellow5']
        for response in responses:
            count = 0
            while count < 5:
                count += 1
                try:
                    print(request.form[response + 'green' + str(count)])
                except:
                    print('lool unselected')
                else:
                    try:
                        print(request.form[response + 'yellow' + str(count)])
                    except:
                        print('lol unselected 4 yellow')
                    else:
                        flash('Please Specify only 1 CheckMark per letter.')
                        break
                        return render_template('waffleColumns.html', rowDictionary=request.form['solve_word'])

            someDic[response] = [['_', '_', '_', "_", "_"], [],
                                 []]  ##3 lists in the list: 1 for position, 1 for the letters that are in word, one for the ones that aren't
            word = request.form[response + 'word']
            if word=='':
                flash('Specify a Word. Why didn\'t you specify a word?')
                break
                return render_template('waffleColumns.html')
            for thing in thingsInForm:
                flag = 0
                try:
                    print(request.form[response + thing])
                except:
                    flag += 1
                else:
                    if flag == 0:
                        if 'green' in thing:
                            index = int(thing[5:]) - 1
                            someDic[response][0][int(index)] = word[index]
                            someDic[response][1].append(word[index])
                        else:
                            index = int(thing[6:]) - 1
                            someDic[response][1].append(word[index])
            for letter in word:
                if letter not in someDic[response]:
                    someDic[response][2].append(letter) #Part of the NONO Letters

        # Check if it has all info
        # Change it a bit here
        print(someDic)

        print(f"Inside flask function: {threading.current_thread().name}")
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        answerDoc = loop.run_until_complete(
            solveWaffle(someDic))
        row1 = answerDoc['r1']
        row2 = answerDoc['r2']
        row3 = answerDoc['r3']
        column1 = answerDoc['c1']
        column2 = answerDoc['c2']
        column3 = answerDoc['c3']
        return render_template('possibleWaffle.html', r1=row1, r2=row2, r3=row3, c1=column1, c2=column2, c3=column3)
    elif request.method == 'GET':
        return render_template('waffleRows.html')

async def solveWaffle(theDic):
    responses = ['r1', 'r2', 'r3', 'c1', 'c2', 'c3']
    letterBank = []
    answerDoc = {}
    bank = []
    ##Somedic is correct! Now lets try solving this :(
    for key in theDic.keys():  ##the top row middle row crap
        for letter in theDic[key][2]:
            bank.append(letter)  ##Possible letter choices
    letterBank = list(dict.fromkeys(bank))
    for response in responses:
        print("Let's find the words for the " + response)
        answerDoc[response] = []
        ##To do so, we have to adjust the letter bank for thiis word.
        specificLetterBank = letterBank[:]  ##Prevents the editing of both lists cuz cringe momento
        for letter in theDic[response][2]:  ##This is the nono letters. ONTO SOLVING YEAHHHH
            if letter in specificLetterBank:
                specificLetterBank.remove(letter)  ##Removes the letters that aren't allowed
        for letter in theDic[response][1]:
            specificLetterBank.append(letter)  ##This may be the cause idk

        if "c" in response:
            for letter in theDic['r1'][1]:
                specificLetterBank.append(letter)
            for letter in theDic['r2'][1]:
                specificLetterBank.append(letter)
            for letter in theDic['r3'][1]:
                specificLetterBank.append(letter)
        elif "r" in response:
            for letter in theDic['c1'][1]:
                specificLetterBank.append(letter)
            for letter in theDic['c2'][1]:
                specificLetterBank.append(letter)
            for letter in theDic['c3'][1]:
                specificLetterBank.append(letter)

        for n in theDic[response][0]:
            if n != '_':
                specificLetterBank.append(n)  # adding the green letters

        for word in Lines:  ##Legit copy pasted from og wordle solver
            flag = 1
            word = word.replace("\n",
                                "")  ##Gets rid of the annoying \n in every word. This is only in MY TXT FILE! Check if yours has this problem too.
            if len(word) != 5:
                flag = 0

            for letter in list(word):
                # if letter in someDic[response][2]:  ## If that letter is in the list of unavailable letters, set the flag to 0
                # flag = 0
                if letter not in specificLetterBank:
                    flag = 0
            for letter in theDic[response][1]:
                if letter not in list(word):
                    flag = 0

            if flag == 1:
                flag2 = 1
                for n in theDic[response][0]:
                    if n != '_':
                        if word[theDic[response][0].index(n)] != n:  ##If the placement is NOT the same
                            flag2 = 0

                # for n in letters:
                # if n not in word:
                # flag2 = 0

                if flag2 == 1:
                    if word not in answerDoc[response]:
                        ##Doing a final check to try and get the most accurate words

                        answerDoc[response].append(word)
        print(str(len(answerDoc[response])) + " answer(s) found for the " + response)
        print(answerDoc)
    #for n in responses:
        #print(str(answerDoc[n]) + ' | These are the word choices for the ' + n)
    return answerDoc


async def solveWordle(wordd,notWork, placement, letters):
    noo = []
    possibleWords = []
    for letter in notWork: #notWork is a string of all the leters that hopefully dont work
        noo.append(letter)
    #Funtimes start now!!
    for word in Lines:
        flag=1
        word = word.replace("\n", "")##Gets rid of the anna# oying \n in every word. This is only in MY TXT FILE! Check if yours has this problem too.
        for letter in list(word):
            if letter in noo:  ## If that letter is not in the list of available letters, set the flag to 0
                flag = 0
        if len(word) != 5:
            flag=0
        if flag == 1:
            flag2=1
            for n in placement:
                if n != '_':
                    if word[placement.index(n)] != n:  ##If the placement is NOT the same
                        flag2=0
            for n in letters:
                if n not in word:
                    flag2=0
            if flag2==1:
                if word not in possibleWords:
                    possibleWords.append(word)
    if possibleWords == []:
        return '999'
    else:
        return possibleWords



@app.route('/solve', methods=['POST', 'GET'])
def solver():
    print(request.form)
    print(f"Inside flask function: {threading.current_thread().name}")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    #Getting the ones that exist
    count=0
    while count < 5:
        count +=1
        try:
            print(request.form['green'+str(count)])
        except:
            print('waafcdsfafdsafada')
        else:
            try:
                print(request.form['yellow' + str(count)])
            except:
                print('double wacka')
            else:
                flash('Please specify only 1 check mark per letter.')
                return render_template('index.html')
                break
    if request.form['notWork'] != '' or ' ' not in request.form['notWork']:
        thingsInForm = ['green1', 'green2', 'green3', 'green4', 'green5', 'yellow1', 'yellow2', 'yellow3', 'yellow4', 'yellow5']
        word = request.form['word']
        placement=['_', '_', '_', '_', '_']
        knownLetters=[]
        for thing in thingsInForm:
            flag=0
            try:
                print(request.form[thing])
            except: #Doesnt exist
                flag+=1
            else:
                if flag==0:
                    if 'green' in thing:
                        index = int(thing[5:])-1
                        placement[int(index)] = word[index]
                        knownLetters.append(word[index])
                    else:
                        index = int(thing[6:]) - 1
                        knownLetters.append(word[index])
        result = loop.run_until_complete(solveWordle(request.form['word'], request.form['notWork'], placement, knownLetters))
        if '999' in result:
            flash('Sorry, no words were found.')
            return render_template('index.html')
        else:
            return render_template('possibleWords.html', words=result)
    else:
        if request.form['notWork'] == '':
            flash('Please specify some letters that are grey (don\'t work)!')
            return render_template('index.html')
        else:
            flash('Don\'t add a space in the grey letter list.')
            return render_template('index.html')

@app.route('/cheat', methods=['POST', 'GET'])
def cheater():
    print(request.form)
    print(f"Inside flask function: {threading.current_thread().name}")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    if request.form['the_date'] == '':
        flash('Specify a date or choose one of the options to cheat.')
        return render_template('index.html')
    elif request.form['the_date']=='today':
        trueWordleDate = date.today()
        trueWordleDate = trueWordleDate.strftime("%b %d %Y")
        leAnswer = []
        for n in answers:
            if trueWordleDate in n:
                leAnswer.append(n)
                break
        return render_template('possibleWords.html', words=leAnswer)
    elif request.form['the_date'] == 'tomorrow':
        trueWordleDate = date.today()
        trueWordleDate = trueWordleDate + timedelta(1)
        trueWordleDate = trueWordleDate.strftime("%b %d %Y")
        leAnswer = []
        for n in answers:
            if trueWordleDate in n:
                leAnswer.append(n)
                break
        return render_template('possibleWords.html', words=leAnswer)
    else:
        d = datetime.datetime.strptime(request.form['the_date'], "%Y-%m-%d")
        trueWordleDate = d.strftime("%b %d %Y")

        leAnswer = []
        for n in answers:
            if trueWordleDate in n:
                leAnswer.append(n)
                break

        return render_template('possibleWords.html', words=leAnswer)


if __name__ == '__main__': ##Allows me to run the flask app in terminal
    app.run(host="0.0.0.0", port=7124, debug=True)
