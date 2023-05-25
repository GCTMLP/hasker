from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View, CreateView
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm, LoginForm
from .models import Profile

import json
import re


class Register(CreateView):
	"""
	Функция валидации формы регистрации
	"""
	form_class = RegistrationForm
	template_name = 'register.html'
	success_url = "/"
	
	def form_valid(self, form):
		res = super().form_valid(form)
		user = form.save()
		if user:
			file_name = form.cleaned_data['username'] +'_'+ \
						self.request.FILES['photo'].name
			# Проходим процедуру сохранения фотографии 
			# (в отдельной таблице хранится путь до фото
			# у конкретного пользователя)

			Profile.objects.create(photo=file_name, 
								user_id=user.id)
			# Вызывае функцию сохранения файла
			handle_uploaded_file(self.request.FILES['photo'].file, file_name)
			# Залогиниваемся от вновь зарегистрированного пользователя 
			# и перенаправлеям его на страницу вопросов
			login(self.request, user)
		return res


def handle_uploaded_file(f, save_name):
	"""
	Функция сохранения аватарки при регистрации
	"""
	f.seek(0)
	file = open(settings.MEDIA_ROOT+'/'+save_name, 'wb')
	file.write(f.read())


class SignUp(LoginView):
	"""
    Функция валидации формы входа
    """
	form_class = LoginForm
	template_name = 'login.html'
	success_url = "/"

	def form_valid(self, form):
		res = super().form_valid(form)
		user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				login(self.request, user)
		return res


class SettingsView(TemplateView):
	"""
	Показываем основной шаблон страницы настройки (шаблон изначально пустой,
	все данные подгружаются в него через vue.js ajax запросом)
	"""
	template_name = "settings.html"


class SettingsViewData(View):
	"""
	Класс обработки ajax запроса. Полученаем инфорацию о пользователе
	и рендерим ее для отправки обратно в js
	"""
	def post(self, request):
		#try:
			session_user = request.user.id
			qs = Profile.objects.select_related('user').get(
				user_id=int(session_user))
			data = {}
			data['email'] = qs.user.email
			data['foto'] = settings.MEDIA_URL+qs.photo
			data['login'] = qs.user.username
			return JsonResponse(json.dumps(data), safe=False)
		# except:
		# 	return JsonResponse('false', safe=False)


class SettingsChangeData(View):
	"""
	Класс обработки ajax запроса. Полученаем инфорацию которую необходимо 
	изменить у пользователя (login, email, avatar)
	"""
	def post(self, request):
		# Получаем данные о сессии 
		session_user = request.user.id
		session_user_name = request.user.username
		# Данные приходят в виде FormData, их них мы получаем картинку,
		# если она была изменена. Затем мы ее сохраняем в папку с аватарками
		try:
			name = '/'+session_user_name + '_' + re.findall(
				r'filename="([\s\S]*?)"', str(request.body))[0]
			data = (request.body.split(b"\r\n\r\n")[1])
			f = open(settings.MEDIA_ROOT + name, 'wb')
			f.write(data)
			profile = Profile.objects.get(user_id=session_user)
			profile.photo = name
			profile.save()
		# Если картинка не была изменена
		except:
			pass
		try:

			# Получаем login и email из формы и записываем их в базу
			login = re.findall(r'login"\\r\\n\\r\\n([\s\S]*?)\\r',
							   str(request.body))[0]
			email = re.findall(r'email"\\r\\n\\r\\n([\s\S]*?)\\r',
							   str(request.body))[0]
			user = User.objects.get(id=session_user)
			user.username = login
			user.email = email
			user.save()
			return JsonResponse('true', safe=False)
		except:
			return JsonResponse('false', safe=False)
