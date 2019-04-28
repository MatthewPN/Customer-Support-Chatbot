# need to set FLASK_APP
# FLASK_APP=Main.py
# Start:
# python -m flask
# For server: python -m flask --host=0.0.0.0
import json
from flask import Flask, request, jsonify, render_template
import re
import pickle
from socket import gethostname
from AnswerStats import AnswerStats
from inference import inference


# Code Infomation

total_count = 0

# used to increment word count for a specific sentence in the hashmap answer/count
def incrementDictCount(counts, answer):
    if answer in counts:
        counts[answer] += 1
    else:
        counts[answer] = 1


def readTrainingData(words, file):
    global total_count
    counts = {}
    for line in file:
        line = line.lower()
        questionAnswer = line.split("::")
        answer = questionAnswer[1].rstrip()
        for text in questionAnswer[0].split():
            if len(text) > 3:
                # increment word count for question and total word count
                incrementDictCount(counts, answer)
                total_count += 1
                word = re.sub(r'\W+', '', text)
                # if word in dict, check if value (another dict) contains that answer as the key
                if word in words:
                    answerMap = words[word]
                    if answer in answerMap:
                        answerMap[answer] += 1
                    # if answer is not in dict, add it
                    else:
                        answerMap[answer] = 1
                # if word not in dict, create new item with new dictionary as value
                else:
                    words[word] = {}
                    temp = words[word]
                    temp[answer] = 1
    return counts


def trainAgent():
    global total_count
    words = {}
    path = "C:\\Users\\Blake\\Downloads\\SP\\QuestionAnswer.txt"
    training_file = open(path, "r")
    # counts contains answer as key and value as the count of words per that sentence
    counts = readTrainingData(words, training_file)
    calculations_dict = {}
    # calculate values that will be used in Bayes formula
    for answer, count, in counts.items():
        calculations_dict[answer] = AnswerStats(count, count / total_count)
    serializedWords = open(
        "serializedWords.p", 'wb+')
    pickle.dump(words, serializedWords)
    serializedCalculations = open(
        "serializedCalculations.p", 'wb+')
    pickle.dump(calculations_dict, serializedCalculations)


def answer_question(question):
    words = pickle.load(open("serializedWords.p", "rb"))
    calculations = pickle.load(open("serializedCalculations.p", "rb"))
    finished = determine_question(
        calculations, words, question)
    if finished != False:
        return finished


""""
hashmap1: Calculation_dict
    {Question, Object1}

object1 = Object1.count and Object1.weight

hashmap2: words
    {word, hashmap3}

hashmap3: word sublevel
    {answer, count of that word} 

Just remember that the training input needs to be in a single txt file.  This layout:

    This is the question:: This is the answer

"::" delimits the end of the question and the beginning of the answer. 
"""


def determine_question(calcDict, wordsDict, sentence,):
    CalcProb = {}  # store answers
    for question in calcDict:
        CalcProb[question] = 0.0  # set up a dict to store weight
    for word in sentence.split():  # breaks each user sentence into words
        if word in wordsDict:  # if the word from the user sentence exists in our words list
            # list of keys that are from the words dict[word]
            key1 = wordsDict[word].keys()
            key2 = CalcProb.keys()  # list of keys of the CalcProb
            # for each key in key1(matching word keys) check if Key2 has a matching key.
            for x in key1:
                if key2.__contains__(x):
                    CalcProb[x] += (wordsDict[word][x] /
                                    calcDict.get(x).total_count)
    # Perform Naive Bayes on Sentence
    answer = naive_bayes_SP(calcDict, CalcProb)
    return answer


def naive_bayes_SP(caldict, calcprob):
    Prediction = {}  # used to hold the Predictions in
    z = 0  # is used to make sure we can make an attempt at the sentence. We found the users sentence in our data
    highest = {'Highest': 0.0}  # this var is used to
    for test in calcprob.values():
        z += test
    if z == 0:  # we will be unable to use this sentence
        print("We had no data that matched the users sentence")
        return False  # used to catch in the main() loop
    elif z != 0:  # we have words that match the users sentence
        for question in caldict:
            # set up a dict to store Predictions
            Prediction[question] = (
                calcprob[question] * caldict[question].weight)
    for answer in Prediction:  # make sure we have the highest value
        pop1 = next(iter(highest.keys()))  # grab the next element in the dict
        # compare values and if true, remove old value and replace with new
        if Prediction[answer] > next(iter(highest.values())):
            highest.pop(pop1)  # remove old value
            highest[answer] = Prediction[answer]  # add new value
    return highest


 # Flask Infomation
app = Flask(__name__)
app.debug = True

@app.route('/')
def sign_up():
    return render_template('Shell.html')


@app.route('/SubmitData', methods=['GET'])
def submit_data():
    userinput = request.args.get('inpTxt').lower()
    answer = answer_question(userinput)
    if answer is not None:
        print(answer)
        percent = list(answer.values())[0]
        print(percent)
        if percent > 0.03:
            print("Bays")
            return json.dumps(list(answer)[0])
        else:
            print("Net")
            net = (inference(userinput))
            return json.dumps(list(net["answers"])[net["best_index"]])
    else:
        print("Net")
        net = (inference(userinput))
        return json.dumps(list(net["answers"])[net["best_index"]])

if __name__ == '__main__':
    app.run(host='0.0.0.0')