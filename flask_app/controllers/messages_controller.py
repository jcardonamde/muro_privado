from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.messages import Message


@app.route('/send_message', methods = ['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    
    Message.save(request.form)
    return redirect('/wall')

@app.route('/delete/message/<int:id>') #Id del mensaje se recibe a través de URL
def destroy_message(id):
    if Message.validate_delete({'id': id , 'receiver_id': session['user_id']}):
        #formulario = {
        #    "id": id
        #}
        Message.destroy({'id': id })
    else:
        ip = request.remote_addr
        return render_template('danger.html', ip = ip, id = id)
    
    return redirect ('/wall')