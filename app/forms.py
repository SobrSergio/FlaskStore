from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo

from wtforms import BooleanField, PasswordField, SubmitField, TextAreaField, StringField, FileField, IntegerField, SelectField

from models import *





class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Слишком короткий или длинный логин')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат почты')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80, message='Слишком короткий или длинный пароль')])
    submit = SubmitField('Зарегистрироваться')
    
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такой email уже зарегистрирован')
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такой user уже зарегистрирован')
    

class LoginForm(FlaskForm):
    usernameoremail = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')
    remember_me = BooleanField('Запомнить меня')
    
    def validate_usernameoremail(self, usernameoremail): 
        if '@' in usernameoremail.data:
            user = User.query.filter_by(email = usernameoremail.data).first()
            if user is not None:
                 if not user.check_password(self.password.data):
                     raise ValidationError('Введите правильную почту/пароль')
            else:
                raise ValidationError('Введите правильную почту/пароль')
        else:
            user = User.query.filter_by(username = usernameoremail.data).first() 
            if user is not None:
                 if not user.check_password(self.password.data):
                     raise ValidationError('Введите правильное имя/пароль')
            else:
                raise ValidationError('Введите правильное имя/пароль')



class Profileform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Слишком короткий или длинный логин')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат почты')])
    phone = StringField('Phone', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    submit = SubmitField('Сохранить')



class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Cбросить пароль')
    
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунта с такой почтой нет.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password_confirm', validators=[DataRequired(), EqualTo('password', message='Повторный пароль неправильный.')])
    submit = SubmitField('Cбросить пароль')


class AddBrandForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    
    def validate_name(self, name):
        brand = Brand.query.filter_by(name=name.data).first()
        if brand is not None:
            raise ValidationError('Такой бренд уже есть')
        
class DeleteBrandForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def validate_name(self, name):
        brand = Brand.query.filter_by(name=name.data).first()
        if brand is None:
            raise ValidationError('Такой бренд нет')

class DeleteCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is None:
            raise ValidationError('Такой категории нет')



class AddCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    
    def validate_name(self, name):
        сategory = Category.query.filter_by(name=name.data).first()
        if сategory is not None:
            raise ValidationError('Такая категория уже есть')
        

class AddProductsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    size = StringField('size', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Сохранить')
    
    
    def validate_name(self, name):
        product = Products.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Такой продукт уже есть')

class DeleteProductsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def validate_name(self, name):
        product = Products.query.filter_by(name=name.data).first()
        if product is None:
            raise ValidationError('Такого продукта нет')
    


class EditProductsForm(FlaskForm):
    submit = SubmitField('Сохранить')
        

class EditOneProductsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    size = StringField('size', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Сохранить')


class DeliveryForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Слишком короткий или длинный логин')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат почты')])
    phone = StringField('Phone', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    index = StringField('index', validators=[DataRequired()])
    submit = SubmitField('Оформить')
