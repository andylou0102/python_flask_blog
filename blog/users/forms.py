from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.model import User


class RegistrationForm(FlaskForm):
    username = StringField('名稱', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('信箱', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[DataRequired()])
    check_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('信箱已被使用 請更換其他組信箱')

class LoginForm(FlaskForm):
    email = StringField('信箱', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember = BooleanField('記住我')
    submit = SubmitField('登入')

class AccountUpdateForm(FlaskForm):
    username = StringField('名稱', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('信箱', validators=[DataRequired(), Email()])
    image = FileField('更改個人照片', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('信箱已被使用 請更換其他組信箱')

class RequestResetForm(FlaskForm):
    email = StringField('信箱', validators=[DataRequired(), Email()])
    submit = SubmitField('發送')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('沒有符合的帳號. 請先註冊該信箱')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密碼', validators=[DataRequired()])
    check_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

class ContectForm(FlaskForm):
    name = StringField('名稱', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('信箱', validators=[DataRequired(), Email()])
    phone_number = IntegerField('電話號碼', validators=[DataRequired()])
    message = TextAreaField('回覆', validators=[DataRequired()])
    submit = SubmitField('Send')