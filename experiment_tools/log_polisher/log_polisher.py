import sys
import re


def is_epoch_line(line:str):
    return re.search(r'Epoch \d+/\d+', line) is not None


def is_train_line(line:str):
    return re.search(r'\d{2}:\d{2}:\d{2} train', line) is not None


def is_valid_line(line:str):
    return re.search(r'\d{2}:\d{2}:\d{2} valid', line) is not None


def parse(line:str, state):
    """ extract the useful line depending on the state
    """
    if state == 0 and is_epoch_line(line):  # need epoch
        return line, 1  
    elif state == 1 and is_train_line(line):  # need train
        return line, 2
    elif state == 2:  # got train, need valid
        if is_epoch_line(line):
            return line, 1  
        elif is_valid_line(line):
            return line, 0  

    return None, state


source_path = sys.argv[1]
target_path = sys.argv[2]

try:
    source = open(source_path)
except FileNotFoundError as e:
    print(e)
    sys.exit()

target = open(target_path, 'w')

state = 0  # need epoch line at the begining

for line in source:
    content, state = parse(line, state)
    if content:
        target.write(content)

source.close()
target.close()



