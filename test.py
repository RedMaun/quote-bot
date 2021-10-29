# from iteration_utilities import deepflatten

# a = [
#     [{'id': 504931958, 'link': 'https://vk.com/id504931958', 'name': 'Никита Гурба', 'text': 'бубрздум', 'images': []}], 
#     [{'id': 504931958, 'link': 'https://vk.com/id504931958', 'name': 'Никита Гурба', 'text': 'да', 'images': []}, 
#     [{'id': 504931958, 'link': 'https://vk.com/id504931958', 'name': 'Никита Гурба', 'text': '', 'images': []}]]
#     ]
# n = {'id': 504931958, 'link': 'https://vk.com/id504931958', 'name': 'Никита Гурба', 'text': 'бубрздум', 'images': []}

# def search(a, n):
#     for i in range(len(a)):
#         if (not(isinstance(a[i], list))):
#             if a[i] == n:
#                 h.append(i)
#                 return h
#         else:
#             h.append(i)
#             search(a[i], n, h)

#     # return list(deepflatten(b))


# test = search(a, n)
# print(test, a[0][0])
# s = 'a'
# for i in test:
#     s += '[{}]'.format(i)

# exec(s + ' = 1')
# print(a)

a = [1, 2, [3, 4, 5]]
exec('a = ' + str(a).replace('3', '1'))
print(a)