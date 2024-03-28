import pdb

from requests import request

from const import kitsu_api_base,  kitsu_headers

test = request('GET', f'{kitsu_api_base}/anime/4555', headers=kitsu_headers)

with open('./data/test_data.json', 'w') as outfile:
  outfile.write(test._content.decode('utf-8'))