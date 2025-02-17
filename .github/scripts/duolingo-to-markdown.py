import requests, os, sys
from bs4 import BeautifulSoup


def duolingo_request():
    username = os.getenv('DUOLINGO_USERNAME')
    url = f"https://www.duolingo.com/2017-06-30/users?username={username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

    return response.json()


def get_duolingo_info(data):
    num_language = int(os.getenv('DUOLINGO_LANGUAGE_LENGTH'))
    user_data = data.get('users', [{}])[0]
    streak = user_data['streak']
    xp_per_language = {}
    for course in user_data.get('courses', []):
        name = course.get('title', 'Unknown')
        xp = course.get('xp', 0)
        if xp > 0:
            xp_per_language[name] = xp

    lang_list = list()
    for lang, xp in xp_per_language.items():
        lang_list.append((xp, lang))
    lang_list.sort(reverse=True)
    lang_list = lang_list[:num_language]
    
    return streak, lang_list

def update_readme(streak, lang_list):
    username = os.getenv('DUOLINGO_USERNAME')
    with open('README.md', 'r', encoding='utf-8') as file:
        readme = file.readlines()
    duolingo_line_index = readme.index('<!-- duolingo -->\n') + 1
    duolingo_line = '<p align="center"><img src="https://d35aaqx5ub95lt.clo'\
                    'udfront.net/images/dc30aa15cf53a51f7b82e6f3b7e63c68.svg">'\
                    f'Duolingo username: <strong> {username} </strong> </br>' 
    duolingo_line += f'Last Streak: <strong> {streak} </strong> <img'\
            ' width="20.5px" height="15.5px" src="https://d35aaqx5ub95lt.'\
            'cloudfront.net/vendor/398e4298a3b39ce566050e5c041949ef.svg"></br>'


    duolingo_line += """<table align="center"><tr><th>Language</th><th>Experience</th></tr>"""
    for lang in lang_list:
        duolingo_line += f"""<tr><th>{lang[1]} </th><th><span><img width="20.5px" height="15.5px" src=\
                "https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"\
                ><span >{lang[0]}</span></span></th></tr>"""
    if (readme[duolingo_line_index] == duolingo_line):
        sys.exit(0)
    else:
        duolingo_line = duolingo_line + '</table></p> \n'
        readme[duolingo_line_index] = duolingo_line
    with open('README.md', 'w', encoding='utf-8') as file:
        file.writelines(readme)


a, b = get_duolingo_info(duolingo_request())
update_readme(a, b)

