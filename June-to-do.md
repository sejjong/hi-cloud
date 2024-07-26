# June to-do

1. docker 설치
   ```bash
   sudo dnf -y update
   sudo dnf -y install docker
   ```
2. docker 실행
   ```bash
   sudo systemctl start docker
   udo chmod 666 /var/run/docker.sock
   ```
3. container 3개 실행
```bash
bash 로 실행
sudo docker run -d --name nginx-container nginx
sudo docker run -d --name busybox-container busybox sh -c "while true; do echo Hello from Busybox; sleep 3600; done"
sudo docker run -d --name alpine-container alpine sleep 1000
또는 python 코드 안에서 실행
client.containers.run("nginx", name="nginx-container", detach=True)
client.containers.run("busybox", "sh -c 'while true; do echo Hello from Busybox; sleep 3600; done'", name="busybox-container", detach=True)
client.containers.run("alpine", "sleep 1000", name="alpine-container", detach=True)
```
4. python 코드
``` python
# Docker 클라이언트 생성
client = docker.from_env()

# 실행 중인 모든 컨테이너 목록 가져오기
containers = client.containers.list(all=True)

print("Docker Containers:")
for container in containers:
    print(f"ID: {container.id}, Name: {container.name}, Status: {container.status}")

    # 컨테이너의 실시간 통계 정보 가져오기
    stats = container.stats(stream=False)

    print("Stats:")
    print(f"CPU Usage: {stats['cpu_stats']['cpu_usage']['total_usage']}")
    print(f"Memory Usage: {stats['memory_stats']['usage']}")
    print(f"Network IO: {stats['networks']['eth0']['rx_bytes']} RX, {stats['networks']['eth0']['tx_bytes']} TX")
    print("="*40)

# Docker 클라이언트 종료
client.close()
```
6. python 코드 결과
   ![image](https://github.com/user-attachments/assets/736045d7-720e-422b-a0fe-d1ab4c593570)

7. sudo docker ps -a 결과
![image](https://github.com/user-attachments/assets/22d8fb6e-63ae-45ac-b299-bb1edd33e2dd)
