from sqlalchemy import create_engine

def get_pool(host:str,db:str,user:str,passwd:str):

    engine = create_engine('mysql+mysqldb://'+user+':'+passwd+'@'+host+'/'+db,echo=True)
    return engine


def excuate_sql(db,sql):
    print(sql.encode('utf-8'))
    cur=db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print("rollback:"+e)
        db.rollback()
        return
    return cur.fetchall()
