parentheses = ['()', '[]', '{}']
text  = '()'.replace(' ', '')

for i in range(len(text)//2):
    for j in parentheses:
        text = text.replace(j, '')

if len(text)==0:
    print('Nice')
else:
    print('Bruh')