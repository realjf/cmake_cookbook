## 获取docker镜像

```shell script
docker run -it devcafe/cmake-cookbook_ubuntu-18.04
git clone https://github.com/dev-cafe/cmake-cookbook.git
cd cmake-cookbook
pipenv install --three
pipenv run python testing/collect_tests.py 'chapter-*/recipe-*'

```

