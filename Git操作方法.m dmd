### **git命令**
	
	> git clone https://....... [项目名]  克隆下来远程仓库
	> git remote -v 查看远程仓库
	> git commit -a( add的意思 ) -m "描述"
	> git push 向远程仓库提交已经commit的内容

	> git 查看git命令
	> git help -a 查看所有git子命令
	> git blame -L 100,110 <filename> 逐行(从100-110行)查看修改历史
	> git clean -n 列出要清楚的档案(还没有放入缓存区的文件）
	> git clean -f 真正清楚
	> git clean -x 连gitignore忽略的档案也清除
	> 删除1. git rm a.txt 在缓存区里将a文件删除
	> 删除2. rm a.txt 之后再 add . 
	> git add -p a 一个文件内的修改分多次提交
	
	> git status 查看当前状态 -sb short branch 信息更简略

	> git show HEAD(hash值) 查看某个提交的信息
	> git show HEAD^ 查看HEAD前一个提交
	> git show HEAD~2 查看HEAD前第二个提交
	
	show加哈希，log看仓库或文件
	> git log 查看日志
	> git log 
	> git log --oneline 查看简化版日志
	> git hi 日志用到极致了是这个(log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short)
	 --grep <msg> 可以过滤
	 -n 查看最新的n条
	> git log <file name> 查看某个文件的提交情况

	> git diff hash1 hash2 查看两个版本之间的差异
	> git diff 工作区与暂存区的差异
	> git diff --cached 暂存区与HEAD版本的差异
	> git diff HEAD 工作区与HEAD版本的差异
	> git diff <tag name> 工作区与tag版本的差异

### **Commit规范**
	<type> (<scope>) : <subject>
	// 空一行
	<body>
	// 空一行
	<footer>
	
	第一行head，整体不超过72字。scope是模块、文件名等，可不写。
	subject要用现在时态描述，动词开头create等，无句号。
	
	body详细解释，可以换行，也是第一人称。
	
	footer可以关闭Issues：
	close #6 关闭第6号footer可以关闭Issues

	- type:
		feat：新功能（feature）
		fix：修复bug
		docs：文档
		style：格式（不影响代码运行的变动）
		refactor：重构
		test：增加测试
		chore：构建过程或辅助工具的变动
	
	demo:
		docs(dom): edit dom/element
	
### **配置别名**
git config --global alias.ci commit
or
进入～的.gitconfig中写
[alias]
        ci = commit

### **回撤操作**
> git reset HEAD 回撤暂存区内容到工作目录
> git reset HEAD --soft 回撤提交内容到暂存区
> git reset HEAD --hard 回撤提交，完全放弃变更(回到工作目录？）（只要记得hash值，还可以再回去）
> git push -f 回撤远程仓库
> - git add .
> - git commit --amend  -m "message" 回撤前一次提交并与现在的修改一同算做新一次提交，提交上去。
> git rebase -i HEAD~3 选择最近3个提交做变基操作，之后会进到窗口：
> - 


### **协议**
- 本地协议：
本地clone、pull、push等
在局域网的文件服务器中使用
不建议加file:// 直接用路径
- git协议
访问速度快，无授权机制
一般用作只读仓库，配合其他协议用
- http(s)协议
克隆远程仓库
添加远程仓库
使用
每次要输入密码
- SSH SecureShell
git clone ssh://.......
git clone git@github.com : ...... [项目名] (一般用这种简写)
git remote add origin git@github.com : ......
生成密钥：
ssh-Keygen -t rsa -C "your email"
(-t rsa是密钥算法)
之后问到的passphrase设置为空即可
然后去保存目录里找，用一个带pub后缀的是公钥
要把公钥放到guthub网站上
