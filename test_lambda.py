import json
import boto3
import os
import logging
import datetime

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel("INFO")

states = {'OK':0,'ALARM':1,'INSUFFICIENT_DATA':2}

def lambda_handler(event, context):
    # count = 0
    alarm_list = []
    conn = boto3.client('cloudwatch')
    if conn.can_paginate("describe_alarms"):
        paginator = conn.get_paginator('describe_alarms')
        for response in paginator.paginate():
            for alarm_response in response['MetricAlarms']:
                alarm_name = alarm_response['AlarmName']
                alarm_value = alarm_response['StateValue']
                state_value_digit = states.get(alarm_value)
                alarm_last_updated_obj = alarm_response['AlarmConfigurationUpdatedTimestamp']
                last_updated = alarm_updated_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
                alarm_list.append({alarm_name:(alarm_state_value,last_updated)})
                # count += 1
                conn.put_metric_data(
                    MetricData = [
                        {
                            'MetricName':'AlarmState',
                            'Dimensions':[
                                {
                                    'Name':'By Alarm Name',
                                    'Value':alarm_name
                                },    
                            ],
                            'Timestamp':datetime.datetime.now(),
                            'Unit':'Count',
                            'Value':state_value_digit
                        },    
                    ],
                    Namespace='CloudWatchAlarmsNew'
                )

        # _LOGGER.info({'alarms_count':count})
        for data in alarm_list:
            _LOGGER.info('Alarm_Data:%s',data)
