from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)
# rotas

@app.route('/') # rota home
def home():
    return render_template("index.html") # rederiza a página 

@app.route('/chat') # rota chat
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room: 
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

# parte do servidor 

@socketio.on('send_message') # quando enviar uma mensagem, o servidor recebe a informação
def handle_send_message_event(data):
    app.logger.info("{} enviou uma mensagem na sala: {}".format(data['username'],
                                                                data['room']))
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room') # quando alguém entrar na sala, o servidor recebe a informação
def handle_join_room_event(data):
    app.logger.info("{} entrou na sala {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)