from dataclasses import dataclass
from src.types.paysites import Paysite, Service_User, Service_Post


@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return ""


@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return ""


@dataclass
class Kemono_Dev(Paysite):
    name: str = 'kemono-dev'
    title: str = 'Kemono Dev'
    user: User = User()
    post: Post = Post()
    color: str = '#808080'
