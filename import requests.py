import requests
import json
from operator import itemgetter

class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_fotos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'extended': 1, 'count': 5, 'album_id': 'profile'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_albums(self):
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {'owner_id': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        #new_path = file_path.replace("\\", "/")
        list_path = file_path.split('/')
        res = requests.get(f'{URL}/upload?path=vkfoto/{list_path[-1]}&overwrite=true', headers=headers).json()
        with open(file_path, 'rb') as f:
            try:
                result = requests.put(res['href'], files={'file':f})
                print(result)
            except KeyError:
                print(res)

def saveLinkToFile(link, filename):
    req = requests.get(link)
    with open(filename, 'wb') as file:
        file.write(req.content)

if __name__ == '__main__':
    with open('key.txt') as f:
        vk_token = f.readline()
        ya_token = f.readline()

    listfoto = []
    user_id = '4565454'
    vk = VK(vk_token, user_id)

    fotos = vk.get_fotos()
    for foto in fotos['response']['items']:
        dict = {}
        max_foto = max(foto['sizes'], key=itemgetter('height'))
        filename = str(foto['likes']['count'])+'.png'
        filename_full = 'downloads/' + filename
        saveLinkToFile(max_foto['url'], filename_full)
        dict['file_name'] = filename
        dict['size'] = max_foto['height']
        listfoto.append(dict)
        
    with open('result.json', 'w') as filejson:
        json.dump(listfoto, filejson)

    uploader = YaUploader(ya_token)
    for foto in listfoto:
        result = uploader.upload('downloads/' + foto['file_name'])

