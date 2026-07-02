# from neomodel import (
#     StructuredNode,
#     StringProperty,
#     IntegerProperty,
#     BooleanProperty,
#     FloatProperty,
#     DateProperty,
#     DateTimeProperty,
#     EmailProperty,
#     ArrayProperty,
#     JSONProperty,
#     get_config
# )
from datetime import date, datetime
from neomodel import *

config = get_config()
config.database_url = "bolt://<username>:<password>@localhost:7687"

class Person(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    age = IntegerProperty()

class Company(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class types(StructuredNode):
    name = StringProperty(index=True)
    age = IntegerProperty()
    types = BooleanProperty()
    money = FloatProperty()
    now_date = DateProperty()
    now_datetime = DateTimeProperty()
    email = EmailProperty()
    hobbies = ArrayProperty(StringProperty())
    json_data = JSONProperty()
    default_value = StringProperty(default="Default Value")
    required_field = StringProperty(required=True)
    unique_field = StringProperty(unique_index=True)

class worker(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    age = IntegerProperty()
    works = RelationshipTo('types', 'Friends')

class Student(StructuredNode):
    name = StringProperty(required=True)
    friends = RelationshipTo("Student", "FRIEND")
    wokers = RelationshipFrom('Company', 'WORKS')

class friendrel(StructuredRel):
    close_friend = BooleanProperty(default=False)
    since = IntegerProperty(default=2023)

class guy(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    age = IntegerProperty()
    friends = RelationshipTo('guy', 'FRIENDS', model=friendrel)
    @property
    def friends_count(self):
        return self.name

# Skipper = Person(name="Skipper", age=21).save()
# Ghost= Person(name="Ghost", age=22).save()
# print(f"Created: {Skipper.name}, Age: {Skipper.age}")
# for person in Person.nodes:
#     print(f"Name: {person.name}, Age: {person.age}, ID: {person.element_id}")

# google=Company(name='Google').save()
# microsoft=Company(name='Microsoft').save()
# for company in Company.nodes:
#     print(f"Company Name: {company.name}, ID: {company.element_id}")


# data = types(
#     name="Skipper",
#     age=21,
#     types=True,
#     money=1000.50,
#     now_date=date.today(),
#     now_datetime=datetime.now(),
#     email="Skipper@gmail.com",
#     hobbies=["Reading", "Traveling", "Coding"],
#     json_data={"key1": "value1", "key2": "value2"},
#     required_field="This field is required",
#     unique_field="Unique Value"
# ).save()
# print(data)

# data = types(
#     name="Ghost",
#     age=22,
#     types=False,
#     money=456454.54,
#     now_date=date.today(),
#     now_datetime=datetime.now(),
#     email="naught@gmail.com",
#     hobbies=["playiing", "Traveling", "doctor"],
#     json_data={"key1": "value1", "key2": "value2"},
#     # required_field="This field is required",
#     required_field='',
#     unique_field="Unique Value"
# ).save()
# print(data)

# types2 = types(
#     name="Rahul",
#     age=22,
#     is_types=True,
#     money=15000.50,
#     now_date=date(2004, 8, 14),
#     now_datetime=datetime.now(),
#     email="rahul@gmail.com",
#     hobbies=["Java", "Spring Boot", "Football"],
#     json_data={
#         "theme": "light",
#         "language": "Hindi",
#         "notifications": False
#     },
#     required_field="Full Stack Developer",
#     unique_field="STU002"
# )

# types2.save()

# types3 = types(
#     name="Priya",
#     age=20,
#     is_types=True,
#     money=18000,
#     now_date=date(2006, 1, 10),
#     now_datetime=datetime.now(),
#     email="priya@gmail.com",
#     hobbies=["React", "JavaScript", "UI Design"],
#     json_data={
#         "theme": "dark",
#         "language": "English",
#         "notifications": True
#     },
#     required_field="Frontend Developer",
#     unique_field="STU003"
# )

# types3.save()

# types4 = types(
#     name="Anjali",
#     age=23,
#     is_types=False,
#     money=50000,
#     now_date=date(2003, 11, 18),
#     now_datetime=datetime.now(),
#     email="anjali@gmail.com",
#     hobbies=["Machine Learning", "Python", "TensorFlow"],
#     json_data={
#         "theme": "light",
#         "language": "Kannada",
#         "notifications": True
#     },
#     required_field="AI Engineer",
#     unique_field="STU004"
# )

# types4.save()

# types5 = types(
#     name="David",
#     age=24,
#     is_types=False,
#     money=72000.90,
#     now_date=date(2002, 6, 30),
#     now_datetime=datetime.now(),
#     email="david@gmail.com",
#     hobbies=["Docker", "Kubernetes", "AWS"],
#     json_data={
#         "theme": "dark",
#         "language": "English",
#         "notifications": False
#     },
#     required_field="DevOps Engineer",
#     unique_field="STU005"
# )

# types5.save()



# worker1 = worker(name="Skipper", age=21).save()
# worker1=worker.nodes.get(name="Skipper")

# worker2 = worker(name="Ghost", age=22).save()
# worker3 = worker(name="Rahul", age=23).save()
# for worker in worker.nodes:
#     print(f"Name: {worker.name}, Age: {worker.age}, ID: {worker.element_id}")

# worker1.works.connect(types.nodes.get(unique_field="STU001"))


# g=Company.nodes.get(name="Google")
# print(g)
# user1 = Student.nodes.get(name="user1")
# user1.wokers.connect(g)

# print(Student.nodes.all())
# user1 = Student(name="user1").save()
# user1 = Student.nodes.get(name="user1")
# rahul = Student.nodes.get(name="Rahul")
# user1.friends.disconnect(rahul)

# rahul = Student(name="Rahul").save()
# user1.friends.connect(rahul)
# rahul.friends.connect(user1)
# krishna = Student(name="krishna").save()
# balram = Student(name="balram").save()
# krishna = Student.nodes.get(name="krishna")
# balram = Student.nodes.get(name="balram")
# krishna.friends.connect(Student.nodes.get(name="balram"))
# balram.friends.connect(Student.nodes.get(name="user1"))
# user1.friends.connect(krishna)
#     print(k)
# for k in Student.nodes:

# for k in Company.nodes.all():
#     print(k)
#     k.delete()

# for k in Student.nodes.all():
#     print(k)
#     k.delete()

# for k in types.nodes.all():
#     print(k)
#     k.delete()

# for k in Person.nodes.all():
#     print(k)
#     k.delete()

# for k in worker.nodes.all():
#     print(k)
#     k.delete()

# rel=user1.friendrel.relationship(rahul)
# rel.since=2023
# rel.save()

# Skipper = Person(name="Skipper", age=21).save()
# krishna = Person(name="Krishna", age=22).save()
# ravi = Person(name="Ravi", age=23).save()


# Skipper = guy.nodes.get_or_none(name="Skipper") or guy(
#     name="Skipper", age=21).save()
# krishna = guy.nodes.get_or_none(name="Krishna") or guy(
#     name="Krishna", age=22).save()
# ravi = guy.nodes.get_or_none(name="Ravi") or guy(name="Ravi", age=23).save()

# Skipper.friends.connect(krishna, properties={
#                          'close_friend': True, 'since': 2022})
# Skipper.friends.connect(
#     ravi, properties={'close_friend': False})

# Skipper = guy.nodes.get(name="Skipper")

# print(Skipper.friends.is_connected(krishna) ) # Returns True
# # Skipper.friends.disconnect(ravi)  # Disconnects the relationship
# Skipper.friends.disconnect_all()  # Disconnects all relationships
# for friend in Skipper.friends:
#         rel = Skipper.friends.relationship(friend)
#         print(f"{Skipper.name} is friends with {friend.name}, Close Friend: {rel.close_friend}, Since: {rel.since}")
# user1=guy.nodes.get_or_none(name="user1")
# print(user1)
# Skipper=guy.nodes.filter(name__icontains="Skipper").first()
# Skipper=guy.nodes.filter(name__contains="Skipper")
# Skipper=guy.nodes.filter(name__endswith="mar").first()
# Skipperl=guy.nodes.filter(name__endswith="mar").first()
# Skippers=guy.nodes.filter(name__startswith="sa")
# print(Skipper.name)
# print(Skipper)
# print(Skipperl.name)
# agel=guy.nodes.filter(age__gt=21).first()
# print(agel.name)
# print(agel.age)
# print(agel.friends_count)
# age1 = guy.nodes.exclude(age__lt=22).first()
# print(age1.name)
# age = guy.nodes.filter(name='Skipper').first()
# print(age.name)
# print(guy.nodes.filter(name__icontains='Skipper').exists())
# count(),order_by('age'),distinct(),exists(),first(),last(),get_or_none(),get_or_create(),filter(),exclude()


# def get_friends_till_hop(person, max_hop=3, visited=None, current_hop=0):
#     if visited is None:
#         visited = set()

#     if current_hop > max_hop or person.name in visited:
#         return

#     visited.add(person.name)

#     for friend in person.friends.all():
#         print(f"{'  ' * current_hop}Hop {current_hop}: {friend.name}")
#         if current_hop < max_hop:
#             get_friends_till_hop(friend, max_hop, visited, current_hop + 1)


# age = guy.nodes.filter(name='Skipper').first()
# if age:
#     get_friends_till_hop(age, max_hop=3)


