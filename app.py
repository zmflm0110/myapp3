from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mathlog-secret-key'

users = {
    'admin': '1234',
    'user1': 'pass1',
}

records = []
next_id = 1


@app.route('/')
def index():
    return render_template('index.html', records=records)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 로그인 확인
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('mypage'))
        else:
            error = '아이디 또는 비밀번호가 틀렸습니다.'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/mypage')
def mypage():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('mypage.html', username=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        global next_id
        title = request.form['title'].strip()# 사용자의 실수 공백이나 빈칸 입력 방지
        difficulty = int(request.form['difficulty'])
        reason = request.form['reason'].strip()
        records.append({
            'id': next_id,#인덱스로 사용
            'username': session['username'],
            'title': title,
            'difficulty': difficulty,
            'reason': reason,
        })
        next_id += 1
        return redirect(url_for('index'))
    return render_template('add.html')



@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    global records
    new_records = []
    for r in records:
        if r['id'] == record_id and r['username'] == session['username']:
            pass
        else:
            new_records.append(r)
    records = new_records
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
