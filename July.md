## ss-agent
### agent 동작방식

```python
import docker
from time import strftime, localtime
import json, time
import psutil
import requests
from collections import OrderedDict

engine_type = "docker"
agent_id = "agent_ss"
def get_server_stats(tm):
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    memory_total = round(mem_info.total/1024/1024, 0)
    avaliable_memory = round(mem_info.available/1024/1024, 0)
    memory_used = memory_total - avaliable_memory
    memory_percent = round(memory_used/memory_total*100,2)

    _dict = {}
    _dict['engine_type'] = engine_type
    _dict['agent_id'] = agent_id
    _dict['ser_cpu_count'] = cpu_count
    _dict['ser_cpu_percent'] = cpu_percent
    _dict['ser_memory_total'] = memory_total
    _dict['ser_memory_used'] = memory_used
    _dict['ser_memory_percent'] = memory_percent
    _dict['ser_get_datetime'] = dt
    print(_dict)
    return _dict


def get_container_stats(tm):
    client = docker.from_env()
    _list = []
    for container in client.containers.list(all=True):

        _dict = {}
        _dict['engine_type'] = "docker"
        _dict['agent_id'] = "agent_ss"
        _dict['node_name'] = "ss-agent"
        _dict['container_name'] = container.name
        _dict['status'] = container.status
        _dict['con_get_datetime'] = dt


        if container.status == "running":
            stats = container.stats(stream=False)
            total_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            prev_total_usage = stats['precpu_stats']['cpu_usage']['total_usage']
            system_cpu_usage = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            cpu_usage = total_usage - prev_total_usage
            cpu_percentage = cpu_usage / system_cpu_usage

            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percentage = (memory_usage / memory_limit) * 100

            _dict['con_cpu_percent'] = round(cpu_percentage, 2)
            _dict['con_memory_usage'] = round(memory_usage/1024/1024, 2)
            _dict['con_memory_percent'] = round(memory_percentage, 2)

        else:
            _dict['con_cpu_percent'] = 0
            _dict['con_memory_usage'] = 0
            _dict['con_memory_percent'] = 0
        print(_dict)
        _list.append(_dict)

    return _list

if __name__ == '__main__':

    now = time.time()
    tm = localtime(now)
    dt = strftime('%Y-%m-%d %I:%M:%S', tm)

    server_stats = get_server_stats(dt)
    container_stats = get_container_stats(dt)

    body = OrderedDict()
    body = server_stats
    body['container_stats'] = container_stats
    data = json.dumps(body, ensure_ascii=False, indent="\t")
    print(data)

    url = "http://13.209.193.135:8000/monitor_info"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    print(response.text)
```


## ss-server 
### server 동작방식 - flask

```python
from flask import Flask, request, jsonify
import os
import sys
import datetime
import pandas as pd
from typing import List, Union
from pydantic import BaseModel
from common import ConfigManager, MySQLWrapper, CommonUtil

app = Flask(__name__)

config_manager = None
logger = None
commonUtil = CommonUtil.CommonUtil()

class ContainerStats(BaseModel):
    engine_type: str
    agent_id: str
    node_name: str
    container_name: str
    status: str
    con_cpu_percent: float
    con_memory_usage: float
    con_memory_percent: float
    con_get_datetime: str

class MonitorInfo(BaseModel):
    engine_type: str
    agent_id: str
    ser_cpu_count: int
    ser_cpu_percent: float
    ser_memory_total: int
    ser_memory_used: int
    ser_memory_percent: float
    ser_get_datetime: str
    container_stats: Union[List[ContainerStats], None] = None

def setup():
    global config_manager
    global logger

    config_manager = ConfigManager.ConfigManager()
    config_file = os.getenv('SERVER_CONFIG', './config/config.xml')
    config_manager.load_config(config_file)
    logger = config_manager.get_logger()

@app.route('/monitor_info', methods=['POST'])
def post_monitor_info():
    try:
        myfunc = sys._getframe().f_code.co_name
        if not config_manager or not logger:
            setup()  # Ensure setup is called

        data = request.get_json()
        monitorInfo = MonitorInfo(**data)

        logger.info(f"[{myfunc}] called api. item:{monitorInfo}")

        _dict = {
            'engine_type': monitorInfo.engine_type,
            'agent_id': monitorInfo.agent_id,
            'ser_cpu_count': monitorInfo.ser_cpu_count,
            'ser_cpu_percent': monitorInfo.ser_cpu_percent,
            'ser_memory_total': monitorInfo.ser_memory_total,
            'ser_memory_used': monitorInfo.ser_memory_used,
            'ser_memory_percent': monitorInfo.ser_memory_percent,
            'ser_get_datetime': monitorInfo.ser_get_datetime,
        }

        _list = []
        if monitorInfo.container_stats:
            for container in monitorInfo.container_stats:
                con_dict = {
                    'engine_type': str(container.engine_type),
                    'agent_id': str(container.agent_id),
                    'node_name': str(container.node_name),
                    'container_name': str(container.container_name),
                    'status': str(container.status),
                    'con_cpu_percent': container.con_cpu_percent,
                    'con_memory_usage': container.con_memory_usage,
                    'con_memory_percent': container.con_memory_percent,
                    'con_get_datetime': str(container.con_get_datetime),
                }
                _list.append(con_dict)

        mysql_wrapper = MySQLWrapper.MySQLWrapper()
        mysql_wrapper.set_logger(config_manager.get_logger())
        mysql_wrapper.db_connect(config_manager.get_db_connection_info())

        df = pd.json_normalize(_dict)
        mysql_wrapper.db_insert(df, 'server', "insertonly")

        df = pd.json_normalize(_list)
        mysql_wrapper.db_insert(df, 'container', "insertonly")

        mysql_wrapper.db_commit()
        mysql_wrapper.db_close()

        json_data = commonUtil.make_json_result(True, "0", "", "")
        return jsonify(json_data)

    except Exception as err:
        json_data = commonUtil.make_json_result(False, "99", f"{str(err)}", None)
        logger.error(f"[{myfunc}] Exception err:{str(err)}, data:{data}")
        mysql_wrapper.db_close()
        return jsonify(json_data)

if __name__ == '__main__':
    os.environ.setdefault('SERVER_HOME', '/')

    try:
        setup()  # Ensure setup is called before running the app
        
        server_home = os.getenv('SERVER_HOME')
        now = datetime.datetime.now()
        if server_home is None:
            print(f"{now} ENV SERVER_HOME not found")
            raise Exception

        config_file = os.getenv('SERVER_CONFIG', './config/config.xml')
        config_manager = ConfigManager.ConfigManager()
        config_manager.load_config(config_file)
        config_server = config_manager.get_server_info()

        app.run(host=config_server.ip, port=config_server.port, debug=True)

    except Exception as err:
        now = datetime.datetime.now()
        print(f"{now} process terminated with exception")
        raise SystemExit(-1)
```


