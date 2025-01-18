# airflow docker hub
- https://hub.docker.com/r/apache/airflow

# airflow 공식 문서
- docker 세팅 : https://airflow.apache.org/docs/docker-stack/build.html
- docker-compose 세팅 : https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

# Docker 실행

1. 설정 파일로 이동
```shell
cd /docker/airflow
```

2. docker-compose 실행
```shell
docker-compose up
# 백그라운드 실행
docker-compose up -d
```

# 로컬에서 airflow 세팅

1. 데이터베이스 초기화
```shell
docker-compose up airflow-init
```
> 생성된 계정에는 로그인 airflow과 비밀번호가 있습니다 airflow.

2. 웹 서버 시작
```shell
docker-compose up
```

### 실행 후 로그 예시
```shell
ed9b09fc84b1   apache/airflow:2.10.4   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-scheduler_1
7cb1fb603a98   apache/airflow:2.10.4   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    0.0.0.0:8080->8080/tcp             compose_airflow-webserver_1
74f3bbe506eb   postgres:13             "docker-entrypoint.s…"   18 minutes ago   Up 17 minutes (healthy)   5432/tcp                           compose_postgres_1
```
