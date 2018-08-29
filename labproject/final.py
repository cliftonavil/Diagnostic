import re
def c_replace(main_string, change_this, change_with):
    #for string reverse
    reverse_list = []
    for i in change_with:
        reverse_list.insert(0, i)
        join_string = " ".join(reverse_list)
        reversed_final = re.sub(' ', '', join_string)
    #for string change
    string_list=main_string.split(' ')
    new_list = []
    for string in string_list:
        if string !=change_this:
            new_list.append(string)
    new_list.insert(3,reversed_final)
    result=" ".join(new_list)
    return result
main_string = 'Marry had a little lamb.'
change_this = 'little'
change_with = 'big'
replaced_string = c_replace(main_string, change_this, change_with )
print(replaced_string)