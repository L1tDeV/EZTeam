import sqlite3 as sq

async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, name TEXT, date TEXT, photo TEXT, phone TEXT, projects TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS questions(question_id TEXT PRIMARY KEY, question TEXT, answer TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS projects(project_id TEXT PRIMARY KEY, project TEXT, info TEXT, people TEXT)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS checker(username TEXT PRIMARY KEY, user_id TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY, user_id TEXT)")

    db.commit()

async def create_user(user_id, lst):
    fl = False
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    db.commit()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", (user_id, lst[0],lst[1],'',lst[2],lst[3]))
        db.commit()
        fl = True
    return fl

async def create_question(question, answer):
    fl=True
    try:
        lst = list(cur.execute("SELECT * FROM questions").fetchall())
        db.commit()
        ind = str(len(lst)+1)
        cur.execute("INSERT INTO questions VALUES(?, ?, ?)", (ind, question, answer))
        db.commit()
        fl = True
    except:
        fl=False
    return fl

async def edit_user(user_id, lst):
    fl = False
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    db.commit()
    if user:
        cur.execute("DELETE from users WHERE user_id == '{key}'".format(key=user_id))
        db.commit()
        fl = await create_user(user_id, lst)
    return fl

async def get_user_prof(user_id):
    try:
        user = list(cur.execute("SELECT * FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone())
        db.commit()
        return user
    except:
        return []
    
async def get_checks():
    lst = list(cur.execute("SELECT * FROM checker").fetchall())
    db.commit()
    lst = list(map(lambda x: x[0], lst))
    return lst

async def add_checks(username):
    fl=True
    try:
        cur.execute("INSERT INTO checker VALUES(?, ?)", (username, ''))
        db.commit()
        fl = True
    except:
        fl=False
    return fl

async def del_checks(username):
    fl=True
    try:
        cur.execute("DELETE from checker WHERE username == '{key}'".format(key=username))
        db.commit()
        fl = True
    except:
        fl=False
    return fl

async def get_admins():
    lst = list(cur.execute("SELECT * FROM admins").fetchall())
    db.commit()
    lst = list(map(lambda x: x[0], lst))
    return lst

async def add_admins(username):
    fl=True
    try:
        cur.execute("INSERT INTO admins VALUES(?, ?)", (username, ''))
        db.commit()
        fl = True
    except:
        fl=False
    return fl

async def del_admins(username):
    fl=True
    try:
        cur.execute("DELETE from admins WHERE username == '{key}'".format(key=username))
        db.commit()
        fl = True
    except:
        fl=False
    return fl

async def get_check_lst(user_id, username):
    user = cur.execute("SELECT * FROM checker WHERE username == '{key}'".format(key=username)).fetchone()
    db.commit()
    # print(user)
    try:
        user = cur.execute("SELECT * FROM checker WHERE username == '{key}'".format(key=username)).fetchone()
        # checks = sq.connect('new.db').cursor().execute("SELECT * FROM checker")
        # print(checks[0])
        # lst_checker = []
        # for elem in checks:
        #     lst_checker.append(elem[0])
        # sq.connect('new.db').commit()
        db.commit()
        if user:
            if user[1]==user_id:
                return True
            else:
                print(1)
                cur.execute("DELETE from checker WHERE username == '{key}'".format(key=username))
                db.commit()
                cur.execute("INSERT INTO checker VALUES(?, ?)", (username, user_id))
                db.commit()
                return True
        else:
            user = cur.execute("SELECT * FROM checker WHERE user_id == '{key}'".format(key=user_id)).fetchone()
            db.commit()
            if user:
                if user[0]==username:
                    return True
                else:
                    cur.execute("DELETE from checker WHERE user_id == '{key}'".format(key=user_id))
                    db.commit()
                    cur.execute("INSERT INTO checker VALUES(?, ?)", (username, user_id))
                    db.commit()
                    return True
            else:
                return False
        # return lst_checker
    except:
        await db_start()
        await get_check_lst(user_id, username)

async def create_project_db(project, descr, people):
    fl=True
    try:
        lst = list(cur.execute("SELECT * FROM projects").fetchall())
        db.commit()
        ind = str(len(lst)+1)
        cur.execute("INSERT INTO projects VALUES(?, ?, ?, ?)", (ind, project, descr, people))
        db.commit()
        fl = True
    except:
        fl=False
    return fl


async def is_admin(user_id, username):
    user = cur.execute("SELECT * FROM admins WHERE username == '{key}'".format(key=username)).fetchone()
    db.commit()
    # print(user)
    try:
        user = cur.execute("SELECT * FROM admins WHERE username == '{key}'".format(key=username)).fetchone()
        # checks = sq.connect('new.db').cursor().execute("SELECT * FROM checker")
        # print(checks[0])
        # lst_checker = []
        # for elem in checks:
        #     lst_checker.append(elem[0])
        # sq.connect('new.db').commit()
        db.commit()
        if user:
            if user[1]==user_id:
                return True
            else:
                print(1)
                cur.execute("DELETE from admins WHERE username == '{key}'".format(key=username))
                db.commit()
                cur.execute("INSERT INTO admins VALUES(?, ?)", (username, user_id))
                db.commit()
                return True
        else:
            user = cur.execute("SELECT * FROM admins WHERE user_id == '{key}'".format(key=user_id)).fetchone()
            db.commit()
            if user:
                if user[0]==username:
                    return True
                else:
                    cur.execute("DELETE from admins WHERE user_id == '{key}'".format(key=user_id))
                    db.commit()
                    cur.execute("INSERT INTO admins VALUES(?, ?)", (username, user_id))
                    db.commit()
                    return True
            else:
                return False
        # return lst_checker
    except:
        await db_start()
        await get_check_lst(user_id, username)

def get_users_lst():
    try:
        users = sq.connect('new.db').cursor().execute("SELECT * FROM users")
        lst_users = []
        for elem in users:
            lst_user = [elem[1],elem[2], elem[4], elem[5]]
            lst_users.append(lst_user)
        sq.connect('new.db').commit()
        return lst_users
    except:
        db_start()
        get_users_lst()

def get_questions_lst():
    try:
        questions = sq.connect('new.db').cursor().execute("SELECT * FROM questions")
        lst_questions = []
        lst_answers = []
        for elem in questions:
            lst_questions.append(elem[1])
            lst_answers.append(elem[2])
        sq.connect('new.db').commit()
        return lst_questions, lst_answers
    except:
        db_start()
        get_questions_lst()

def get_project_lst():
    try:
        projects = sq.connect('new.db').cursor().execute("SELECT * FROM projects")
        lst_project = []
        lst_answer = []
        for elem in projects:
            lst_project.append(elem[1])
            need_els = list(elem[3].split('|'))
            answ = elem[2]+'|\n'
            for people in need_els:
                answ += '\n✔️'+people
            lst_answer.append(answ)
        return lst_project, lst_answer
    except:
        db_start()
        get_project_lst()

# async def edit_user(state, user_id):
#     async with state.proxy() as data:
#         cur.execute("UPDATE users SET ")
