from utils.mysql.create import *
from utils.mysql.get import *
from utils.mysql.execute import execute_delete
from utils.mysql.connect import *


# print(create_talent('test'))

# print(create_talent('test'))
#
# print(create_alias('test', 'test'))

t = get_talent('watson')
if t:
    print("t: " + str(t))

# file = open('./talents.json', 'r', encoding='utf-8')
# talents = json.loads(file.read())
# file.close()
#
#
# for t in talents:
#     name = t['full_name']
#
#     print('Creating talent: ' + name)
#     print(create_talent(name))
#
#     print('\tCreating alias: ' + t['name'] + ' for ' + name)
#     print(create_alias(t['name'], name))
#
#     for a in t['aliases']:
#         print('\tCreating alias: ' + a + ' for ' + name)
#         print(create_alias(a, name))
#
#     print('\n')