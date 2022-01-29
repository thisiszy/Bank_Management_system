# Bank Management System
数据库课程大作业

## 使用
1. 安装mysql
2. 克隆仓库
```bash
git clone https://github.com/thisiszy/Bank_Management_system.git
cd Bank_Management_system
```
3. frontend
```bash
cd frontend
npm install
npm run serve
```
4. backend
```bash
cd ..
pip install -r requirements.txt
./run.sh
```
5. 导入数据，用mysql依次执行`crebas.sql`和`insdata.sql`文件即可。
6. 默认没有登录验证，如果要加入，可以将app.py中的`NO_AUTH`改为`False`（如果开启登陆验证，需要手动使用`backend/action.py`中的`addAdmin`函数添加用户名和密码。

## 其它信息
关于系统的设计之类的资料见`doc.pdf`