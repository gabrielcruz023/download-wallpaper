#! /usr/bin/python

import sys, random, WallhavenApi, ctypes, urllib3

urllib3.disable_warnings()

search_term, resolutions, is_sfw, category, wallpaper_path = sys.argv[1:]

api_parameters = { "sorting": "random", "page": 1 }
api_parameters["resolutions"] = resolutions
api_parameters["purity_" + is_sfw] = True
api_parameters["category_" + category] = True
api_parameters["search_query"] = search_term

wallhaven = WallhavenApi.WallhavenApi(verify_connection=True)
new_wallpaper = random.choice(wallhaven.get_images_numbers(**api_parameters))
wallpaper_url = wallhaven.get_image_short_url(image_number=new_wallpaper)

with open("wallpaper_log.txt", 'r+') as logfile:
	content = logfile.readlines()
	content.append(wallpaper_url + '\n')
	logfile.writelines(content)

wallhaven.download_image(image_number=new_wallpaper, file_path=wallpaper_path)

ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)