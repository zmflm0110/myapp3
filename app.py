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
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = '아이디 또는 비밀번호가 틀렸습니다.'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/record')
def record():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = session['username']
    user_records = [r for r in records if r['username'] == user]
    return render_template('record.html', records=user_records)


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
        title = request.form['title'].strip()
        difficulty = int(request.form['difficulty'])
        reason = request.form['reason'].strip()
        records.append({
            'id': next_id,
            'username': session['username'],
            'title': title,
            'difficulty': difficulty,
            'reason': reason,
        })
        next_id += 1
        return redirect(url_for('record'))
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
    return redirect(url_for('record'))


if __name__ == '__main__':
    app.run(debug=True)
