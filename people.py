people = []
def add_people(people):
    person_add = input("Enter a name to be added: ")
    people.append(person_add)
def remove_people(people):
    person_remove = input("Enter a name to be removed: ")
    people.pop(person_remove)