# 这是一个 xtdx 刷课答题的脚本
# 项目架构
## 思路
## 代码分层
```
xtdx
- logs 日志目录
- openAI openai服务目录
- tools 公共工具目录
- - mysql_base.py mysql的基础工具 提供连接、增删改查功能
- - qa_data_tools.py 题库数据更新类
- - request_base.py request请求封装,方便打印日志
- auto_qa.py 答题脚本
- auto_sutdy.py 刷课脚本
- config.py 全局配置
- data.py 
- data_tools.py
- .project_root 用于定位项目目录路径
- logger_base.py 日志公共类
- qa_tools.py 答题工具类
```
# 如何运行
### 安装
```
cd xtdx
python -m venv venv

# windows
venv\Scripts\activate
# Liunx
source myenv/bin/activate

pip install -r requirements.txt
```
### 配置
修改 config.py 中 cookies (浏览器登录后开发者工具随便拿个xtdx.web2.superchutou.com域的接口cookies即可)
### 自动刷题
```liunx
python auto_study.py
```
### 自动答题
```liunx
python auto_qa.py
```
# 未来规划
# 联系我们