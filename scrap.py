import requests
import re
import json
from bs4 import BeautifulSoup
import os


def login_into_site(login_url):
    """Log into www.guitaredomination.com site."""

    config = load_config()

    print("Logging as " + config['login'] + ' in ' + login_url)

    s = requests.session()
    p = s.get(login_url)

    soup = BeautifulSoup(p.text, "html.parser")
    div = soup.find_all('input', {'id': '_mgmnonce_user_login'})

    match = re.search(r'value=\"(.*)\"', str(div))
    if match:
        user_login = match.group(1)

    payload = {'log': config['login'],
               'pwd': config['password'],
               'wp-submit': 'Connexion',
               'testcookie': '1',
               'redirect_to': '',
               '_mgmnonce_user_login': user_login,
               '_wp_http_referer': '/login/'}

    r = s.post(login_url, data=payload)

    if r.status_code == 200:
        print("Loggin Ok")
    else:
        print("An error occured while trying to log in " + login_url)
        print("Error code " + r.status_code)

    return s


def get_list_of_lessons(s, url):
    """ Return a list of links to video guitar lessons."""
    p = s.get(url)

    soup = BeautifulSoup(p.text, "html.parser")
    lessons_links = list()
    for link in soup.find_all('a'):
        if url in link.get('href'):
            lessons_links.append(link.get('href'))

    return lessons_links


def get_list_of_audio_lessons(s, url):
    """ Return a list of links to audio guitar lessons."""
    p = s.get(url)

    soup = BeautifulSoup(p.text, "html.parser")
    lessons_links = list()
    for link in soup.find_all('a'):
        if 'mp3' in link.get('href'):
            lessons_links.append(url + '/' + link.get('href'))

    return lessons_links


def get_url_last_part(url):
    """ Return the last part of url."""
    l = url.rsplit('/', 1)
    return l[-1]


def extract_video_link_from_script(html_page):
    """Extract from javascript links to private vimeo channels."""

    soup = BeautifulSoup(html_page, "html.parser")
    js = soup.find_all('script')

    match = re.search(r'progressive\":(.*)', str(js))
    if match:
        str1 = match.group(1)

    match = re.search(r'},\"ga_account.*', str(js))
    if match:
        str2 = match.group(0)

    str1 = str1.replace(str2, '')

    data = json.loads(str1)
    score = 0
    result = data[0]
    for d in data:
        if(d['height'] * d['width'] > score):
            score = d['height'] * d['width']
            result = d

    return result


def get_video_link_from_url(s, url):
    """Extract script in iframe where all videos links are present."""

    p = s.get(url)
    soup = BeautifulSoup(p.content, "html.parser")

    try:
        r = s.get(soup.iframe['src'], headers={'Referer': url})
        return extract_video_link_from_script(r.content)
    except:
        return None


def download_content(url, file_name):
    """Download content from url and store it into file_name."""
    import urllib.request
    print("Downloading " + file_name)
    if not os.path.exists(file_name):
        urllib.request.urlretrieve(url, file_name)
    print("Done")


def load_config():
    '''Load the config file from disk.'''
    with open('config.json') as f:
        return json.load(f)


if __name__ == '__main__':

    #
    # Log into the site
    #
    login_url = 'http://www.guitaredomination.com/login/'
    s = login_into_site(login_url)

    courses_base_url = "http://www.guitaredomination.com/mes-cours/"
    modules = ['gd-debutant', 'gd-lead', 'gd-blues1', 'gd-blues2']

    for module in modules:

        module_dir = module
        if not os.path.exists(module_dir):
            os.mkdir(module_dir)

        url = courses_base_url + module
        print(url)

        #
        # Downloading audio lessons
        #
        audio_url = 'http://www.guitaredomination.com/wp-content/uploads/trackjams/'
        audio_lessons = get_list_of_audio_lessons(s, audio_url + module)

        for lesson in audio_lessons:
            audio_file = get_url_last_part(lesson)

            audio_file = audio_file.replace('_', '-')
            match = re.search(r'^(\d)-', audio_file)
            if match:
                audio_file = '0' + audio_file

            download_content(lesson, module_dir + '/lecon-' + audio_file)

        #
        # Downloading video lessons
        #
        lessons = get_list_of_lessons(s, url)
        for lesson in lessons:
            video_link = get_video_link_from_url(s, lesson)
            if video_link is None:
                print("No video in " + get_url_last_part(lesson))
            else:
                video = get_url_last_part(lesson)
                match = re.search(r'lecon-(\d)-', video)
                if match:
                    video = video.replace('lecon-', 'lecon-0')
                download_content(video_link['url'], module_dir + '/' + video + '.mp4')
