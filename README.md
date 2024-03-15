# 2024年春季睿信-C语言程序设计 BITLeXueRANK_2024C
# 反卷王提示脚本By DecEric

2024年春季睿信-C语言程序设计排名更新系统

| 提醒！ | 在 **formatted_time** 时，**current_user_name** 已经完成了 **current_problem_name**。|
|---------|--------------------------------------|
| 附件 | PNG图片，目前前十名情况|

这段代码是一个Python脚本,使用Selenium WebDriver自动与一个网站(https://lexue.bit.edu.cn/course/view.php?id=15114)进行交互。以下是代码的分解:

它导入了必要的模块,如selenium、hashlib、requests、smtplib和email。
它设置了SMTP服务器详细信息、发件人和收件人邮箱地址、登录URL以及网站的用户凭证。
它初始化了Chrome WebDriver,使用无头模式和其他选项。
它导航到登录URL,并通过输入账号和密码凭证执行登录过程。
它进入一个循环,不断刷新网站并检查"最新提交的题目"部分是否有更新。
如果检测到用户"杨 宏宇"有新的题目,它会截取最新AC(通过)题目和当前排行榜截图。
它构造一封电子邮件,包括主题、内容和截图作为附件。
它使用SMTP服务器凭证将电子邮件发送到指定的收件人邮箱地址。
这个脚本的设计目的是监控特定用户在一个在线编码比赛或课程中的进展,并在用户解决新问题时发送带有更新内容和相关截图的电子邮件通知。

注意:你需要用实际的SMTP服务器详细信息、电子邮件地址、账户凭证和网站URL替换占位符,才能使脚本正常工作。

## 为何需要我的账号、密码？

如前所述，程序需要登录乐学，因而需要一个已登录的账户。

像这样的程序确实有可能窃取您的账号、密码，您的确应当保持警惕。但若您检查一下这个程序的代码，就会发现它并未这样做。