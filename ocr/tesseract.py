import subprocess
import tempfile
import os.path


class ParsingFailed(Exception):
    pass


keepOneColorPath = os.path.join('keepOneColor', 'dist', 'build', 'keepOneColor',
                                'keepOneColor')


def recognise(imagePath, subtitleColor, language):
    tmpfile = tempfile.NamedTemporaryFile()
    filename, fileExtension = os.path.splitext(imagePath)
    tmpfilePath = tmpfile.name + fileExtension

    try:
        subprocess.check_output([keepOneColorPath, imagePath, tmpfilePath,
                                '--keep', subtitleColor])
        output = subprocess.check_output(['tesseract', tmpfilePath, '-', '-l',
                                         language])
        return output.decode('utf-8', errors='strict').strip()
    except subprocess.CalledProcessError as e:
        raise ParsingFailed(e)

    finally:
        try:
            os.remove(tmpfilePath)
        except OSError:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='''Run tesseract on subtitled
                                     image''')
    parser.add_argument('imagePath', metavar='FILEPATH', type=str,
                        help='Path of a target image')
    parser.add_argument('--lang', dest='language', default='eng',
                        help='language of the subtitles')
    parser.add_argument('--color', metavar='(R, G, B)', type=str, dest='color',
                        help='language of the subtitles',
                        default='(255, 255, 0)')

    args = parser.parse_args()

    print recognise(args.imagePath, args.color, args.language).encode('utf-8')
