# Maryam Sajjad
# mas454
# 11285700
# CMPT 317 - Jeff Long


import io
import sys


def create_constraints(players_list, values_list, result_dict):
    # do nested loop to create keys for the dictionary, making sure no keys have duplicate players
    for player in range(len(players_list)):
        for player2 in range(len(players_list)):
            if players_list[0] == players_list[player2]:
                pass
            else:
                # create a list of tuples to show the values that this constraint allows. currently has all values and
                # doesn't take constraints into account
                values_to_add = []
                for value in values_list:
                    for value2 in values_list:
                        values_to_add.append((value, value2))
                # add to dictionary
                result_dict[players_list[0], players_list[player2]] = values_to_add
        players_list.remove(players_list[0])


def check_constraints(constraints, result, variables):
    """
    checks the constraints, and based on if its friends, enemies, or veto, calls the appropriate function
    :param constraints: list of constraints provided in the given file
    :param result: the dictionary including all constraints to return
    :param variables: players in the given file
    """
    for player in variables:  # going to see each player in variables
        # print(player)
        for constraint in constraints:  # loop through specific constraints
            # print(constraint)
            if player == constraint[0]:  # is this player == first value in constraint?
                if constraint[1] == "friend":  # both players in key tuple need to be mentioned
                    friend_constraint(result, (constraint[0], constraint[2]))  # going to loop through the
                elif constraint[1] == "enemy":  # both players in key tuple need to be mentioned
                    enemy_constraint(result, (constraint[0], constraint[2]), (constraint[2], constraint[0]))
                elif constraint[1] == "vetos":  # only one player needs to be mentioned.
                    veto_constraint(result,
                                    constraint[2], constraint[0])  # only need to look out for the value to remove
                    # and which key has player


def friend_constraint(result, key_tuple):
    """all results for certain player pairing must have same games"""
    placeholder = result[key_tuple].copy()
    for value in placeholder:
        if value[0] != value[1]:
            result[key_tuple].remove(value)


def enemy_constraint(result, key_tuple, alt_key_tuple):
    """all results for certain player pairing must have different games"""
    if key_tuple not in result:
        placeholder = result[alt_key_tuple].copy()
        key_tuple = alt_key_tuple
    else:
        placeholder = result[key_tuple].copy()
    for value in placeholder:
        if value[0] == value[1]:
            result[key_tuple].remove(value)


def veto_constraint(result, vetoed_game, player):
    """
        excludes game for any player that has vetoed it.
        for all keys in dict, check if player in key. if yes, then iterate through
        all values, and any value including game, remove value.
    """
    for key in result:
        if player == key[0]:
            placeholder = result[key].copy()
            for value in placeholder:  # iterates through all acceptable values in this constraint
                if vetoed_game == value[0]:  # if vetoed game is in a value, remove it
                    result[key].remove(value)
        elif player == key[1]:
            placeholder = result[key].copy()
            for value in placeholder:  # iterates through all acceptable values in this constraint
                if vetoed_game == value[1]:  # if vetoed game is in a value, remove it
                    result[key].remove(value)


def main():
    """
    main function, takes the file given as argument when running the file. separates the values and variables and
    constraints to set up the program to run nicely. calls my functions that do the other work. lastly, it prints the
    resulting dictionary of constraints to a file.
    """
    file_name = sys.argv[1]
    constraints = []
    result = dict()
    with io.open(file_name, 'r') as raf:
        lines = raf.readlines()
        variables = lines[0].strip('\n').split(' ')
        values = lines[1].strip('\n').split(' ')
        for line in range(len(lines)):
            if line > 1:
                constraints.append(lines[line].strip('\n').split(' '))
    variables_list = variables.copy()
    create_constraints(variables, values, result)
    check_constraints(constraints, result, variables_list)

    # constraints will be output to a file in the same directory. looks ugly but it is correct. if it were to comply
    # with json dumps, then the keys and my other code has issues since my tuples turned into a string.
    output_file_name = "new.txt"
    with io.open(output_file_name, "w") as waf:
        waf.write(str(result))


if __name__ == "__main__":
    main()
