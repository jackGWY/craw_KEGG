import os
from lxml import etree
import requests
import urllib
import time
import pymysql

def crawKeggTarget(url):
    time.sleep(20)
    target_dict={
        "has_disease":"None",
        "has_pathway":"None"
    }
    #headers = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    data = requests.get(url, headers=headers).text
    s = etree.HTML(data)
    target_name=s.xpath('/html/body/div/table/tr/td/table[1]/tr/td[3]/font/text()')
    if target_name==[]:
        target_name="None"
    else:
        target_name=target_name[0].strip()
        print("target_name:",target_name)
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
                        "kegg_target_pathway_name":"None"
                    }
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
                        kegg_target_hsa_link=kegg_target_hsa_link[0].strip()
                        print("kegg_target_hsa_link:",kegg_target_hsa_link)
                        pathway_dict["kegg_target_hsa_link"]=kegg_target_hsa_link

                    kegg_target_pathway_name = s.xpath('/html/body/div/table/tr/td/table[2]/tr/td[1]/form/table/tr/td/table'
                                                   '/tr[' + str(i) + ']/td/table[' + str(j) + ']/tr/td[2]/text()')
                    if kegg_target_pathway_name==[]:
                        continue
                    else:
                        kegg_target_pathway_name=kegg_target_pathway_name[0].strip()
                        print("kegg_target_pathway_name:",kegg_target_pathway_name)
                        pathway_dict["kegg_target_pathway_name"]=kegg_target_pathway_name

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
                        print("target_disease_name:", target_disease_name)
                        disease_dict["target_disease_name"]=target_disease_name

if __name__ == "__main__":
    url='https://www.genome.jp/dbget-bin/www_bget?hsa:5743'
    crawKeggTarget(url)