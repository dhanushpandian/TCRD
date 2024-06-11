import os
import sys
from urllib.request import urlretrieve
import mysql.connector
import tcrd.obo as obo
import chardet  # Ensure chardet is installed: pip install chardet

CONFIG = [{'name': 'Mondo', 'DOWNLOAD_DIR': 'C:/tcrd/', 
            'BASE_URL': 'http://purl.obolibrary.org/obo/', 'FILENAME': 'mondo.obo',
            'parse_function': 'parse_mondo', 'load_function': 'load_mondo'}]

def download(name):
    try:
        cfgd = next(d for d in CONFIG if d['name'] == name)
    except StopIteration:
        print(f"No configuration found for {name}")
        return None

    # Ensure the download directory exists
    os.makedirs(cfgd['DOWNLOAD_DIR'], exist_ok=True)

    fn = os.path.join(cfgd['DOWNLOAD_DIR'], cfgd['FILENAME'])
    
    # Remove the existing file if it exists
    if os.path.exists(fn):
        os.remove(fn)
    
    url = cfgd['BASE_URL'] + cfgd['FILENAME']
    
    print(f"\nDownloading {url}")
    print(f"         to {fn}")
    
    # Download the file
    try:
        urlretrieve(url, fn)
        print("Done.")
        return fn
    except Exception as e:
        print(f"Error downloading the file: {e}")
        return None

def parse_mondo(fn):
    if not fn:
        print("No file to parse")
        return None

    print(f"Parsing Mondo file {fn}")
    parser = obo.Parser(fn)
    raw_mondo = {}
    for stanza in parser:
        if stanza.name != 'Term':
            continue
        raw_mondo[stanza.tags['id'][0].value] = stanza.tags
    mondod = {}
    for mondoid, md in raw_mondo.items():
        if 'is_obsolete' in md:
            continue
        if 'name' not in md:
            continue
        init = {'mondoid': mondoid, 'name': md['name'][0].value}
        if 'def' in md:
            init['def'] = md['def'][0].value
        if 'comment' in md:
            init['comment'] = md['comment'][0].value
        if 'is_a' in md:
            init['parents'] = []
            for parent in md['is_a']:
                # for now, just ignore parent source info, if any.
                cp = parent.value.split(' ')[0]
                init['parents'].append(cp)
        if 'xref' in md:
            init['xrefs'] = []
            for xref in md['xref']:
                if xref.value.startswith('http') or xref.value.startswith('url'):
                    continue
                if len(xref.value.split(' ')) == 1:
                    (db, val) = xref.value.split(':')
                    init['xrefs'].append({'db': db, 'value': val})
                else:
                    (dbval, src) = xref.value.split(' ', 1)
                    (db, val) = dbval.split(':')
                    init['xrefs'].append({'db': db, 'value': val, 'source': src})
        mondod[mondoid] = init
    print("  Got {} Mondo terms".format(len(mondod)))
    return mondod

def store_mondo_data(parsed_data, db_config):
    try:
        # Establishing the connection
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()

        # SQL query to insert data into the mondo table
        insert_query = """
        INSERT INTO mondo (mondoid, name, def, comment)
        VALUES (%s, %s, %s, %s)
        """

        insert_query2="""INSERT INTO mondo_parent(mondoid,parentid) VALUES (%s,%s)"""

        insert_query3="""INSERT INTO mondo_xref(id,mondoid,db,value,equiv_to,source_info,did) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        xref_cnt = 1
        
        for mondoid, data in parsed_data.items():
            mondoid_val = data.get('mondoid', None)
            name_val = data.get('name', None)
            def_val = data.get('def', None)
            comment_val = data.get('comment', None)

            # Inserting data into the table
            cursor.execute(insert_query, (mondoid_val, name_val, def_val, comment_val))

            parents_val=data.get('parents',None)
            
            if parents_val is not None:
                for i in parents_val:
                    cursor.execute(insert_query2,(mondoid_val,i))

            xref_val = data.get('xrefs',None)

            if xref_val is not None:
                for dict1 in xref_val:
                   # "equiv" is in dict['source']? equiv_to=1:equiv_to=0
                    # if "equiv" in str(dict1['source']):
                    #     equiv_to=1
                    # else:
                    
                    #if xref_cnt==1:
                        #print(xref_val)
                        #print(type(xref_val))
                        #print(dict1)
                        #print(type(dict1))
                        #print(dict1['source'])
                        #print(type(dict1['source']))
                        #print(dict1.keys())
                    
                    s1 = 'NULL'  
                    if 'source' in dict1.keys():
                        if "equiv" in dict1['source']:
                            equiv_to=1
                        else:
                            equiv_to=0
                        s1 = dict1['source']
                    # dict['db']
                    # dict['val']
                    # dict['source']
                    cursor.execute(insert_query3,(xref_cnt,mondoid_val, dict1['db'], dict1['value'], equiv_to, s1,'NULL'))
                    xref_cnt+=1

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

    finally:
        # Closing the connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mondo'
}

if __name__ == '__main__':
    fn = download('Mondo')
    if fn:
        parsed_file = parse_mondo(fn)
        if parsed_file:
            print("Success")
            store_mondo_data(parsed_file, db_config)
        else:
            print("Failed to parse the file")
    else:
        print("Failed to download the file")