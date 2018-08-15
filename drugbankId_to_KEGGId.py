import pymysql
import time
f=open('KEGG_Drug_link.txt','r')
conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase', charset='utf8')
for line in f.readlines():
    list2=line.split(' ')
    kegg_id=list2[0]
    KEGG_Drug_link=list2[1]
    drugbank_id= list2[2]
    drugbank_url= list2[3]
    value={}
    value={
        "kegg_id":kegg_id,
        "KEGG_Drug_link":KEGG_Drug_link,
        "drugbank_id": drugbank_id,
        "drugbank_url": drugbank_url
    }
    sql="replace into drugbank_keggDrug(kegg_id,KEGG_Drug_link,drugbank_id,drugbank_url)VALUES " \
        "(%(kegg_id)s,%(KEGG_Drug_link)s,%(drugbank_id)s,%(drugbank_url)s)"
    cur = conn.cursor()
    try:
        cur.execute(sql,value)
        conn.commit()
        cur.close()
    except Exception as e:
        print("???????????????????????????????????????")
        print(e)
        conn.rollback()
        time.sleep(10)

conn.close()
f.close()

