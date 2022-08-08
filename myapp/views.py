from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextId = 4
topics = [
    {'id':1, 'title':'Software', 'body':'소프트웨어(software)는 프로그램과 프로그램의 수행에 필요한 절차, 규칙, 관련 문서 등을 총칭합니다. <br> <blockquote>프로그램: 일련의 작업을 처리하기 위한 명령어, 관련된 데이터의 집합.<br> 자료구조: 자료의 표현, 처리, 저장방법 등을 총칭. 데이터 간의 논리적 관계, 처리 알고리즘 등</blockquote>'},
    {'id':2, 'title':'System', 'body':'View is..'},
    {'id':3, 'title':'SDM; Software Development Methodology', 'body':'Model is..'},
]

def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href=/read/{topic["id"]}>{topic["title"]}</a></li>'
    
    return(f'''
    <html>
    <body>
        <h1><a href="/">MAACKIA'S STUDY NOTE</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <li><a href="/create/">Create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
    ''')

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(
        HTMLTemplate(article)
    )

@csrf_exempt
def create(request):
    global nextId
    print('request.method', request.method)
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        url = '/read/' + str(nextId)
        nextId += 1
        topics.append(newTopic)
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        id = request.POST['id']
        print(id)
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))
