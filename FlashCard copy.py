# Group: Shiv, Marisa, and Sahana
# Alexa Skill: FlashCards
# Description: A program which has two categories and subcategories from
# which the user can choose to be tested on in the form of flashcards

#hi

import sys
import logging
#You might need this to get a random card for the user! But that's later on -PH
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_flashcards():

    session.attributes['welcome'] = 1
    task_msg = 'Welcome to the Flash Card Skill... Are you ready to study?'

    session.attributes['state'] = 'start'  # conversation state we are in
    session.attributes['repetitions'] = 0  # how many times you have repeated the skill in one session
    session.attributes['correct'] = 0  # how many flashcards the user got correct
    session.attributes['topic'] = ''
    session.attributes['subtopic'] = ''
    session.attributes['question'] = ''
    session.attributes['answer'] = ''

    session.attributes['state'] = 'start' # sets state to 'start'
    return question(task_msg) # alexa asks if you are ready


@ask.intent("YesIntent")
def choose_topic():
    if  session.attributes['state'] == 'start': # checks if state is 'start'
        topic_msg = 'Which topic would you like to choose: Dates or Capitals'
        session.attributes['state'] = 'set_topic'
        return question(topic_msg) # alexa asks you which topic you want to choose
    if session.attributes['state'] == 'check_topic':
        if session.attributes['topic'] == 'DATES':
            subtopic_msg = "Okay... Would you like American History or World History?"
        if session.attributes['topic'] == "CAPITALS":
            subtopic_msg = "Okay... Would you like United States or World Countries?"
        session.attributes['state'] = 'set_subtopic'
        return question(subtopic_msg)
    if session.attributes['state'] == 'check_subtopic':
        if session.attributes['subtopic'] == 'AMERICAN HISTORY':
            q = get_question('USDates.txt')
        if session.attributes['subtopic'] == 'WORLD HISTORY':
            q = get_question('WorldHistoryDates.txt')
        return question(q)
    

@ask.intent("SetTopicIntent")
def choose_subtopic(topic):
    
    if(session.attributes['state'] == 'set_topic'):
        if topic.upper() == 'DATES': #(error message) alexa not recognizing dates try .equals or something else
            session.attributes['topic'] = 'DATES'
            just_checking_msg = "You've picked dates. Is this correct?"
        elif(topic.upper() == ('CAPITALS')):  #(error message) alexa not recognizing dates try .equals or something else
            session.attributes['topic'] = 'CAPITALS'
            just_checking_msg = "You've picked capitals. Is this correct?"
        session.attributes['state'] = 'check_topic'
    if(session.attributes['state'] == 'set_subtopic'):
        if(topic.upper() == 'AMERICAN HISTORY'):
            just_checking_msg = "You've picked American History. Is that the right topic?"
            session.attributes['subtopic'] = 'AMERICAN HISTORY'
        elif topic.upper() == 'WORLD HISTORY':
            just_checking_msg = "You've picked World History. Is that the right topic?"
            session.attributes['subtopic'] = 'WORLD HISTORY'
        session.attributes['state'] = 'check_subtopic'
    return question(just_checking_msg) # alexa asks you sub topic or if you wish to continue based on incoming state
    """
    print(topic)
    return statement(topic)"""

@ask.intent("CheckAnswerIntent")
def checkAnswer(answer):

@ask.intent("NoIntent")
def all_done():
    if session.attributes['state'] == 'start': # checks if state is 'start'
        #(reminder for group)set the current state when coding later
        msg = "Oh well, you could have studied for once in your life ... Goodbye."
        return statement(msg)
    """"""
    if session.attributes['state'] == 'question':
        return statement(session.attributes['answer'])

def get_question(file_name):
    f = open(file_name, 'r', encoding = 'utf-8')
    lines = f.readlines()
    qa = [tuple(qa.strip().split('+')) for qa in lines]
    index = randint(0,24)
    q = qa[index][0]
    a = qa[index][1]
    session.attributes['question'] = q
    session.attributes['answer'] = a
    session.attributes['state'] = 'question'
    return q
    
    

if __name__ == '__main__':
    app.run(debug=True)
