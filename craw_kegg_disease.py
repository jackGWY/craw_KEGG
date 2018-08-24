import os
from lxml import etree
import requests
import urllib
import time
import pymysql

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36'}
def crawKeggDisease(url):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='paindatabase', charset='utf8')
    data = requests.get(url, headers=headers).text
    s = etree.HTML(data)
    kegg_disease_dict={
        "kegg_disease_link":url,
        "kegg_disease_id": "None",
        "kegg_disease_name": "None",
        "Description": "None",
        "Category": "None",
        "kegg_disease_pathway_id": "None",
        "kegg_disease_pathway_link": "None",
        "img_pathway": "None",
        "kegg_disease_pathway_name": "None"
    }
    for i in range(1,22):
        item=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/th/nobr/text()')
        if item==[]:
            continue
        item=item[0].strip()
        if item=="Entry":
            kegg_disease_id=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/table/tr/td[1]/code/nobr/text()')
            if kegg_disease_id==[]:
                kegg_disease_id="None"
            else:
                kegg_disease_id=kegg_disease_id[0].split()[0].strip()
            print("kegg_disease_id:",kegg_disease_id)
            kegg_disease_dict["kegg_disease_id"]=kegg_disease_id
        if item=="Name":
            kegg_disease_name=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/text()')
            if kegg_disease_name==[]:
                kegg_disease_name="None"
            else:
                kegg_disease_name=kegg_disease_name[0].strip()
            print("kegg_disease_name:",kegg_disease_name)
            kegg_disease_dict["kegg_disease_name"]=kegg_disease_name
        if item=="Description":
            Description=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/text()')
            if Description==[]:
                Description="None"
            else:
                Description=Description[0].strip()
            print("Description:",Description)
            kegg_disease_dict["Description"]=Description
        if item=="Category":
            Category=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/text()')
            if Category==[]:
                Category="None"
            else:
                Category=Category[0].strip()
            print("Category:",Category)
            kegg_disease_dict["Category"]=Category
        if item=="Pathway":
            kegg_disease_pathway_id=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/table/tr/td[1]/nobr/a/text()')
            if kegg_disease_pathway_id==[]:
                kegg_disease_pathway_id="None"
            else:
                kegg_disease_pathway_id=kegg_disease_pathway_id[0].strip()
            print("kegg_disease_pathway_id:",kegg_disease_pathway_id)
            kegg_disease_dict["kegg_disease_pathway_id"]=kegg_disease_pathway_id
            kegg_disease_pathway_link = s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr[' + str(
                i) + ']/td/table/tr/td[1]/nobr/a/@href')
            if kegg_disease_pathway_link == []:
                kegg_disease_pathway_link = "None"
            else:
                kegg_disease_pathway_link = kegg_disease_pathway_link[0].strip()
                kegg_disease_pathway_link='https://www.genome.jp'+kegg_disease_pathway_link
                print("kegg_disease_pathway_link:",kegg_disease_pathway_link)
                kegg_disease_dict["kegg_disease_pathway_link"]=kegg_disease_pathway_link
                time.sleep(10)
                data2 = requests.get(kegg_disease_pathway_link, headers=headers).text
                s2 = etree.HTML(data2)
                img_pathway_link=s2.xpath('/html/body/img/@src')
                if img_pathway_link==[]:
                    img_pathway_link="None"
                    print("None")
                else:
                    img_pathway_link=img_pathway_link[0].strip()
                    img_pathway_link='https://www.genome.jp'+img_pathway_link
                    print('img_pathway_link:',img_pathway_link)
                    try:
                        time.sleep(20)
                        f = open(".." + os.sep + "pic_kegg_disease_pathway" + os.sep + kegg_disease_pathway_id + ".png",
                                 'wb')
                        f.write((urllib.request.urlopen(img_pathway_link)).read())
                        f.close()
                        kegg_disease_dict["img_pathway"]=kegg_disease_pathway_id+".png"
                        # f_pathway_link = open("pathway_link_exist.txt", "a")  # img_pathway_link_exist
                        # f_pathway_link.write(img_pathway_link + "\n")
                        # f_pathway_link.close()
                    except Exception as e:
                        print("？？？？？？？？？？？？？？？？？？？？？")
                        print("file write Exception:", e)
            print("kegg_disease_pathway_link:", kegg_disease_pathway_link)

            kegg_disease_pathway_name = s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table/tr[' + str(
                i) + ']/td/table/tr/td[2]/text()')
            if kegg_disease_pathway_name == []:
                kegg_disease_pathway_name = "None"
            else:
                kegg_disease_pathway_name = kegg_disease_pathway_name[0].strip()
            print("kegg_disease_pathway_name:", kegg_disease_pathway_name)
            kegg_disease_dict["kegg_disease_pathway_name"]=kegg_disease_pathway_name

        if item=="Gene":
            temp_str = ""
            count_hsa=0
            for text_index in range(1,31):
                text=s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table'
                             '/tr['+str(i)+']/td/div/text()['+str(text_index)+']')
                if text==[]:
                    break
                HSA_list = s.xpath('/html/body/div/table/tr/td[1]/form/table/tr/td/table'
                                   '/tr[' + str(i) + ']/td/div/a/text()')
                if HSA_list==[]:
                    break
                text=text[0].strip()
                temp_str=temp_str+text
                if text_index%3==1:
                    if count_hsa>(len(HSA_list)-1):
                        pass
                    else:
                        temp_str = temp_str + HSA_list[count_hsa]
                        count_hsa = count_hsa + 1
                if text_index % 3 == 2:
                    if count_hsa > (len(HSA_list)-1):
                        pass
                    else:
                        temp_str = temp_str + HSA_list[count_hsa]
                        count_hsa = count_hsa + 1
                if text_index%3==0:
                    print("temp_str:",temp_str)
                    gene_dict={
                        "hsa_str":temp_str,
                        "kegg_disease_link":url,
                        "kegg_id":kegg_disease_dict["kegg_disease_id"]
                    }
                    gene_cursor = conn.cursor()
                    sql_gene = "REPLACE INTO kegg_disease_gene(hsa_str,kegg_disease_link,kegg_id) VALUES (%(hsa_str)s,%(kegg_disease_link)s,%(kegg_id)s)"
                    try:
                        gene_cursor.execute(sql_gene, gene_dict)
                        conn.commit()
                        gene_cursor.close()
                    except Exception as e:
                        print(e)
                        print("??????????????????????????")
                        conn.rollback()
                    temp_str=""

    disease_cursor = conn.cursor()
    sql_disease = "replace INTO kegg_disease(kegg_disease_link,kegg_disease_id,kegg_disease_name,Description," \
                  "Category,kegg_disease_pathway_id,kegg_disease_pathway_link,img_pathway,kegg_disease_pathway_name)" \
                  " VALUES (%(kegg_disease_link)s,%(kegg_disease_id)s,%(kegg_disease_name)s,%(Description)s," \
                  "%(Category)s,%(kegg_disease_pathway_id)s,%(kegg_disease_pathway_link)s,%(img_pathway)s," \
                  "%(kegg_disease_pathway_name)s)"
    try:
        disease_cursor.execute(sql_disease, kegg_disease_dict)
        conn.commit()
        disease_cursor.close()
    except Exception as e:
        print(e)
        print("??????????????????????????")
        conn.rollback()

def getDiseaseUrl():
    disease_url_list=[]
    f=open('target_href_disease_link.txt',"r")
    for line in f.readlines():
        if line=='\n':
            continue
        line=line.split(',')
        url=line[2].strip()
        url='https://www.genome.jp'+url
        disease_url_list.append(url)
    return disease_url_list

if __name__ == "__main__":
    disease_url_list=getDiseaseUrl()
    print("disease_url_list:",disease_url_list)
    for url in disease_url_list:
        print("@@@@@@@@@@@@@@@@@@@@")
        print("url:",url)
        crawKeggDisease(url)
