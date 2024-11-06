# 사이트 최초 구축시 홈페이지 세팅 정보 전달
import requests

s = requests.Session()

try:
    response = s.get('http://127.0.0.1:4321/wordpress/wp-admin/')  # 여기에 요청할 URL을 입력합니다
except requests.exceptions.TooManyRedirects:
    response = s.get('http://127.0.0.1:4321/wp-admin/install.php')
    response = s.post('http://127.0.0.1:4321/wp-admin/install.php?step=1',data={'language' : 'ko_KR'})
    response = s.post('http://127.0.0.1:4321/wp-admin/install.php?step=2',data={'weblog_title' : 'test', 'user_name' : 'root', 'admin_password' : 'root','admin_password2' : 'root','pw_weak' : 'on','admin_email' : 'cora9448@naver.com','blog_public' : 0,'Submit' : '워드프레스 설치','language' : 'ko_KR'})
response = s.post('http://127.0.0.1:4321/wp-login.php/',data={'log' : 'root', 'pwd' : 'root', 'wp-submit' : '로그인', 'redirect_to' : 'http://127.0.0.1:4321/wp-admin/', 'testcookie' : 1})
response = s.get('http://127.0.0.1:4321/wp-admin/')
response = s.post('http://127.0.0.1:4321/wp-login.php', data={'log' : 'root', 'pwd' : 'root', 'wp-login':'로그인','redirect_to':'http://127.0.0.1:4321/wp-admin/','testcookie':1})
print(response.text)