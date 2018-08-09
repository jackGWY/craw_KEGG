import os
from lxml import etree
import requests
import urllib
import time
import pymysql

def get_url(url,src):
    img_url_head = txt_wrap_by("//", "/", url)
    imgPath = url.split("//")[0] + "//" + img_url_head + src
    return imgPath

def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def crawKeggToDatabase(url):
    #host_list_len=len(host_list)
    #count_host=0
    time.sleep(20)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    #headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # proxie={"http":host_list[count_host]}
    # if count_host>host_list_len-1:
    #     count_host=0
    # else:count_host=count_host+1
    data = requests.get(url, headers=headers).text
    s = etree.HTML(data)
    value = {
        "kegg_id": "None",
        "kegg_url":"None",
        "Formula": "None",
        "imgPath": "None",
        "pic_kegg_structure": "None",
        "Target_href": "None",
        "Target_id": "None",
        "Pathway_href": "None",
        "Pathway_name": "None",
        "img_pathway_path": "None",
        "pic_kegg_pathway": "None",
        "Structure_map_href": "None",
        "Structure_map_name": "None",
        "Structure_map_title": "None",
        "img_Structure_path": "None",
        "pic_kegg_structure_map": "None"
    }

    for i in range(1, 20):

        Item = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/th/nobr/text()')
        if Item == []:
            print("None")
        else:
            Item = Item[0].strip()
            print(Item)
            if Item == "Entry":
                kegg_id = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(
                    i) + ']/td/table/tr/td[1]/code/nobr/text()')
                print("kegg_id:", kegg_id)
                if kegg_id == None or kegg_id == []:
                    kegg_id = "None"

                else:
                    kegg_id = kegg_id[0].strip().split()[0]
                    print("kegg_id:", kegg_id)
                    value["kegg_id"]=kegg_id
                    value["kegg_url"]=url
            if Item == "Formula":
                Formula = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/td/div/text()')
                print("Formula:", Formula)
                if Formula == None or Formula == []:
                    Formula = "None"

                else:
                    Formula = Formula[0].strip()
                    print("Formula:", Formula)
                    value["Formula"]=Formula
            if Item == "Structure":
                src = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/td/a[1]/@href')
                print("src:", src)
                if src == None or src == []:
                    src="#"
                else:
                    src = src[0].strip()
                    print("src:", src)

                    img_url_head = txt_wrap_by("//", "/", url)

                    imgPath = url.split("//")[0] + "//" + img_url_head + src
                    print("imgPath:", imgPath)
                    value["imgPath"]=imgPath
                    try:
                        f = open(".." + os.sep + "pic_kegg_structure" + os.sep + kegg_id + ".gif", 'wb')
                        time.sleep(20)
                        # proxie = {"http": host_list[count_host]}
                        # if count_host > host_list_len - 1:
                        #     count_host = 0
                        # else:
                        #     count_host = count_host + 1
                        f.write((urllib.request.urlopen(imgPath)).read())

                        f.close()
                        value["pic_kegg_structure"]=kegg_id + ".gif"
                    except Exception as e:
                        print("file write Exception:", e)

            if Item == "Target":
                Target_href = s.xpath(
                    '/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/td/div/a[1]/@href')
                Target_id = s.xpath(
                    '/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/td/div/a[1]/text()')
                print("Target_href:", Target_href)
                print("Target_id:", Target_id)
                if Target_href == None or Target_href == [] or Target_id == None or Target_id == []:
                    Target_href = "#"
                    Target_id = "None"

                else:
                    Target_href = Target_href[0].strip()
                    Target_href=get_url(url,Target_href)
                    print("Target_href:", Target_href)
                    value["Target_href"]=Target_href
                    Target_id = Target_id[0].strip()
                    print("Target_id:", Target_id)
                    value["Target_id"]=Target_id
                f_drug = open('E:' + os.sep + 'paindatabase' + os.sep + 'craw_KEGG'
                              + os.sep + 'Target_kegg_id.txt', 'a')
                f_drug.writelines(Target_id + " " + Target_href + " " + kegg_id + " " + url + '\n')
                f_drug.close()

            if Item == "Pathway":
                Pathway_href = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(
                    i) + ']/td/table/tr/td[1]/nobr/a/@href')
                Pathway_name = s.xpath(
                    '/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(
                        i) + ']/td/table/tr/td[1]/nobr/a/text()')
                print("Pathway_href:", Pathway_href)
                print("Pathway_name:", Pathway_name)
                if Pathway_href == None or Pathway_href == [] or Pathway_name == None or Pathway_name == []:
                    Pathway_href = "#"
                    Pathway_name = "None"

                else:
                    Pathway_href = Pathway_href[0].strip()
                    Pathway_href = get_url(url, Pathway_href)
                    print("Pathway_href:", Pathway_href)
                    value["Pathway_href"]=Pathway_href
                    Pathway_name = Pathway_name[0].strip()
                    print("Pathway_name:", Pathway_name)
                    value["Pathway_name"]=Pathway_name

                    url3 = Pathway_href
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
                    time.sleep(20)
                    # proxie = {"http": host_list[count_host]}
                    # if count_host > host_list_len - 1:
                    #     count_host = 0
                    # else:
                    #     count_host = count_host + 1
                    data3 = requests.get(url3, headers=headers).text
                    s3 = etree.HTML(data3)
                    img_pathway_path = s3.xpath('/html/body/img/@src')
                    if img_pathway_path == None or img_pathway_path == []:
                        img_pathway_path = "None"

                    else:
                        img_pathway_path = img_pathway_path[0].strip()
                        img_pathway_path = get_url(url3, img_pathway_path)
                        print("img_pathway_path:", img_pathway_path)
                        value["img_pathway_path"]=img_pathway_path
                        try:
                            f = open(".." + os.sep + "pic_kegg_pathway" + os.sep + kegg_id + ".png", 'wb')
                            time.sleep(20)
                            # proxie = {"http": host_list[count_host]}
                            # if count_host > host_list_len - 1:
                            #     count_host = 0
                            # else:
                            #     count_host = count_host + 1
                            f.write((urllib.request.urlopen(img_pathway_path)).read())
                            f.close()
                            value["pic_kegg_pathway"]=kegg_id + ".png"
                        except Exception as e:
                            print("file write Exception:", e)

            if Item == "Structure map":
                Structure_map_href = s.xpath('/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(
                    i) + ']/td/table[1]/tr/td[1]/nobr/a/@href')
                Structure_map_name = s.xpath(
                    '/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(
                        i) + ']/td/table[1]/tr/td[1]/nobr/a/text()')
                Structure_map_title = s.xpath(
                    '/html/body/div/table/tr/td/form/table/tr/td/table/tr[' + str(i) + ']/td/table[1]/tr/td[2]/text()')
                print("Structure_map_href:", Structure_map_href)
                print("Structure_map_name:", Structure_map_name)
                print("Structure_map_title:", Structure_map_title)
                if Structure_map_href == None or Structure_map_href == [] or Structure_map_name == None or Structure_map_name == []:
                    Structure_map_href = "#"
                    Structure_map_name = "None"

                else:
                    Structure_map_href = Structure_map_href[0].strip()
                    Structure_map_href = get_url(url, Structure_map_href)
                    print("Structure_map_href:", Structure_map_href)
                    value["Structure_map_href"]=Structure_map_href
                    Structure_map_name = Structure_map_name[0].strip()
                    print("Structure_map_name:", Structure_map_name)
                    value["Structure_map_name"]=Structure_map_name
                    Structure_map_title = Structure_map_title[0].strip()
                    print("Structure_map_title:", Structure_map_title)
                    value["Structure_map_title"]=Structure_map_title

                    url2 = Structure_map_href
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
                    time.sleep(20)
                    # proxie = {"http": host_list[count_host]}
                    # if count_host > host_list_len - 1:
                    #     count_host = 0
                    # else:
                    #     count_host = count_host + 1
                    data2 = requests.get(url2, headers=headers).text
                    s2 = etree.HTML(data2)
                    img_Structure_path = s2.xpath('/html/body/img/@src')
                    if img_Structure_path == None or img_Structure_path == []:
                        img_Structure_path = "None"

                    else:
                        img_Structure_path = img_Structure_path[0].strip()
                        img_Structure_path = get_url(url2, img_Structure_path)
                        print("img_Structure_path:", img_Structure_path)
                        value["img_Structure_path"]=img_Structure_path
                        try:
                            f = open(".." + os.sep + "pic_kegg_structure_map" + os.sep + kegg_id + ".png",
                                     'wb')
                            time.sleep(20)
                            # proxie = {"http": host_list[count_host]}
                            # if count_host > host_list_len - 1:
                            #     count_host = 0
                            # else:
                            #     count_host = count_host + 1
                            f.write((urllib.request.urlopen(img_Structure_path)).read())
                            f.close()
                            value["pic_kegg_structure_map"]=kegg_id + ".png"
                        except Exception as e:
                            print("file write Exception:", e)
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='paindatabase', charset='utf8')
    cursor1=conn.cursor()
    sql = "REPLACE INTO kegg_drug VALUES (%(kegg_id)s,%(kegg_url)s,%(Formula)s,%(imgPath)s,%(pic_kegg_structure)s,%(Target_href)s,%(Target_id)s,%(Pathway_href)s,%(Pathway_name)s,%(img_pathway_path)s,%(pic_kegg_pathway)s,%(Structure_map_href)s,%(Structure_map_name)s,%(Structure_map_title)s,%(img_Structure_path)s,%(pic_kegg_structure_map)s)"
    # value={
    # "kegg_id":kegg_id,
    # "Formula":Formula,
    # "imgPath":imgPath,
    # "pic_kegg_structure":kegg_id + ".gif",
    # "Target_href":Target_href,
    # "Target_id":Target_id,
    # "Pathway_href":Pathway_href,
    # "Pathway_name":Pathway_name,
    # "img_pathway_path":img_pathway_path,
    # "pic_kegg_pathway":kegg_id + ".png",
    # "Structure_map_href":Structure_map_href,
    # "Structure_map_name":Structure_map_name,
    # "Structure_map_title":Structure_map_title,
    # "img_Structure_path":img_Structure_path,
    # "pic_kegg_structure_map":kegg_id + ".png"
    # }
    try:
        cursor1.execute(sql,value)
        cursor1.close()
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:conn.close()


def get_host_list():
    f_host = open(".." + os.sep + "craw_KEGG" + os.sep + "proxy.txt", "r")
    host_list = []
    for line in f_host.readlines():
        # print(line.strip())
        host_list.append(line.strip())
    return host_list
def kegg_drug_link_exist_list():
    f_host = open(".." + os.sep + "creawl_drugbank" + os.sep + "KEGG_Drug_link_exist.txt", "r")
    host_list = []
    for line in f_host.readlines():
        # print(line.strip())
        host_list.append(line.strip())
    return host_list
def write_kegg_drug_link_exist(url):
    f = open(".." + os.sep + "creawl_drugbank" + os.sep + "KEGG_Drug_link_exist.txt", "a")
    f.writelines(url+"\n")
    f.close()

if __name__ =="__main__":

    f_KEGG_Drug_link = open(".." + os.sep + "creawl_drugbank"+os.sep+"KEGG_Drug_link.txt","r")
    #host_list=get_host_list()
    exist_list=kegg_drug_link_exist_list()
    for line in f_KEGG_Drug_link.readlines():
        url=line.split(" ")[1]
        if url in exist_list:
            continue
        else:
            print("@@@@@@@@@@@@")
            print(url)
            crawKeggToDatabase(url)
            write_kegg_drug_link_exist(url)
        # print("@@@@@@@@@@@@")
        # print(url)
        # crawKeggToDatabase(url)










