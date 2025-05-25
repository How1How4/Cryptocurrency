import data_gethistory as dg
import db_build as db
import db_table_build as dtb

db.dbuild()
dtb.dtbuild()
dg.add_history_price(30)



