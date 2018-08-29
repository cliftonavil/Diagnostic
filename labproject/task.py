import re
change_with = 'clifton'
reverse_list = []
for i in change_with:
    reverse_list.insert(0, i)
    y=" ".join(reverse_list)
    reversed_final=re.sub(' ', '', y)
print(reversed_final)

