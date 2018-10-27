import requests, pytz
import localization

import utils as f
import db_operations

from datetime import datetime
from picture_maker import DafYomiSender
from io import BytesIO


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_daf(user_id: int, lang: str) -> BytesIO:
    loc = db_operations.get_location_by_id(user_id)
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': f'{now.month}/{now.day}/{now.year}',
        'lat': loc[0],
        'lng': loc[1]
    }
    daf = requests.get(URL, params=params)
    daf_dict = daf.json()
    daf_str = localization.DafYomi.get_str(
        lang,
        daf_dict["dafYomi"]["masechta"],
        daf_dict["dafYomi"]["daf"]
    )
    daf_pic = DafYomiSender(lang).get_daf_picture(daf_str)
    return daf_pic
