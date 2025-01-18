# Docker 기본 커맨드

## 1. Docker 버전 확인
Docker 버전 정보를 확인하려면 다음 커맨드를 사용합니다.
```bash
docker --version
```

## 2. Docker 이미지 관리

### 2.1. Docker 이미지 목록 확인
로컬에 저장된 Docker 이미지를 확인하려면:
```bash
docker images
```

### 2.2. Docker 이미지 다운로드
이미지를 Docker Hub에서 다운로드하려면:
```bash
docker pull <이미지명>:<태그>
```
예시:
```bash
docker pull ubuntu:latest
```

### 2.3. Docker 이미지 삭제
로컬에서 Docker 이미지를 삭제하려면:
```bash
docker rmi <이미지명>
```
예시:
```bash
docker rmi ubuntu:latest
```

## 3. Docker 컨테이너 관리

### 3.1. Docker 컨테이너 실행
컨테이너를 실행하려면 다음 명령어를 사용합니다.
```bash
docker run <옵션> <이미지명>
```
예시 (인터랙티브 모드로 Ubuntu 실행):
```bash
docker run -it ubuntu:latest /bin/bash
```

### 3.2. Docker 컨테이너 목록 확인
현재 실행 중인 컨테이너 목록을 확인하려면:
```bash
docker ps
```

### 3.3. Docker 컨테이너 중지
컨테이너를 중지하려면:
```bash
docker stop <컨테이너ID 또는 이름>
```

### 3.4. Docker 컨테이너 삭제
컨테이너를 삭제하려면:
```bash
docker rm <컨테이너ID 또는 이름>
```

## 4. Docker 이미지 및 컨테이너 빌드

### 4.1. Docker 이미지 빌드
`Dockerfile`을 사용하여 이미지를 빌드하려면:
```bash
docker build -t <이미지명>:<태그> <디렉토리경로>
```
예시:
```bash
docker build -t myapp:latest .
```

### 4.2. Docker 컨테이너 실행 중 로그 확인
실행 중인 컨테이너의 로그를 확인하려면:
```bash
docker logs <컨테이너ID 또는 이름>
```

## 5. Docker 네트워크 관리

### 5.1. Docker 네트워크 목록 확인
현재 사용 가능한 네트워크를 확인하려면:
```bash
docker network ls
```

### 5.2. Docker 네트워크 생성
새로운 네트워크를 생성하려면:
```bash
docker network create <네트워크명>
```

### 5.3. Docker 네트워크 삭제
네트워크를 삭제하려면:
```bash
docker network rm <네트워크명>
```

## 6. Docker 볼륨 관리

### 6.1. Docker 볼륨 목록 확인
현재 사용 가능한 볼륨을 확인하려면:
```bash
docker volume ls
```

### 6.2. Docker 볼륨 생성
새로운 볼륨을 생성하려면:
```bash
docker volume create <볼륨명>
```

### 6.3. Docker 볼륨 삭제
볼륨을 삭제하려면:
```bash
docker volume rm <볼륨명>
```


## Docker 리소스 정리 명령어

### 1. 이미지 삭제
특정 이미지를 삭제하려면:
```bash
docker rmi [이미지ID]
```

### 2. 모든 이미지 삭제
모든 이미지를 삭제하려면:
```bash
docker rmi $(docker images -q)
```

### 3. 사용하지 않는 모든 볼륨 제거
컨테이너가 없는 사용하지 않는 모든 볼륨을 제거하려면:
```bash
docker system prune
```

### 4. 사용하지 않는 볼륨 조회
사용하지 않는 볼륨을 조회하려면:
```bash
docker volume ls -qf dangling=true
```

### 5. 사용하지 않는 볼륨 삭제
사용하지 않는 볼륨을 삭제하려면:
```bash
docker volume rm $(docker volume ls -qf dangling=true)
```

### 6. 사용하지 않는 볼륨 조회 및 삭제
사용하지 않는 볼륨을 조회하고 삭제하려면:
```bash
docker volume ls -qf dangling=true | xargs -r docker volume rm
```

### 7. 중지된 모든 컨테이너 삭제
중지된 모든 컨테이너를 삭제하려면:
```bash
docker container prune
```

### 8. 이름 없는 모든 이미지 삭제
이름이 없는 모든 이미지를 삭제하려면:
```bash
docker image prune
```

### 9. 사용하지 않는 Docker 네트워크 삭제
사용하지 않는 Docker 네트워크를 삭제하려면:
```bash
docker network prune
```
