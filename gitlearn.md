### 使用git最小配置

* 配置方法  
git config --global user.name 'xxxx'  
git config --global user.email 'xxxx'  

* 查看配置信息  
git config --list (--global)
global当前用户所有仓库有效，local只对当前仓库有效, system对系统所有用户有效
### 建立git仓库
两种场景
	已有项目代码纳入已有管理 cd 文件夹； git init
	新建项目使用git管理 cd文件夹； git init PROJECT会生成项目文件夹；

### git工作区
git status 查看状态信息
git rm remove暂存区文件
git mv readme.md readme.txt 重命名文件
git add 后面可以跟多个文件 文件夹 git add index.html images
git add -u 将所有收到管理的文件添加到暂存区
git commit -m'add index + images
git log 查看日志
git log oneline 简洁模式查看git历史
git log -n5 查看最近的5个commit 可以组合使用 git log -n5 --oneline
git log --all --graph --oneline --n4 图形化展示 --all表示所有分支的历史
gitk工具图形化变更信息
### .git仓库




### github
####