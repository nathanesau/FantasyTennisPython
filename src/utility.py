# utility program for downloading data (not used in application)

from downloadDialog import *
from drawParser import *

years = [2015, 2016]

for year in years:
    tmp_dir = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"
    data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/" + str(year) + "/"
    html_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_data/" + str(year) + "/"

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(html_dir):
        os.mkdir(html_dir)

    downloadArchive(year=year, out_dir=tmp_dir)
    download_options = getDownloadOptions()

    url_list = []
    tourney_names = []
    for url in download_options.values():
        if url.rfind('archive') != -1 or url.rfind('current') != -1:
            url_list.append("https://www.atptour.com" + url)
            if url.rfind('archive') != -1:
                tourney_name = url[url.rfind('archive') + len("archive") + 1:]
                tourney_name = tourney_name[:tourney_name.find('/')]
                tourney_names.append(tourney_name)
            elif url.rfind('current') != -1:
                tourney_name = url[url.rfind('current') + len("current") + 1:]
                tourney_name = tourney_name[:tourney_name.find('/')]
                tourney_names.append(tourney_name)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    for i in range(len(url_list)):
        fname = html_dir + tourney_names[i] + ".html"
        url = url_list[i]
        req = Request(url=url, headers=headers)
        try:
            html = urlopen(req).read()
        except:
            print("cannot open url")
            continue
        html_file = open(fname, "w")
        html_file.write(html.decode("utf-8"))
        html_file.close()

    for i in range(len(tourney_names)):
        html_file = tourney_names[i] + ".html"
        db_file = html_file.replace(".html", ".db")
        try:
            html_to_db(html_dir + html_file, data_dir + db_file)
        except:
            print("error in html_to_db (.html file not exist?)")
            continue
