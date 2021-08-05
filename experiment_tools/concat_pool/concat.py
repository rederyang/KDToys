import os


out_log = 'train#p.log'
box = 'box'
max = 100

target = open(out_log, 'w')  # override

try:
    with open(os.path.join(box, 'train#p.log')) as source:
        target.write(source.read()+'\n')
        print(os.path.join(box, 'train#p.log' + ' concated.'))
except FileNotFoundError as e:
    print('train#p.log does not exist and has been skipped.')

for i in range(max):
    file_name = 'train#'+str(i)+'.log'
    source_name = os.path.join(box, file_name)
    if not file_name in os.listdir(box):
        print('reach the end.')
        break
    with open(source_name) as source:
        target.write(source.read())
        print(source_name + ' concated.')
        
target.close()

