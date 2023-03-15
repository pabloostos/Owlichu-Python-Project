#%%
import requests


api_key = 'a34fb0de-1934-49c0-8afa-80d65f0a2856'

word = 'hello'

def get_word_definition(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        if 'meta' in data and 'id' in data['meta']:
            word_id = data['meta']['id']
            if ('def' in data) and ('sseq' in data['def'][0]) and ('dt' in data['def'][0]['sseq'][0][0][1]):
                definitions = data['def'][0]['sseq'][0][0][1]['dt'][0][1]
                return word_id, definitions
            else:
                return word, None
        else:
            return None
    else:
        return None

palabra = get_word_definition(word)
if palabra:
    print(f'''
    {palabra[0]}
    {palabra[1]}''')
# %%
string = 'Hola watoakj.'

for x in string:
        if not (x.isalpha() or x.isspace()): 
            print(True)
        else: print(False)


# %%
from datetime import datetime
return datetime.utcnow()

# %%


