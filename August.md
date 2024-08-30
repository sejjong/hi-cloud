## application 데이터 통신
### a. 서버 REST API url :
### b. REST API METHOD : POST
### ss-server
```bash
[2024-08-30 21:59:46,616][PID:153135(139748416661056)][INFO] [post_monitor_info] called api. item:engine_type='docker' agent_id='agent_ss' ser_cpu_count=1 ser_cpu_percent=0.0 ser_memory_total=1956 ser_memory_used=569 ser_memory_percent=29.09 ser_get_datetime='2024-08-30 12:59:41' container_stats=[ContainerStats(engine_type='docker', agent_id='agent_ss', node_name='ss-agent', container_name='redis-container', status='running', con_cpu_percent=0.0, con_memory_usage=3.4, con_memory_percent=0.17, con_get_datetime='2024-08-30 12:59:41'), ContainerStats(engine_type='docker', agent_id='agent_ss', node_name='ss-agent', container_name='alpine-container', status='exited', con_cpu_percent=0.0, con_memory_usage=0.0, con_memory_percent=0.0, con_get_datetime='2024-08-30 12:59:41'), ContainerStats(engine_type='docker', agent_id='agent_ss', node_name='ss-agent', container_name='busybox-container', status='running', con_cpu_percent=0.0, con_memory_usage=0.43, con_memory_percent=0.02, con_get_datetime='2024-08-30 12:59:41'), ContainerStats(engine_type='docker', agent_id='agent_ss', node_name='ss-agent', container_name='nginx-container', status='running', con_cpu_percent=0.0, con_memory_usage=2.44, con_memory_percent=0.12, con_get_datetime='2024-08-30 12:59:41')]
[2024-08-30 21:59:46,625][PID:153135(139748416661056)][INFO] [db_connect] MySQL connected. config:(ss-db.c3m8aeg2u6ny.ap-northeast-2.rds.amazonaws.com)
[2024-08-30 21:59:46,626][PID:153135(139748416661056)][INFO] [db_insert] DB insert start. table(server) columns(8) rows(1)
[2024-08-30 21:59:46,626][PID:153135(139748416661056)][INFO] [db_insert] SQL:INSERT INTO server(engine_type,agent_id,ser_cpu_count,ser_cpu_percent,ser_memory_total,ser_memory_used,ser_memory_percent,ser_get_datetime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
[2024-08-30 21:59:46,628][PID:153135(139748416661056)][INFO] [db_insert] DB insert success. table(server)
[2024-08-30 21:59:46,629][PID:153135(139748416661056)][INFO] [db_insert] DB insert start. table(container) columns(9) rows(4)
[2024-08-30 21:59:46,629][PID:153135(139748416661056)][INFO] [db_insert] SQL:INSERT INTO container(engine_type,agent_id,node_name,container_name,status,con_cpu_percent,con_memory_usage,con_memory_percent,con_get_datetime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
[2024-08-30 21:59:46,630][PID:153135(139748416661056)][INFO] [db_insert] DB insert success. table(container)
[2024-08-30 21:59:46,634][PID:153135(139748416661056)][INFO] [db_close] MySQL disconnected.
```
### ss-agent
```bash
(ss) [root@ip-172-31-8-86 ~]# python3.12 main.py 
{'engine_type': 'docker', 'agent_id': 'agent_ss', 'ser_cpu_count': 1, 'ser_cpu_percent': 0.0, 'ser_memory_total': 1956.0, 'ser_memory_used': 569.0, 'ser_memory_percent': 29.09, 'ser_get_datetime': '2024-08-30 12:59:41'}
{'engine_type': 'docker', 'agent_id': 'agent_ss', 'node_name': 'ss-agent', 'container_name': 'redis-container', 'status': 'running', 'con_get_datetime': '2024-08-30 12:59:41', 'con_cpu_percent': 0.0, 'con_memory_usage': 3.4, 'con_memory_percent': 0.17}
{'engine_type': 'docker', 'agent_id': 'agent_ss', 'node_name': 'ss-agent', 'container_name': 'alpine-container', 'status': 'exited', 'con_get_datetime': '2024-08-30 12:59:41', 'con_cpu_percent': 0, 'con_memory_usage': 0, 'con_memory_percent': 0}
{'engine_type': 'docker', 'agent_id': 'agent_ss', 'node_name': 'ss-agent', 'container_name': 'busybox-container', 'status': 'running', 'con_get_datetime': '2024-08-30 12:59:41', 'con_cpu_percent': 0.0, 'con_memory_usage': 0.43, 'con_memory_percent': 0.02}
{'engine_type': 'docker', 'agent_id': 'agent_ss', 'node_name': 'ss-agent', 'container_name': 'nginx-container', 'status': 'running', 'con_get_datetime': '2024-08-30 12:59:41', 'con_cpu_percent': 0.0, 'con_memory_usage': 2.44, 'con_memory_percent': 0.12}
{
	"engine_type": "docker",
	"agent_id": "agent_ss",
	"ser_cpu_count": 1,
	"ser_cpu_percent": 0.0,
	"ser_memory_total": 1956.0,
	"ser_memory_used": 569.0,
	"ser_memory_percent": 29.09,
	"ser_get_datetime": "2024-08-30 12:59:41",
	"container_stats": [
		{
			"engine_type": "docker",
			"agent_id": "agent_ss",
			"node_name": "ss-agent",
			"container_name": "redis-container",
			"status": "running",
			"con_get_datetime": "2024-08-30 12:59:41",
			"con_cpu_percent": 0.0,
			"con_memory_usage": 3.4,
			"con_memory_percent": 0.17
		},
		{
			"engine_type": "docker",
			"agent_id": "agent_ss",
			"node_name": "ss-agent",
			"container_name": "alpine-container",
			"status": "exited",
			"con_get_datetime": "2024-08-30 12:59:41",
			"con_cpu_percent": 0,
			"con_memory_usage": 0,
			"con_memory_percent": 0
		},
		{
			"engine_type": "docker",
			"agent_id": "agent_ss",
			"node_name": "ss-agent",
			"container_name": "busybox-container",
			"status": "running",
			"con_get_datetime": "2024-08-30 12:59:41",
			"con_cpu_percent": 0.0,
			"con_memory_usage": 0.43,
			"con_memory_percent": 0.02
		},
		{
			"engine_type": "docker",
			"agent_id": "agent_ss",
			"node_name": "ss-agent",
			"container_name": "nginx-container",
			"status": "running",
			"con_get_datetime": "2024-08-30 12:59:41",
			"con_cpu_percent": 0.0,
			"con_memory_usage": 2.44,
			"con_memory_percent": 0.12
		}
	]
}
200
{
  "data": "",
  "pageInfo": {},
  "resultCode": "0",
  "resultMessage": "",
  "success": true
}
```

### table container
![image](https://github.com/user-attachments/assets/d62759db-9f72-41ae-8cb7-fdb23b428dd3)

### table server
![image](https://github.com/user-attachments/assets/8b056123-fb81-4418-be4c-93b1f5177b98)
