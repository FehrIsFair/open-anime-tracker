import pdb

from requests import request

from const import kitsu_api_base,  kitsu_headers

anime_id = '47132'

test = request('GET', f'{kitsu_api_base}/anime/{anime_id}', headers=kitsu_headers)

with open(f'./data/{anime_id}.json', 'w') as outfile:
  outfile.write(test._content.decode('utf-8'))