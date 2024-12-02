import math
import re

scoping_mode = 'dynamic'  # Toggle between 'dynamic' and 'static'
class LimitedDict(dict):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity

    def __setitem__(self, key, value):
        if len(self) >= self.capacity:
            raise MemoryError("dictfull: Exceeded dictionary capacity")
        super().__setitem__(key, value)

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Pop from an empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Peek from an empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __repr__(self):
        return str(self.items)

    def __getitem__(self, index): # allows access to stack
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]

    def __len__(self):
        return len(self.items)

def toggle_scoping():
    global scoping_mode
    if scoping_mode == 'dynamic':
        scoping_mode = "static"
    else:
        scoping_mode = "dynamic"
    print(f"Scoping mode is: {scoping_mode}")
def process_boolean(value):
    if value == "true":
        return (True, True)
    elif value == "false":
        return (True, False)
    else:
        return False

def process_number(value):
    try:
        float_value = float(value)
        if float_value.is_integer():
            return (True, int(float_value))
        else:
            return (True, float_value)
    except ValueError:
        return False

def process_code_block(value):
    if len(value) >= 2 and value.startswith("{") and value.endswith("}"):
        return (True, value[1:-1].split())

def process_name_constant(value):
    if value.startswith("/"):
        return (True, value)


def process_string(value):
    if value.startswith("(") and value.endswith(")"):
        return (True, value[1:-1])

def process_constants(input):
    res = process_boolean(input)
    res = res or process_number(input)
    res = res or process_code_block(input)
    res = res or process_name_constant(input)
    res = res or process_string(input)
    return res


def process_input(input):
    # Use regular expression to split input while preserving parentheses-enclosed strings
    tokens = re.findall(r'\{.*?}|\(.*?\)|\S+', input)
    # Process each token in the sequence
    for token in tokens:
        result = process_constants(token)
        if result:
            operand_stack.push(result[1])
        else:
            lookup_in_dictionary(token)


def lookup_in_dictionary(input):
    if scoping_mode == 'dynamic':
        # For dynamic scoping, look in the most recent dictionary (top of the stack)
        top_dict = dictionary_stack.peek()
        if input in top_dict:
            value = top_dict[input]
        else:
            print(f"'{input}' not found in current dictionary")
            return
    elif scoping_mode == 'static':
        # For lexical scoping, look in the outermost dictionary (first dictionary in the stack)
        for dictionary in dictionary_stack.items:
            if input in dictionary:
                value = dictionary[input]
                break
        else:
            print(f"'{input}' not found in any dictionary")
            return


    if callable(value):
        value()
    elif isinstance(value, list):
        for item in value:
            process_input(item)
    else:
        operand_stack.push(value)
    top_dict = dictionary_stack.peek()
    # if input in top_dict:
    #     value = top_dict[input]
    # elif input in global_dict:
    #     value = global_dict[input]
    if input in global_dict:
        value = global_dict[input]
    else:
        print(" not in dictionary ")
        return
    if callable(value):
        value()
    elif isinstance(value, list):
        for item in value:
            process_input(item)
    else:
        operand_stack.push(value)




def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.lower() == 'quit':
            break
        process_input(user_input)
        print(f"Operand Stack: {operand_stack}")
        #print(f"Dictionary Stack: {dictionary_stack}")


###################################################
# Arithmatic Operations
def add_operation():
    if operand_stack.size() >= 2:
        op1 = operand_stack.pop()
        op2 = operand_stack.pop()
        res = op1 + op2
        operand_stack.push(res)
    else:
        print(" not enough operands")


def sub_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        res = op1 - op2
        operand_stack.push(res)
    else:
        print(" not enough operands")


def mul_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        res = op1 * op2
        operand_stack.push(res)
    else:
        print(" not enough operands")


def div_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        res = op1 / op2

        operand_stack.push(res)
    else:
        print(" not enough operands")


def idiv_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        res = op1 // op2

        operand_stack.push(res)
    else:
        print(" not enough operands")

def mod_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        res = op1 % op2
        operand_stack.push(res)
    else:
        print(" not enough operands")


def abs_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        if op > 0:
            res = op
        else:
            res = op * (-1)
        operand_stack.push(res)
    else:
        print(" not enough operands")


def neg_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        if op > 0:
            res = op * (-1)
        else:
            res = op
        operand_stack.push(res)
    else:
        print(" not enough operands")


def ceiling_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        res = math.ceil(op)
        operand_stack.push(res)
    else:
        print(" not enough operands")


def floor_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        res = math.floor(op)
        operand_stack.push(res)
    else:
        print(" not enough operands")


def is_halfway(value):
    fractional_part, integer_part = math.modf(value)
    return fractional_part == 0.5 or fractional_part == -0.5


def round_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        if is_halfway(op) and op > 0: # round up
            res = math.ceil(op)
        else:
            res = round(op)
        operand_stack.push(res)
    else:
        print(" not enough operands")


def sqrt_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        res = op * op
        operand_stack.push(res)
    else:
        print(" not enough operands")


###################################################
# Stack manipulations
def exch_operation():
    if operand_stack.size() >= 2:
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        operand_stack.push(op2)
        operand_stack.push(op1)
    else:
        print(" not enough operands")


def pop_operation():
    if operand_stack.size() >= 1:
        operand_stack.pop()
    else:
        print(" not enough operands")


def copy_operation():
    if operand_stack.size() >= 1:
        copyNums = operand_stack.pop()
        if copyNums > operand_stack.size():
            print(" range check error")
        else:
            for i in range(copyNums):
                operand_stack.push(operand_stack[i])
    else:
        print ("not enough operands")


def dup_operation():
    if operand_stack.size() >= 1:
        dup = operand_stack.peek()
        operand_stack.push(dup)
    else:
        print(" not enough operands")


def clear_operation():
    for i in range(operand_stack.size()):
        operand_stack.pop()


def count_operation():
    if operand_stack.size() >= 1:
        operand_stack.push(operand_stack.size())
    else:
        operand_stack.push(0)

###################################################
# Dictionary
def dict_operation():
    if operand_stack.size() >= 1:
        # valid
        capacity = operand_stack.pop()
        if not isinstance(capacity, int) or capacity < 0:
            print("Error: Capacity must be a nonnegative integer")
            return
        newDict = LimitedDict(capacity)
        operand_stack.push(newDict)
    else:
        print(" not enough operands")


def length_operation():
    if operand_stack.size() >= 1:
        top = operand_stack.pop()
        if isinstance(top, dict) or isinstance(top, str):
            operand_stack.push(len(top))
        else:
            print(" top of stack is not a dictionary")
    else:
        print( "not enough operands")


def maxLength_operation():
    if operand_stack.size() >= 1:
        tempDict = operand_stack.pop()
        maxLeng = tempDict.capacity
        operand_stack.push(maxLeng) # push max capacity
    else:
        print (" not enough operands")


def begin_operation():
    if operand_stack.size() >= 1:
        tempDict = operand_stack.pop()
        if isinstance(tempDict, dict):
            dictionary_stack.push(tempDict)
        else:
            print(" top of stack is not dictionary")
    else:
        print (" not enough operands")


def end_operation():
    if dictionary_stack.size() > 1:
        dictionary_stack.pop()
    else:
        print(" dict stack underflow")


def def_operation():
    if operand_stack.size() >= 2:
        value = operand_stack.pop()
        name = operand_stack.pop()

        if isinstance(name, str) and name.startswith("/"):
            key = name[1:]
            dictionary_stack.peek()[key] = value
        else:
            operand_stack.push(name)
            operand_stack.push(value)
    else:
        print(" not enough operands")


##########################################################
# Strings
def get_operation():
    if operand_stack.size() >= 2:
        index = operand_stack.pop()
        string = operand_stack.pop()
        if index >= len(string):
            print (" range check error")
            return
        else:
            operand_stack.push(string[index])


def getinterval_operation():
    if operand_stack.size() >= 3:
        endIndex = operand_stack.pop()
        startIndex = operand_stack.pop()
        string = operand_stack.pop()
        res = ""
        if startIndex > endIndex or startIndex < 0 or endIndex >= len(string):
            print(" range check error")
            return
            # Extract the substring from startIndex to endIndex (inclusive)
        for i in range(startIndex, endIndex + 1):
            res += string[i]
        operand_stack.push(res)
    else:
        print(" not enough operands")


def putinterval_opeartion():
    if operand_stack.size() >= 3:
        newStr = operand_stack.pop()
        index = operand_stack.pop()
        string = operand_stack.pop()
        res = ""
        if index < 0 or index > len(string):
            print(" range check error")
            return
        for i in range(index):
            res += string[i]
        res += newStr
        operand_stack.push(res)
    else:
        print(" not enough operands")


###########################################################
# Bit and Boolean operations
def eq_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 == obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 == obj2
        else:
            result = obj1 == obj2
        operand_stack.push(result)
    else:
        print(" not enough operands")


def ne_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 != obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 != obj2
        else:
            result = obj1 != obj2
        operand_stack.push(result)
    else:
        print(" not enough operands")


def ge_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 >= obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 >= obj2
        else:
            try:
                result = obj1 >= obj2
            except TypeError:
                print("Error: Unsupported comparison between types.")
                return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def gt_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 > obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 > obj2
        else:
            try:
                result = obj1 > obj2
            except TypeError:
                print("Error: Unsupported comparison between types.")
                return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def le_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 <= obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 <= obj2
        else:
            try:
                result = obj1 <= obj2
            except TypeError:
                print("Error: Unsupported comparison between types.")
                return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def lt_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, (int, float)) and isinstance(obj2, (int, float)):
            result = obj1 < obj2
        elif isinstance(obj1, str) and isinstance(obj2, str):
            result = obj1 < obj2
        else:
            try:
                result = obj1 < obj2
            except TypeError:
                print("Error: Unsupported comparison between types.")
                return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def and_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, bool) and isinstance(obj2, bool):
            result = obj1 and obj2
        elif isinstance(obj1, int) and isinstance(obj2, int):
            result = obj1 & obj2
        else:
            print("Error: operands must be either both booleans or both integers.")
            return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def or_operation():
    if operand_stack.size() >= 2:
        obj2 = operand_stack.pop()
        obj1 = operand_stack.pop()
        if isinstance(obj1, bool) and isinstance(obj2, bool):
            result = obj1 or obj2
        elif isinstance(obj1, int) and isinstance(obj2, int):
            result = obj1 | obj2
        else:
            print("Error: operands must be either both booleans or both integers.")
            return
        operand_stack.push(result)
    else:
        print(" not enough operands")


def not_operation():
    if operand_stack.size() >= 1:
        op = operand_stack.pop()
        if isinstance(op, bool):
            result = not op
        elif isinstance(op, int):
            result = ~op
        else:
            print("Unsupported type for 'not' operation")
            return
        operand_stack.push(result)
    else:
        print(" not enough operands")


####################################################
# Flow Control
def if_operation():
    if operand_stack.size() >= 2:
        proc = operand_stack.pop()
        boolean = operand_stack.pop()
        if boolean:
            for token in proc:  # Process each token in the procedure
                process_input(token)
    else:
        print(" not enough operands")


def ifelse_operation():
    if operand_stack.size() >= 3:
        proc2 = operand_stack.pop()
        proc1 = operand_stack.pop()
        boolean = operand_stack.pop()
        if boolean:
            for token in proc1:  # Process each token in the procedure
                process_input(token)
        else:
            for token in proc2:  # Process each token in the procedure
                process_input(token)
    else:
        print(" not enough operands")


def for_operation():
    if operand_stack.size() >= 4:
        proc = operand_stack.pop()
        limit = operand_stack.pop()
        increment = operand_stack.pop()
        initial = operand_stack.pop()
        current = initial
        while (increment > 0 and current <= limit) or (increment < 0 and current >= limit):
            operand_stack.push(current)
            for token in proc:  # Process each token in the procedure
                process_input(token)
            current += increment
    else:
        print(" not enough operands")


def repeat_operation():
    if operand_stack.size() >= 3:
        proc = operand_stack.pop()
        count = operand_stack.pop()
        for _ in range(count):
            for token in proc:  # Process each token in the procedure
                process_input(token)
    else:
        print(" not enough operands")


####################################################
# Input and Output
def print_operation():
    if operand_stack.size() >= 1:
        string = operand_stack.pop()
        if isinstance(string, str):
            print(f"{string}")
        else:
            print(" print only works with strings")
            return
    else:
        print(" not enough operands")


def equalsign_operation():
    if operand_stack.size() >= 1:
        val = operand_stack.pop()
        print(f"{val}")
    else:
        print(" not enough operands")


def doubleequalsign_operation():
    if operand_stack.size() >= 1:
        val = operand_stack.pop()
        if isinstance(val, str):
            print(f"({val})")
        else:
            print(f"{val}")
    else:
        print(" not enough operands")


# utilized CHATGPT for this function that isn't required, I used it to test other functions.
def put_operation():
    if operand_stack.size() >= 3:
        value = operand_stack.pop()
        index_or_key = operand_stack.pop()
        target = operand_stack.pop()

        if isinstance(target, list):
            if isinstance(index_or_key, int):
                if 0 <= index_or_key < len(target):
                    target[index_or_key] = value
                else:
                    print("Rangecheck error: Index out of bounds.")
                    return
            else:
                print("Invalid operand: Expected integer index for array.")
                return

        elif isinstance(target, str):
            if isinstance(index_or_key, int):
                if 0 <= index_or_key < len(target):
                    target = target[:index_or_key] + value + target[index_or_key + 1:]
                else:
                    print("Rangecheck error: Index out of bounds.")
                    return
            else:
                print("Invalid operand: Expected integer index for string.")
                return

        elif isinstance(target, dict):
            if isinstance(index_or_key, str):
                if isinstance(target, LimitedDict) and len(target) >= target.capacity:
                    print("Error: dictfull: Exceeded dictionary capacity.")
                    return
                target[index_or_key] = value
            else:
                print("Invalid operand: Expected string key for dictionary.")
                return
        else:
            print("Invalid operand: Expected array, string, or dictionary.")
            return
        operand_stack.push(target)
    else:
        print("Not enough operands")



operand_stack = Stack()
dictionary_stack = Stack()
dictionary_stack.push({})

dictionary_stack.peek()["add"] = add_operation
dictionary_stack.peek()["def"] = def_operation
dictionary_stack.peek()["sub"] = sub_operation
dictionary_stack.peek()["mul"] = mul_operation
dictionary_stack.peek()["div"] = div_operation
dictionary_stack.peek()["idiv"] = idiv_operation
dictionary_stack.peek()["mod"] = mod_operation
dictionary_stack.peek()["abs"] = abs_operation
dictionary_stack.peek()["neg"] = neg_operation
dictionary_stack.peek()["ceiling"] = ceiling_operation
dictionary_stack.peek()["floor"] = floor_operation
dictionary_stack.peek()["round"] = round_operation
dictionary_stack.peek()["sqrt"] = sqrt_operation
dictionary_stack.peek()["exch"] = exch_operation
dictionary_stack.peek()["pop"] = pop_operation
dictionary_stack.peek()["copy"] = copy_operation
dictionary_stack.peek()["dup"] = dup_operation
dictionary_stack.peek()["clear"] = clear_operation
dictionary_stack.peek()["count"] = count_operation
dictionary_stack.peek()["dict"] = dict_operation
dictionary_stack.peek()["length"] = length_operation
dictionary_stack.peek()["maxlength"] = maxLength_operation
dictionary_stack.peek()["begin"] = begin_operation
dictionary_stack.peek()["end"] = end_operation
dictionary_stack.peek()["put"] = put_operation
dictionary_stack.peek()["get"] = get_operation
dictionary_stack.peek()["getinterval"] = getinterval_operation
dictionary_stack.peek()["putinterval"] = putinterval_opeartion
dictionary_stack.peek()["eq"] = eq_operation
dictionary_stack.peek()["ne"] = ne_operation
dictionary_stack.peek()["ge"] = ge_operation
dictionary_stack.peek()["gt"] = gt_operation
dictionary_stack.peek()["le"] = le_operation
dictionary_stack.peek()["lt"] = lt_operation
dictionary_stack.peek()["and"] = and_operation
dictionary_stack.peek()["or"] = or_operation
dictionary_stack.peek()["not"] = not_operation
dictionary_stack.peek()["if"] = if_operation
dictionary_stack.peek()["ifelse"] = ifelse_operation
dictionary_stack.peek()["for"] = for_operation
dictionary_stack.peek()["repeat"] = repeat_operation
dictionary_stack.peek()["print"] = print_operation
dictionary_stack.peek()["="] = equalsign_operation
dictionary_stack.peek()["=="] = doubleequalsign_operation
dictionary_stack.peek()["toggle"] = toggle_scoping

global_dict = {
    "add": add_operation,
    "def": def_operation,
    "sub": sub_operation,
    "mul": mul_operation,
    "div": div_operation,
    "idiv": idiv_operation,
    "mod": mod_operation,
    "abs": abs_operation,
    "neg": neg_operation,
    "ceiling": ceiling_operation,
    "floor": floor_operation,
    "round": round_operation,
    "sqrt": sqrt_operation,
    "exch": exch_operation,
    "pop": pop_operation,
    "copy": copy_operation,
    "dup": dup_operation,
    "clear": clear_operation,
    "count": count_operation,
    "dict": dict_operation,
    "length": length_operation,
    "maxlength": maxLength_operation,
    "begin": begin_operation,
    "end": end_operation,
    "put": put_operation,
    "get": get_operation,
    "getinterval": getinterval_operation,
    "putinterval": putinterval_opeartion,
    "eq": eq_operation,
    "ne": ne_operation,
    "ge": ge_operation,
    "gt": gt_operation,
    "le": le_operation,
    "lt": lt_operation,
    "and": and_operation,
    "or": or_operation,
    "not": not_operation,
    "if": if_operation,
    "ifelse": ifelse_operation,
    "for": for_operation,
    "repeat": repeat_operation,
    "print": print_operation,
    "=": equalsign_operation,
    "==": doubleequalsign_operation,
    "toggle": toggle_scoping
}


repl()


