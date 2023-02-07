
# alembic 초기화

alembic이 잘 설치되었다면 이제 alembic 초기화 작업을 진행해야 한다. 파이참 터미널에서 다음과 같은 명령을 실행하자.

[파이참 터미널]

(myapi) c:/projects/myapi> alembic init migrations
  Creating directory projects/myapi/migrations ...  done
  Creating directory projects/myapi/migrations/versions ...  done
  Generating projects/myapi/migrations/script.py.mako ...  done
  Generating projects/myapi/migrations/env.py ...  done
  Generating projects/myapi/migrations/README ...  done
  Generating projects/myapi/alembic.ini ...  done
  Please edit configuration/connection/logging settings in 'projects/myapi/alembic.ini' before proceeding.
그러면 myapi 디렉터리 하위에 migrations라는 디렉터리와 alembic.ini 파일이 생성된다. migrations 디렉터리는 alembic 도구를 사용할 때 생성되는 리비전 파일들을 저장하는 용도로 사용되고 alembic.ini 파일은 alembic의 환경설정 파일이다.

alembic을 이용하여 테이블을 생성 또는 변경할 때마다 작업 파일이 생성되는데 이 작업 파일을 리비전 파일이라고 한다. 그리고 이 리비전 파일은 migrations 디렉터리에 저장된다.

이어서 alembic.ini 파일을 파이참으로 열어서 다음과 같이 수정하자.

[파일명: projects/myapi/alembic.ini]

(... 생략 ...)
sqlalchemy.url = sqlite:///./myapi.db
(... 생략 ...)
alembic이 사용할 데이터베이스의 접속주소를 설정했다.

그리고 migrations 디렉터리의 env.py도 다음과 같이 수정하자.

[파일명: projects/myapi/migrations/env.py]

(... 생략 ...)
import models
(... 생략 ...)

# add your model's MetaData object here

# for 'autogenerate' support

# from myapp import mymodel

# target_metadata = mymodel.Base.metadata

target_metadata = models.Base.metadata
(... 생략 ...)
리비전 파일 생성하기
그리고 파이참 터미널에서 alembic revision --autogenerate 명령을 수행하자.

[파이참 터미널]

(myapi) c:/projects/myapi> alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'question'
INFO  [alembic.autogenerate.compare] Detected added table 'answer'
  Generating projects/myapi/migrations/versions/fed28bf52b05_.py ...  done  
그러면 migrations/versions 디렉터리에 fed28bf52b05_.py와 같은 리비전 파일이 생성된다. 리비전(revision)이란 생성된 fed28bf52b05_.py 파일에서 .py 확장자를 제외한 fed28bf52b05_와 같은 버전 번호를 가리킨다. 리비전은 alembic revision --autogenerate 명령을 수행할 때 무작위로 만들어진다.

리비전 파일에는 테이블을 생성 또는 변경하는 실행문들이 들어 있다.

리비전 파일 실행하기
이어서 alembic revision --autogenerate 명령으로 만들어진 리비전 파일을 alembic upgrade head 명령으로 실행하자.

[파이참 터미널]

(myapi) c:/projects/myapi> alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> fed28bf52b05, empty message
이 과정에서 데이터베이스에 모델에 정의한 question과 answer라는 이름의 테이블이 생성된다. 지금까지 잘 따라왔다면 projects/myapi 디렉터리에 myapi.db 파일이 생성되었을 것이다. myapi.db가 바로 SQLite 데이터베이스의 데이터 파일이다.
