from misc import db
from misc import ENCRYPTION_ALGORITHM

import jwt
import hashlib
from peewee import Model
from aiogram.utils.markdown import bold
from peewee import IntegerField, CharField, ForeignKeyField


class User(Model):
	user_id = IntegerField()
	key = CharField()

	class Meta:
		database = db
		db_table = 'users'

	def _encode_key(self, key):
		return hashlib.md5(bytes(key, 'utf8')).hexdigest()

	@classmethod
	def create(cls, **query):
		query['key'] = cls._encode_key(cls, query['key'])
		return super().create(**query)

	def check_key(self, key):
		return self.key == self._encode_key(key)


class Password(Model):
	user = ForeignKeyField(User, related_name='passwords')
	source = CharField()
	password = CharField()
	email = CharField(null=True)
	username = CharField(null=True)
	phone = CharField(null=True)

	class Meta:
		database = db
		db_table = 'passwords'

	def _decipher_field(self, field, key):
		return jwt.decode(field, key, algorithms=[ENCRYPTION_ALGORITHM])['value']

	def decipher(self, key):
		self.password = self._decipher_field(self.password, key)

		if self.email:
			self.email = self._decipher_field(self.email, key)
		if self.username:
			self.username = self._decipher_field(self.username, key)
		if self.phone:
			self.phone = self._decipher_field(self.phone, key)

		return self

	@classmethod
	def create(cls, **query):
		key = query.pop('key')
		user = query.pop('user')
		source = query.pop('source')

		for i in query.keys():
			query[i] = jwt.encode({'value': query[i]}, key, algorithm=ENCRYPTION_ALGORITHM)
		query['user'] = user
		query['source'] = source

		return super().create(**query)

	def get_text_data(self):
		text = (f'Источник: {bold(self.source)}\n'
				f'Пароль: {bold(self.password)}\n')

		if self.email:
			text += f'Email: {bold(self.email)}\n'
		if self.username:
			text += f'Логин: {bold(self.username)}\n'
		if self.phone:
			text += f'Телефон: {bold(self.phone)}\n'

		return text