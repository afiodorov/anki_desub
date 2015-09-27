from microsofttranslator import Translator
import json

with open('bingToken.json') as tokenFile:
    token = json.load(tokenFile)

translator = Translator(token["clientID"], token["clientSecret"])


def translate(text, langTo, langFrom):
    return translator.translate(text, langTo, from_lang=langFrom)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='''Run Bing translate''')
    parser.add_argument('--from', dest='langFrom', metavar='LANG', type=str,
                        help='from language')
    parser.add_argument('to', default='eng', metavar='LANG',
                        type=str, help='target language')
    parser.add_argument('text', metavar='text', type=str,
                        help='text to translate')

    args = parser.parse_args()

    print translate(args.text, args.to, args.langFrom).encode('utf-8')
