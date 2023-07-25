from s3fs import S3FileSystem
from datetime import datetime
import json


def upload_data_in_s3(**kwarg):
    s3Obj = S3FileSystem(key= 'ACCESS_KEY_GOES_HERE',secret='SECRET_KEY_GOES_HERE')
    data =  kwarg['task_instance'].xcom_pull(task_ids='getting_data_from_api',key='return_value')
    timeStamp = datetime.now()
    for count,jsdt in enumerate(data):
        with s3Obj.open('s3://packt-data-store/data_{}_{}'.format(timeStamp, count),'w') as file:
            json.dump(jsdt, file)




