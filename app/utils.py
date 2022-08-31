

from flask_mail import Message

from flask import url_for

from app import mail


def send_reset_email(user): #принимается пользователь которому нужно отправить письмо
    token = user.get_reset_token() #использвует функцию создающую токен. (models.py)
    msg = Message('Запрос на смену пароля',
                  sender='SneakShop.ru@gmail.com', #отправител
                  recipients=[user.email]) #кому отправить
    msg.body = f"""
    Здравствуйте, {user.username}.

    На SneakShop был запрошен новый пароль для вашего аккаунта

    Имя пользователя: {user.username}.

    Если вы не отправляли этот запрос, просто проигнорируйте это сообщение. 
    
    Если хотите продолжить:
    Перейдите по этой ссылке чтобы сбросить свой пароль:  (Ссылка станет не действительной через 30 минут после отправки этого письма)
    {url_for('reset_token', token=token, _external=True)}

    Thanks for reading.

    """ #_external = True чтобы получить абсолютный url адрес!
    mail.send(msg)