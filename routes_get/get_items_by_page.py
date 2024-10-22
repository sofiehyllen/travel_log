from flask import Blueprint, render_template
import json
import x
import random 

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)

get_items_by_page = Blueprint("get_items_by_page", __name__)

##############################
@get_items_by_page.get("/items/page/<page_number>")
def function_name(page_number):
    try:
        
        # VALIDATION

        # db, cursor = x.db()
        # q = "QUERY_XXXXX WITH %s"
        # cursor.execute(q, (TUPLE_VARIABLES))
        # db.commit()
        markers = []
        for i in range(10):
            random_lat = random.uniform(54, 56)
            random_lat_rounded = round(random_lat, 2)
            random_lon = random.uniform(11, 13)
            random_lon_rounded = round(random_lon, 2)            
            # marker = {"coords": [{random_lat_rounded}, {random_lon_rounded}], "popup": "Marker 10: New Place" }
            marker = {
                "coords": [random_lat_rounded, random_lon_rounded],
                "popup": "Marker 10: New Place"
            }
            # ic(marker)
            markers.append(marker)
        return f"""<template mix-function="render_items">{json.dumps(markers)}</template>"""
    
    except Exception as ex:

        ic(ex)
        if "db" in locals(): db.rollback()

        # My own exception
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target=\"#toast\" mix-bottom>{ex.message}</template>""", ex.code
        
        # Database exception
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex):
                return """<template mix-target=\"#toast\" mix-bottom>email not available</template>""", 400
            return "<template>System upgrading</template>", 500  
      
        # Any other exception
        return """<template mix-target=\"#toast\" mix-bottom>System under maintenance</template>""", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
