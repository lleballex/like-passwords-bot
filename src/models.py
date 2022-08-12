import hashlib

import jwt
import peewee
from aiogram.utils.markdown import escape_md 

from misc import db
from misc import ENCRYPTION_ALGORITHM


class User(peewee.Model):
    user_id = peewee.IntegerField()
    key = peewee.CharField()

    class Meta:
        database = db
        db_table = 'users'

    def _encode_key(self, key: str):
        return hashlib.md5(bytes(key, 'utf8')).hexdigest()

    @classmethod
    def create(cls, **query):
        query['key'] = cls._encode_key(cls, query['key'])
        return super().create(**query)

    def check_key(self, key: str):
        return self.key == self._encode_key(key)


class Password(peewee.Model):
    user = peewee.ForeignKeyField(User, related_name='passwords')
    source = peewee.CharField()
    password = peewee.CharField()
    email = peewee.CharField(null=True)
    username = peewee.CharField(null=True)
    phone = peewee.CharField(null=True)

    class Meta:
        database = db
        db_table = 'passwords'

    def _decipher_field(self, field, key):
        return jwt.decode(field, key,
                          algorithms=[ENCRYPTION_ALGORITHM])['value']

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
            query[i] = jwt.encode({'value': query[i]},
                                  key, algorithm=ENCRYPTION_ALGORITHM)
        query['user'] = user
        query['source'] = source

        return super().create(**query)
    
    def update_fields(self, key: str, **fields):
        for field in fields:
            if field != 'source' and fields[field]:
                fields[field] = jwt.encode({'value': fields[field]}, key,
                                           algorithm=ENCRYPTION_ALGORITHM)
            setattr(self, field, fields[field])
        self.save()

    def get_message(self):
        text = (f'🌐 Источник: `{escape_md(self.source)}`\n'
                f'🔑 Пароль: `{escape_md(self.password)}`\n')

        if self.email:
            text += f'📧 Email: `{escape_md(self.email)}`\n'
        if self.username:
            text += f'💬 Логин: `{escape_md(self.username)}`\n'
        if self.phone:
            text += f'☎️ Телефон: `{escape_md(self.phone)}`\n'

        return text
