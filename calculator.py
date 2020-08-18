# Simple Calculator with Python

# helper functions
def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_operation(op):
    if op == "+" or "-" or "*" or "/" or "%":
        return True
    else:
        return False


def current_evaluation(first_num):
    def id_operation(op, second_num):
        switcher = {
            "+": first_num + second_num,
            "-": first_num - second_num,
            "*": first_num * second_num,
            "/": first_num / second_num,
            "%": first_num % second_num,
        }
        return switcher.get(op, "Error! Unknown format during evaluation")

    return id_operation


# main calculator function


def calculator(equation_tokens):
    first_in_equation = True
    next_is_num = None
    current_operation = None
    current_total = 0

    for x in equation_tokens:
        if first_in_equation:
            if is_number(x):
                current_total = float(x)
                first_in_equation = False
                next_is_num = False
            else:
                print('Error. Equation is not formatted correctly. Please try again')
                break
        elif next_is_num:
            if is_number(x):
                second_num = float(x)
                evaluation = current_evaluation(current_total)
                current_total = evaluation(current_operation, second_num)
                next_is_num = False
            else:
                print('Error. Equation is not formatted correctly. Please try again')
                break
        else:
            if is_operation(x):
                current_operation = x
                next_is_num = True
            else:
                print('Error. Equation is not formatted correctly. Please try again')
                break
    return current_total


def operations_order_evaluate(tokens_list, op):
    operation_num = tokens_list.count(op)
    while operation_num != 0:
        op_order_tokens = tokens_list[tokens_list.index(op) - 1: tokens_list.index(op) + 2]
        curr_evaluate = calculator(op_order_tokens)
        tokens_list.insert(tokens_list.index(op) + 2, curr_evaluate)
        del tokens_list[tokens_list.index(op) - 1: tokens_list.index(op) + 2]
        operation_num -= 1
    return tokens_list


def evaluate_brackets(tokens_list):
    bracket_tokens = tokens_list
    beginning_bracket = 0
    ending_bracket = 0
    if "(" not in bracket_tokens and beginning_bracket == 0:
        return tokens_list
    else:
        beginning_bracket = len(bracket_tokens) - 1 - bracket_tokens[::-1].index("(")
        ending_bracket = bracket_tokens.index(")")
        while "(" in bracket_tokens:
            bracket_tokens = bracket_tokens[bracket_tokens.index("(") + 1: len(bracket_tokens) - 1 - bracket_tokens[::-1].index(")")]
        bracket_tokens = operations_order_evaluate(bracket_tokens, "/")
        bracket_tokens = operations_order_evaluate(bracket_tokens, "*")
        curr_value = calculator(bracket_tokens)
        tokens_list.insert(ending_bracket + 1, curr_value)
        del tokens_list[beginning_bracket: ending_bracket + 1]
        return evaluate_brackets(tokens_list)

# The calculator will continuously prompt user to input equations until they type in exit.


def continuous_interaction():
    i = ''
    while i != 'exit':
        math_equation = input("Input a math equation using the following characters, each separated by a space.\n"
                              "/ = division, * = multiplication, + = addition, - = subtraction, % = modulo.\n"
                              "Example: 12 * 12\n"
                              "You may use brackets in your equations.\n"
                              "Example: 12 * ( 1 + 9 ) / 9\n"
                              "Type in exit when done\n"
                              "Enter equation: ")
        i = math_equation
        if math_equation == 'exit':
            break
        tokens = math_equation.split()
        print(tokens)
        tokens = evaluate_brackets(tokens)
        tokens = operations_order_evaluate(tokens, "/")
        tokens = operations_order_evaluate(tokens, "*")
        print(calculator(tokens))
    print("You have exited out of the calculator")


continuous_interaction()
