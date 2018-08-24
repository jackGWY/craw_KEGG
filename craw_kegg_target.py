import os
from lxml import etree
import requests
import urllib
import time
import pymysql

def getExistUrl():
    f_getExistUrl=open('Target_url_exist.txt',"r")
    target_url_list=[]
    for line in f_getExistUrl.readlines():
        if line =='\n':
            continue
        line=line.strip()
        target_url_list.append(line)
    return target_url_list

def getPathwayLinkExist():
    f_getPathwayLinkExist=open("pathway_link_exist.txt","r")
    pathway_link_list=[]
    for line in f_getPathwayLinkExist.readlines():
        if line == '\n':
            continue
        line=line.strip()
        pathway_link_list.append(line)
    return pathway_link_list

def get_kegg_target_hsa_link_list():
    f_getPathwayLinkExist=open("kegg_target_hsa_link_exist.txt","r")
    kegg_target_hsa_link_exist_list=[]
    for line in f_getPathwayLinkExist.readlines():
        if line == '\n':
            continue
        line=line.strip()
        kegg_target_hsa_link_exist_list.append(line)
    return kegg_target_hsa_link_exist_list


def crawKeggTarget(url):
    url_list=getExistUrl()
    print("url_list:",url_list)
    # if url in url_list:
    #     return ""
    time.sleep(20)
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='paindatabase', charset='utf8')
    target_dict={
        "Target_href":url,
        "target_name":"None",
        "has_disease":"None",
        "has_pathway":"None",
        "target_id":"None",
        "Gene_name":"None",
        "Definition":"None",
        "aa_seq":"None",
        "nt_seq":"None"
    }
    #headers = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    data = requests.get(url, headers=headers).text

    s = etree.HTML(data)
    target_name=s.xpath('/html/body/div/table/tr/td/table[1]/tr/td[3]/font/text()')
    if target_name==[]:
        pass
    else:
        target_name=target_name[0].strip()
        print("target_name:",target_name)
        target_dict["target_name"]=target_name
    for i in range(1,25):
        item=s.xpath("/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr["+str(i)+"]/th/nobr/text()")
        if item==[]:
            continue
        else:
            item_name=item[0].strip()
            #print("item_name:",item_name)
            if item_name=="Entry":
                target_id = s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr['+str(i)+
                                    ']/td/table/tr/td[1]/code/nobr/text()')
                if target_id==[]:
                    target_id="None"
                else:
                    target_id=target_id[0].strip()
                print("target_id:",target_id)
                target_dict["target_id"]=target_id
                target_dict["target_id"] = target_id
            if item_name=="Gene name":
                Gene_name=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/text()')
                if Gene_name==[]:
                    Gene_name="None"
                else:
                    Gene_name=Gene_name[0].strip()
                print("Gene_name:",Gene_name)
                target_dict["Gene_name"]=Gene_name

            if item_name=="Definition":
                Definition=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/div/text()')
                if Definition==[]:
                    Definition="None"
                else:
                    Definition=Definition[0].strip()
                print("Definition:",Definition)
                target_dict["Definition"]=Definition

            if item_name=="Definition":
                Definition=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr['+str(i)+']/td/div/div/text()')
                if Definition==[]:
                    Definition="None"
                else:
                    Definition=Definition[0].strip()
                print("Definition:",Definition)
                target_dict["Definition"]=Definition

            if item_name=="Pathway":
                target_dict["has_pathway"]="true"
                for j in range(1,20):
                    pathway_dict={
                        "Target_href":url,
                        "kegg_target_hsa":"None",
                        "kegg_target_hsa_link":"None",
                        "kegg_target_pathway_name":"None",
                        "pic_kegg_targets_pathway":"None"
                    }
                    kegg_target_pathway_name = s.xpath(
                        '/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                        '/tr[' + str(i) + ']/td/table[' + str(j) + ']/tr/td[2]/text()')
                    if kegg_target_pathway_name == []:
                        continue
                    else:
                        kegg_target_pathway_name = kegg_target_pathway_name[0].strip()
                        print("kegg_target_pathway_name:", kegg_target_pathway_name)
                        pathway_dict["kegg_target_pathway_name"] = kegg_target_pathway_name

                    kegg_target_hsa=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                            '/tr['+str(i)+']/td/table['+str(j)+']/tr/td[1]/nobr/a/text()')
                    if kegg_target_hsa==[]:
                        continue
                    else:
                        kegg_target_hsa=kegg_target_hsa[0].strip()
                        print("kegg_target_hsa:",kegg_target_hsa)
                        pathway_dict["kegg_target_hsa"]=kegg_target_hsa

                    kegg_target_hsa_link=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                            '/tr['+str(i)+']/td/table['+str(j)+']/tr/td[1]/nobr/a/@href')
                    if kegg_target_hsa_link==[]:
                        continue
                    else:
                        kegg_target_hsa_link='https://www.genome.jp'+kegg_target_hsa_link[0].strip()
                        print("kegg_target_hsa_link:",kegg_target_hsa_link)
                        pathway_dict["kegg_target_hsa_link"]=kegg_target_hsa_link
                        #爬取pathway图片
                        headers = {
                            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
                        # pathway_link_exist=getPathwayLinkExist()
                        # print("pathway_link_exist:",pathway_link_exist)
                        # #if kegg_target_hsa_link not in pathway_link_exist:
                        kegg_target_hsa_link_exist_list=get_kegg_target_hsa_link_list()
                        print("kegg_target_hsa_link_exist_list:",kegg_target_hsa_link_exist_list)
                        if kegg_target_hsa_link not in kegg_target_hsa_link_exist_list:
                            data2 = requests.get(kegg_target_hsa_link, headers=headers).text
                            s2 = etree.HTML(data2)
                            img_pathway_link = s2.xpath('/html/body/img/@src')
                            if img_pathway_link == []:
                                continue
                            img_pathway_link = 'https://www.genome.jp' + img_pathway_link[0].strip()
                            print("img_pathway_link:", img_pathway_link)
                            pathway_link_exist_list = getPathwayLinkExist()
                            print("pathway_link_exist_list:",pathway_link_exist_list)
                            if img_pathway_link not in pathway_link_exist_list:
                                try:
                                    time.sleep(20)
                                    f = open(
                                        ".." + os.sep + "pic_kegg_targets_pathway" + os.sep + kegg_target_hsa + ".png",
                                        'wb')
                                    f.write((urllib.request.urlopen(img_pathway_link)).read())
                                    f.close()
                                    pathway_dict["pic_kegg_targets_pathway"] = kegg_target_hsa + ".png"

                                    f_pathway_link = open("pathway_link_exist.txt", "a")  # img_pathway_link_exist
                                    f_pathway_link.write(img_pathway_link + "\n")
                                    f_pathway_link.close()
                                except Exception as e:
                                    print("？？？？？？？？？？？？？？？？？？？？？")
                                    print("file write Exception:", e)

                            f_kegg_target_hsa_link = open('kegg_target_hsa_link_exist.txt', 'a')
                            f_kegg_target_hsa_link.write(kegg_target_hsa_link + "\n")
                            f_kegg_target_hsa_link.close()

                    path_cursor = conn.cursor()
                    sql_pathway = "REPLACE INTO target_pathway(kegg_target_hsa,kegg_target_hsa_link,kegg_target_pathway_name," \
                                  "pic_kegg_targets_pathway,Target_href) VALUES (%(kegg_target_hsa)s,%(kegg_target_hsa_link)s," \
                                  "%(kegg_target_pathway_name)s,%(pic_kegg_targets_pathway)s,%(Target_href)s)"
                    try:
                        path_cursor.execute(sql_pathway, pathway_dict)
                        conn.commit()
                        path_cursor.close()
                    except Exception as e:
                        print(e)
                        print("??????????????????????????")
                        conn.rollback()


            if item_name=="Disease":
                target_dict["has_disease"]="true"
                for j in range(1,10):
                    disease_dict = {
                        "Target_href": url,
                        "target_disease_id": "None",
                        "target_disease_link": "None",
                        "target_disease_name": "None"
                    }
                    target_disease_id=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                              '/tr['+str(i)+']/td/div/table['+str(j)+']/tr/td[1]/nobr/a/text()')
                    if target_disease_id==[]:
                        continue
                    else:
                        target_disease_id=target_disease_id[0].strip()
                        print("target_disease_id:",target_disease_id)
                        disease_dict["target_disease_id"]=target_disease_id

                    target_disease_link=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                              '/tr['+str(i)+']/td/div/table['+str(j)+']/tr/td[1]/nobr/a/@href')
                    if target_disease_link==[]:
                        continue
                    else:
                        target_disease_link=target_disease_link[0].strip()
                        print("target_disease_link:",target_disease_link)
                        disease_dict["target_disease_link"]=target_disease_link

                    target_disease_name = s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                                  '/tr[' + str(i) + ']/td/div/table[' + str(j) + ']/tr/td[2]/text()')
                    if target_disease_name == []:
                        continue
                    else:
                        target_disease_name = target_disease_name[0].strip()
                        target_disease_name='https://www.genome.jp'+target_disease_name
                        print("target_disease_name:", target_disease_name)
                        disease_dict["target_disease_name"]=target_disease_name
                    f_target_href_disease=open('target_href_disease_link2.txt',"a+")
                    f_target_href_disease.write(url+","+target_disease_id+','+target_disease_link+','+target_disease_name+"\n")
                    f_target_href_disease.close()
                    disease_cursor = conn.cursor()
                    sql_disease="REPLACE INTO target_disease(target_disease_link,target_disease_id,target_disease_name," \
                                "Target_href) VALUES (%(target_disease_link)s,%(target_disease_id)s," \
                                "%(target_disease_name)s,%(Target_href)s)"
                    try:
                        disease_cursor.execute(sql_disease, disease_dict)
                        conn.commit()
                        disease_cursor.close()
                    except Exception as e:
                        print(e)
                        print("??????????????????????????")
                        conn.rollback()


            if item_name=="AA seq":
                AA_seq=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr[16]/td/text()')
                if AA_seq==[]:
                    continue
                else:
                    aa_seq=""
                    for seq in AA_seq:
                        aa_seq=aa_seq+seq
                    print("aa_seq:",aa_seq)

            if item_name=="NT seq":
                NT_seq=s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table/tr[16]/td/text()')
                if NT_seq==[]:
                    continue
                else:
                    nt_seq=""
                    for seq in NT_seq:
                        nt_seq=nt_seq+seq
                    print("nt_seq:",nt_seq)

    target_cursor=conn.cursor()
    sql_target="REPLACE INTO kegg_drug_target(Target_href,target_name,has_disease,has_pathway,target_id,Gene_name," \
               "Definition,aa_seq,nt_seq) VALUES (%(Target_href)s,%(target_name)s,%(has_disease)s,%(has_pathway)s," \
               "%(target_id)s,%(Gene_name)s,%(Definition)s,%(aa_seq)s,%(nt_seq)s)"
    try:
        target_cursor.execute(sql_target,target_dict)
        conn.commit()
        target_cursor.close()
    except Exception as e:
        print(e)
        print("??????????????????????????")
        conn.rollback()

    f_url_exist=open("Target_url_exist.txt","a")
    f_url_exist.write(url+"\n")
    f_url_exist.close()
if __name__ == "__main__":
    f=open('Target_kegg_id.txt',"r")
    for line in f.readlines():
        url=line.split(" ")[1].strip()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("url:",url)
        crawKeggTarget(url)
    # url='https://www.genome.jp/dbget-bin/www_bget?hsa:5743'
    # crawKeggTarget(url)