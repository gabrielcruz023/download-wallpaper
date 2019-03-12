from os.path import realpath, isfile, join
from os import makedirs
import WallhavenApi
import argparse
import ctypes


def get_filename(path: str) -> str:
    """
    Recebe um caminho e retorna o caminho do arquivo a ser baixado.
    """
    path = realpath(path)
    if isfile(path):
        return path

    try:
        makedirs(path)
    except FileExistsError:
        pass

    return join(path, 'Wallpaper.jpg')


def main():
    parser = argparse.ArgumentParser(
        description=('Baixa um wallpaper aleatório do Wallhaven e o define '
                     'como seu wallpaper.'))
    parser.add_argument(
        '-s', '--search', required=True, help='Termo de busca.')
    parser.add_argument(
        '-r',
        '--resolution',
        metavar=('width', 'height'),
        type=int,
        nargs=2,
        required=True,
        help='Resolução do wallpaper.')
    parser.add_argument(
        '-o',
        '--output',
        required=True,
        help='Caminho do arquivo que será baixado.')
    parser.add_argument(
        '-c',
        '--category',
        choices=['general', 'anime', 'people'],
        default='general',
        help='Categoria do wallpaper.')
    parser.add_argument(
        '-nsfw', action='store_true', help='Busca inclusive conteúdo NSFW.')
    parser.add_argument(
        '-set',
        action='store_true',
        help='Definir ou não o arquivo baixado como wallpaper.')
    args = parser.parse_args()

    params = {
        'sorting': 'random',
        'page': 1,
        'resolutions': 'x'.join(map(str, args.resolution)),
        'purity_nsfw': args.nsfw,
        'purity_sfw': not args.nsfw,
        'search_query': args.search,
        'category_' + args.category: True
    }

    w_api = WallhavenApi.WallhavenApi(verify_connection=True)
    w_ids = w_api.get_images_numbers(**params)
    w_path = get_filename(args.output)

    try:
        w_api.download_image(image_number=w_ids[0], file_path=w_path)
    except IndexError:
        print('A busca não retornou resultados.')
        raise
    except Exception:
        print('Ocorreu um erro inesperado ao baixar o wallpaper.')
        raise
    else:
        print('Wallpaper baixado com sucesso.')

    if args.set:
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, w_path, 0)
        except Exception:
            print('Não foi possível alterar o wallpaper do sistema.')


if __name__ == '__main__':
    main()
