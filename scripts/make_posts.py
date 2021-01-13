import os, sqlite3
from os.path import isfile, join
import datetime
md_files = [f for f in os.listdir("markdown_posts") if isfile(join("markdown_posts", f))]

# md_path = "markdown_posts/"
conn = sqlite3.connect('../raider_hacks/site.db')

c = conn.cursor()
for fname in md_files:
    with open("markdown_posts"+"/"+fname) as f:
        print(fname[:-3])
        content = f.readlines()
        str_content = ' '.join([str(elem) for elem in content]) 


        c.execute(
            '''INSERT INTO post(title,content,permissions,user_id) VALUES ({},{},1,1);'''.format(fname[:-3],str_content,1,1)
                            )



c.close()