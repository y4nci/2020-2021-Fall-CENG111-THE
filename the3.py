amount, used, coefficient = [], [], 1
# Those are some variables that will come into handy in the functions.


def tree(lst):  

    # This function turns the input to a legitimate tree.
    # Trees will look like this:
    # ["parent", 2, ["node1", 1, [price1]], ["node2", 2, ["node3", 1, [price3]]]]

    global used
    strlst = str(lst)  # I know this isn't the most noble way to solve this problem, but it works quite good.
    root = [ele for ele in [_ele_[0] for _ele_ in lst] if strlst.count(f"'{ele}'") == 1][0]  # That is the root.

    def convert_to_nested(main, string_list, original_list):  # We need a recursive function.
        global used
        index = string_list[:string_list.find(f"'{main}'")].count("]")

        # strlst.index() will give us the index of the element in the string; however, we don't want this.
        # We need the index in the list. To do that, the function calculates the number of "]"s before the
        # index in the strlst, thus giving us the index of the element in the list.

        if index in used:
            index = string_list[:string_list.find(f"'{main}'", string_list.find(f"'{main}'") + 1)].count("]")
        index -= (index >= len(original_list))  # If index exceeds the length, we will subtract it by 1.
        used.append(index)

        # I used "used" (no pun intended) to keep record of the used indexes. Since str.find() would return the
        # same number over and over again, I needed to tell it that it has been on that index previously to
        # prevent getting stuck in an infinite loop. Best way to do that was to assign a global variable.

        part = original_list[index]
        output = [part[0]]

        if type(part[1]) == float:
            output.extend([1, [original_list[index][1]]])

        else:
            for sub in part[1:]:
                output.extend([sub[0], convert_to_nested(sub[1], string_list, original_list)])

        return output

    used = []  # We need to refresh the list. Otherwise it would be keeping the old indexes.

    return convert_to_nested(root, strlst, lst)  # Done, we have a tree now.


def calculate_price(part_list):
    def calculator(lst):
        total_price = 0

        if type(lst[2][0]) == float:
            total_price += lst[2][0]

        else:
            total_price += sum([lst[lst.index(subpart) - 1] * calculator(subpart) for subpart in lst[2::2]])

        return total_price

    nested_form = tree(part_list)
    return calculator(nested_form)


def required_parts(part_list):  # Here, we will get involved with more global variables.
    global amount  # This is to keep record of the required amounts.
    basics = [part[0] for part in part_list if type(part[1]) == float]  # The name says it all.
    amount = [0 for i in range(len(basics))]  # It will start as a list of 0's, obviously.

    def amount_finder(lst, basic, co=1):
        global amount
        global coefficient

        # "coefficient" is quite important here. Each time the tree branches out, it is also multiplied with
        # a number -sometimes 1- and it definitely has to be considered. We want it to be stable yet easily
        # changeable, so a global variable will do the job for us.

        if type(lst[2][0]) == float:
            amount[basic.index(lst[0])] += 1 * co

        else:
            index = 1
            for subpart in lst[2::2]:
                mul = lst[index]
                coefficient *= mul
                amount_finder(subpart, basic, coefficient)
                coefficient = int(coefficient / mul)
                index += 2

        return amount

    nested_form = tree(part_list)
    return list(zip(amount_finder(nested_form, basics), basics))


def stock_check(part_list, stock_list):
    required_list, stock, missing = required_parts(part_list), [], []

    for stc in stock_list:
        stock += [stc[1], stc[0]]

    for req in required_list:
        part, required_amount = req[1], req[0]

        if part not in stock:
            missing.append((part, required_amount))

        elif part in stock and stock[stock.index(part)+1] < required_amount:
            missing.append((part, required_amount - stock[stock.index(part)+1]))

    return missing
