
#make server-start : 서버 구동 및 자동 세팅완료
server-start:
	docker-compose up
	python3 wordpress_start/register_action.py

#make server-stop : 서버 종료 (주의 : 서버에 있던 플러그인 초기화 됨)
server-stop:
	docker-compose down

#make register : 만일의 상황을 가정하여 자동 가입만 시행하는 명령어
register:
	python3 wordpress_start/register_action.py