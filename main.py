import json


def main():
    with open('data.json') as f:
        data = json.load(f)
        print(data)

        languages = data['Languages'][0]
        print(languages)

        langauge = languages['LanguageCode']
        print(langauge)

        print('-------------')


if __name__ == '__main__':
    main()
