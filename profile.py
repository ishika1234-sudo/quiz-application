import base64
import json
from io import BytesIO

import numpy as np

from flask import Flask,render_template,request,redirect,url_for,session,flash,Blueprint
from matplotlib import pyplot as plt
from werkzeug.datastructures import ImmutableMultiDict
from __init__ import config

profile_blueprint = Blueprint('profile',__name__)

mysql = config()['mysql']


# category wise graph
def category_wise_graph(myth_score,curr_score,ent_score,sci_score,hist_score,health_score):
    img = BytesIO()
    data = {'Mythology': myth_score,'Current affairs': curr_score,'Science': sci_score,
            'Entertainment': ent_score,'History': hist_score,'Health': health_score
            }
    category = list(data.keys())
    performance = list(data.values())

    fig = plt.figure()

    # creating the bar plot
    plt.bar(category,performance,color='maroon',
            width=0.4)

    plt.xlabel("Quiz Category")
    plt.ylabel("Your Performance(%)")
    plt.title("Performance based on quiz category")
    # fig.set_size_inches(10,7.5)
    plt.savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # plt.show()
    # return fig.savefig('static/images/graph' + str(session['id']) +'.png')
    return plot_url


# quiz and score graphs
def quiz_graph(score_list):
    img = BytesIO()
    # x-axis values
    x = []
    for quizz in range(len(score_list)):
        x.append('Quiz' + str(quizz + 1))

    # Y-axis values
    y = score_list

    fig = plt.figure()
    print('X, Y', x, y)
    # Function to plot
    if len(x) == 1 and len(y) == 1:
        x = x[0]
        y = y[0]
    print('X, Y',x,y)
    plt.scatter(x, y)
    plt.plot(x,y)
    plt.xlabel("Quiz")
    plt.ylabel("Your Score ")
    plt.title("Total Score of each quiz")
    plt.ylim([0,6])
    #fig.set_size_inches(10,7.5)
    plt.savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # return fig.savefig('static/images/graph1' + str(session['id']) + '.png')
    return plot_url


# user score category wise
def user_score_category_wise():
    mythology = []
    current_affairs = []
    entertainment = []
    science = []
    history = []
    health = []
    query_wise = []
    cursor = mysql.connection.cursor()
    genre_wise_result = {'genre': ['Mythology','current affairs','entertainment','science','history','health'],
                         'myth_score': [],'curr_score': [],'ent_score': [],
                         'sci_score': [],'hist_score': [],'health_score': [],'performance': [0,0,0,0,0]
                         }
    # to display user scores based on category
    cursor.execute('SELECT quiz_category, score FROM user_quiz_details where userId = %s ',(session['id'],))
    query = cursor.fetchall()
    print('GeNRE WISE RESULTS',query)
    for queries in query:
        if queries[0] == '1':
            genre_wise_result['myth_score'].append(queries[1])
        elif queries[0] == '2':
            genre_wise_result['curr_score'].append(queries[1])
        elif queries[0] == '3':
            genre_wise_result['ent_score'].append(queries[1])
        elif queries[0] == '4':
            genre_wise_result['sci_score'].append(queries[1])
        elif queries[0] == '5':
            genre_wise_result['hist_score'].append(queries[1])
        elif queries[0] == '6':
            genre_wise_result['health_score'].append(queries[1])

    mythology_score = sum(genre_wise_result['myth_score'])
    if genre_wise_result['myth_score']:
        myth_per = len(genre_wise_result['myth_score']) * 5
        mythology_performance = (sum(genre_wise_result['myth_score']) / myth_per) * 100
    else:
        mythology_performance = 0
    mythology.append('Mythology')
    mythology.append(mythology_score)
    mythology.append(len(genre_wise_result['myth_score']) * 5)
    mythology.append(mythology_performance)

    current_affair_score = sum(genre_wise_result['curr_score'])
    if genre_wise_result['curr_score']:
        current_affair_performance = (sum(genre_wise_result['curr_score']) // len(
            genre_wise_result['curr_score'])) * 100
    else:
        current_affair_performance = 0
    current_affairs.append('Current affairs')
    current_affairs.append(current_affair_score)
    current_affairs.append(len(genre_wise_result['curr_score']))
    current_affairs.append(current_affair_performance)

    entertainment_score = sum(genre_wise_result['ent_score'])
    if genre_wise_result['ent_score']:
        entertainment_performance = (sum(genre_wise_result['ent_score']) // len(
            genre_wise_result['ent_score'])) * 100
    else:
        entertainment_performance = 0
    entertainment.append('entertainment')
    entertainment.append(entertainment_score)
    entertainment.append(len(genre_wise_result['ent_score']))
    entertainment.append(entertainment_performance)

    science_score = sum(genre_wise_result['sci_score'])
    if genre_wise_result['sci_score']:
        science_performance = (sum(genre_wise_result['sci_score']) // len(
            genre_wise_result['sci_score'])) * 100
    else:
        science_performance = 0
    science.append('science')
    science.append(science_score)
    science.append(len(genre_wise_result['sci_score']))
    science.append(science_performance)

    history_score = sum(genre_wise_result['hist_score'])
    if genre_wise_result['hist_score']:
        history_performance = (sum(genre_wise_result['hist_score']) // len(
            genre_wise_result['hist_score'])) * 100
    else:
        history_performance = 0
    history.append('history')
    history.append(history_score)
    history.append(len(genre_wise_result['hist_score']))
    history.append(history_performance)

    health_score = sum(genre_wise_result['health_score'])
    if genre_wise_result['health_score']:
        health_performance = (sum(genre_wise_result['health_score']) // len(
            genre_wise_result['health_score'])) * 100
    else:
        health_performance = 0
    health.append('health')
    health.append(health_score)
    health.append(len(genre_wise_result['health_score']))
    health.append(health_performance)

    query_wise.append(mythology)
    query_wise.append(current_affairs)
    query_wise.append(entertainment)
    query_wise.append(science)
    query_wise.append(history)
    query_wise.append(health)
    return {'query_wise': query_wise, 'mythology_performance': mythology_performance,
            'current_affair_performance': current_affair_performance,
            'entertainment_performance': entertainment_performance, 'science_performance': science_performance,
            'history_performance': history_performance, 'health_performance': health_performance }


# profile page
@profile_blueprint.route('/profile/<int:id>',methods=['GET','POST'])
def profile(id):
    if request.method == 'GET':
        genre_dict = {'1': 'mythology'}
        score_list = []
        slot_list = []
        genre_list = []
        date_list = []
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_quiz_details WHERE userId =%s;',(id,))
        # Fetch one record and return result
        user_quiz_details = cursor.fetchall()
        print('user quiz details',user_quiz_details,len(user_quiz_details))
        for details in user_quiz_details:
            print('details',details)
            slot_list.append(details[2])
            score_list.append(details[5])
            genre_list.append(genre_dict[details[3]])
            date_list.append(details[6])
        final_list = zip(slot_list, score_list, genre_list, date_list)
        print('SCORE LITS IS', score_list)
        plot = quiz_graph(score_list)
        print(genre_list,score_list,date_list)

        genre_wise_user_score = user_score_category_wise()
        query_wise = genre_wise_user_score['query_wise']
        print(query_wise)
        plot_ui = category_wise_graph(genre_wise_user_score['mythology_performance'],
                                      genre_wise_user_score['current_affair_performance'],
                                      genre_wise_user_score['entertainment_performance'],
                                      genre_wise_user_score['science_performance'],
                                      genre_wise_user_score['history_performance'],
                                      genre_wise_user_score['health_performance'])

        return render_template('profile.html',user=user_quiz_details,final_list=final_list,query_wise=query_wise,
                               plot=plot,plot_ui=plot_ui)


@profile_blueprint.route('/quiz/<genre>',methods=['GET','POST'])
def quiz(genre):
    score = 0
    slot_id = []
    if request.method == 'GET':
        print('genre is',genre)
        quiz_list = []
        quiz_id = []
        options_list = []
        correct_answer = []
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT slot_id FROM user_quiz_details where userId = %s ',(session['id'],))
        cursor0 = cursor.fetchall()
        if cursor0:
            for slot_ids in cursor0:
                slot_id.append(slot_ids[0])
            slot_id = tuple(slot_id)
            print('slot idsssss',slot_id)

        cursor.execute('SELECT * FROM quiz_genre where genre = %s',(genre,))
        # Fetch one record and return result
        genre_id = cursor.fetchone()
        print('genre id is',genre_id[0])

        if cursor0:
            if len(slot_id) > 1:
                cursor.execute('SELECT * FROM quiz where genre={} and id not in {}'.format(genre_id[0],slot_id))
                # Fetch one record and return result
                user = cursor.fetchone()
            else:
                cursor.execute('SELECT * FROM quiz where genre={} and id not in ({})'.format(genre_id[0],slot_id[0]))
                # Fetch one record and return result
                user = cursor.fetchone()
        else:
            cursor.execute('SELECT * FROM quiz where genre={} '.format(genre_id[0]))
            # Fetch one record and return result
            user = cursor.fetchone()
        print('quiz fetched',user)
        slot = user[0]
        questions = json.loads(user[2])
        for key,value in questions.items():
            quiz_id.append(key)
            quiz_list.append(value['question'])
            options_list.append(value['options'])
            correct_answer.append(value['answer'])
        final = zip(quiz_list,options_list,quiz_id)
        return render_template('quiz.html',final=final,genre=genre,slot=slot, answer=correct_answer)

    if request.method == 'POST':
        user_answer = {}
        print('user now',session['id'],session['username'])
        # print('firm', request.form[slot])
        form = request.form
        print('FORM', form)
        imd = ImmutableMultiDict(form)
        form_dict = imd.to_dict(flat=False)
        print('form dict is',form_dict,int(list(form_dict)[0]))
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM quiz where id=%s ',(int(list(form_dict)[0]),))
        sql = cursor.fetchone()
        # print('sql is',sql)
        slot_id = sql[0]
        # print('slot id is', slot_id)
        slot_questions = json.loads(sql[2])
        quiz_category = sql[1]
        for k in slot_questions:
            if slot_questions[k]['answer'] == form_dict[k][0]:
                user_answer[k] = form_dict[k][0]
                score += 1
            else:
                user_answer[k] = form_dict[k][0]

        user_ans = json.dumps(user_answer)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_quiz_details(userID, slot_id, quiz_category, user_answer, "
                    "score) VALUES ( "
                    "%s, %s, %s, %s, %s)",
                    (session['id'],slot_id,quiz_category,user_ans,score))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profile.profile',id=session['id']))


# details page
@profile_blueprint.route('/details/<int:user_id>/<genre>/<int:slot_id>', methods=['GET','POST'])
def details(user_id, genre, slot_id):
    qlist = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    question = []
    ans = []
    user_ans = []
    final = []
    genre_dict = {'mythology': 1, 'current affairs': 2, 'entertainment': 3, 'science': 4, 'history': 5,
                  'health': 6}
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT slot FROM quiz where genre = %s and id = %s', (genre_dict[genre], slot_id))
    cursor0 = cursor.fetchone()
    # print('cursor0', cursor0[0])
    ques = json.loads(cursor0[0])
    print('QUESTIONS', ques)

    cursor.execute('SELECT user_answer FROM user_quiz_details where userId = %s and slot_id = %s', (user_id, slot_id))
    cursor1 = cursor.fetchone()
    print(cursor1[0], type(cursor1[0]))
    user_answers = json.loads(cursor1[0])
    print('USER ANSWER', user_answers, type(user_answers))

    for q in qlist:
        question.append(ques[q]['question'])
        ans.append(ques[q]['answer'])
        user_ans.append(user_answers[q])
    final = zip(question, ans, user_ans)
    print('FINAL', final)

    return render_template('quiz_details.html', final=final, slot=slot_id)