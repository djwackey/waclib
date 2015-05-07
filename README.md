## waclib ##
it's a python library include mysql, memcache, django reload modules etc.
## Demo ##
### Example 1 ###
<pre>
from waclib import math

print math.add(1, 2)
print math.sub(5, 9)
</pre>
### Example 2 ###
<pre>
from waclib.core import app

app.init(storage_cfg_file="storage.json", 
           model_cfg_file="model.json")

engine = app.get_engine("mysql")

sql = "select * from user"
try:
    rows = engine.master_query(sql)
    for row in rows:
	print row
except Exception, e
    print e
</pre>
### Example 3 ###
<pre>
from waclib.core import app
from waclib.client import mysql

engine = app.get_engine("mysql")

sql = "insert into user values('1', 'wackey', 'worcy_kiddy@126.com')"
try:
    engine.master_execute(sql)
except Exception, e
    print e
</pre>
### Example 4 ###
<pre>
"""
for django
"""
from waclib.core import app
from waclib.server.preforkserver import checker

PlatMainKey = "PLAT_MAIN_KEY_20150506"

def reload_all():
    pass

memcache = app.get_engine("memcache")
app.replace_class("flup.server.preforkserver.PreforkServer", "waclib.server.preforkserver.PreforkServer")

checker.setup(memcache.servers, PlatMainKey, reload_all)
</pre>
