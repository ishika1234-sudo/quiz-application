import json

from flask import Flask,render_template,request,redirect,url_for,session,flash, Blueprint
from matplotlib import pyplot as plt

from __init__ import config


main = Blueprint('main', __name__)

mysql = config()['mysql']


# home page
@main.route('/')
def home():
    return render_template('home.html')


def insert():
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email, user_password) VALUES (%s, %s,%s)",
                    ('Ashoka1','abc@gmail1.com','12345'))
        mysql.connection.commit()
        cur.close()
        return 'success'
    except Exception as e:
        print("Problem inserting into db: " + str(e))
        return False
# insert()


def fetch(id):
    try:
        quiz_list = []
        options_list = []
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM quiz ')
        # Fetch one record and return result
        user = cursor.fetchall()
        # print(user)
        '''for users in user:
            #print(users)
            quiz_list.append(users[1])
            options = json.loads(users[2])
            options_list.append (list(options.values()))
        print(options_list)'''
        # print(json.loads(user[2]), type(json.loads(user[2])))
        return 'success'
    except Exception as e:
        print("Problem fetching from db: " + str(e))
        return False
fetch(2)

# Graph function
def category_wise_graph():
    import matplotlib.pyplot as plt

    data = {'apple': 10, 'grapes': 20}
    names = list(data.keys())
    values = list(data.values())

    fig,axs = plt.subplots(1,3,figsize=(9,3),sharey=True)
    axs[0].bar(names,values)
    axs[1].scatter(names,values)
    axs[1].plot(names,values)
    axs[2].plot(names,values)
    fig.suptitle('Categorical Plotting')
    plt.show()
# category_wise_graph()

app = config()['app']


if __name__ == '__main__':
    app.run(debug=True)
