# 修改日志

| 时间        | 修改人 | 具体内容                                                     |
| ----------- | ------ | ------------------------------------------------------------ |
| 7.13  13:35 | UUQ    | 新增changelog文件                                            |
| 7.13  14:25 | LPR    | 增加static/templates目录，并push一个test.html，支持多个代码文件传入（第一个文件为std）、切换功能。还没支持相似代码高亮功能； 14:40 fix by UUQ |
| 7.13 15:18  | CZX    | README 新增需求                                              |
| 7.13 16:01  | UUQ    | README 前端需求 & **新增接口文档**                           |
| 7.13 21:53  | LPR    | 绘制了一个登陆后的主页、封装了侧边栏的css以及时间和内容展示的js，使用方法可以见menu.html（注：需要修改导入的offcanvas的地址） |
| 7.13 23:48  | LPR    | 修改主页，统一为bootstrap和vue，弃用原生js                   |
| 7.14   0:18 | UUQ    | 将sidebar打包成为vue组件，增加了history页面，**需要/history接口** |
| 7.14 20:55  | WDL    | 初始化Django项目，增加.gitignore文件，链接template/menu.html至主页 |
| 7.15 12:42  | UUQ    | 修复了history页面CSS样式的bug（单击左侧menu会使得页面布局改变），初步完成logout功能 |
| 7.15 15:06  | LPR    | 增加代码上传界面codesCompare.html支持条形图显示、代码下载、standard代码高亮**（其它代码高亮会有bug，这个需要进一步排查）**，对sidebar的显示进行调整（头像放在上面）。**需要后端传入diff列表** |
| 7.15 18:10  | LPR    | 修改了sidebar样式                                            |
| 7.16 14:12  | LPR    | 修改了图标的样式，增加人工标记抄袭/取消标记抄袭按钮，可支持将抄袭文件统一导出为zip的功能 |
| 7.16 17:53  | UUQ    | 增加了sidebar.js icon样式，修复了codesCompare页面模板中宽度过窄导致的margin占位div过窄问题<br>**未修复**：codesCompare页面右侧overflow-x滚动时优先级高于左侧offcanvas条、右侧页面宽度较大，是否改为按比例缩放？ |
| 7.16 02:36  | WDL    | 完成了部分用户登录和认证部分，增加了两个URL：users/login, users/register， **已migrate** |
| 7.17 12:05  | LPR    | 将之前写好的html移动到users目录下，将static移入app中 **（发现有bug，回滚到上一次提交）** |
| 7.17 14:43  | LPR    | 完成登录注册页面，@WDL 可以看一下我在你的user app里面viewer留言 |
| 7.18  0:25  | WDL    | _(上述注释中的问题已解决)_ 合并登录与注册功能，链接check/，codesCompare/与对应的template, 和其他的一些小改动 |
| 7.18  1:13  | LPR    | demo版本（后续可以用组合式api彻底解决，现在属于能够正常运行）在codesCompare和menu中非django传参部分禁止django渲染，解决上一次push后的问题 |
| 7.18  13:40 | CZX    | Codecheck 里，在urls和views里加了处理代码重复率的调用接口，一对多返回一个一维的列表，多对多返回一个二维数组，请求里应包含'pairwise'或'single_to_multiple'参数，表示进行哪种查询 |
| 7.18 19:27  | LPR    | 对settings进行跨域修改，修改codeCompare.html 现在codeCompare能从后端收到前端发来的东西了，具体数据还没有在前端显示 |
| 7.18 20:38  | CZX    | 新建了app：code_comparison，把上午实现的功能从项目目录迁移到了这个app中，新增历史记录功能，每次进行一对多查询，会把查询内容与结果存进数据库里，以及提供了相应的查询接口api/history，返回当前登录用户的历史记录列表 |
| 7.18 20:44  | WDL    | migrate新的代码历史模型                                      |
| 7.18 21:25  | CZX    | 修了一下 urls 的设置问题                                     |
| 7.22 13:00  | czx    | 查重加了 diff 的返回，并存进数据库中                         |
| 7.22 14:07  | czx    | 历史记录返回diff，加了个程设分组查询的代码 group_check_copy.py，有空看看怎么实现的 |
| 7.22 16:10  | UUQ    | 后端增加**/api/logout/接口**，并在前端sidebar组件中**对接完毕**（亲测可用），增加了**对/history/的鉴权**（login required，否则跳转到users/login/，方便测试），**修改history.html，实现了初步的信息展示**（但是跳转和一些具体的信息展示还没有写好，**细节需要讨论**） |
| 7：22 16:24 | LPR    | 修改codeCompared                                             |
| 7：22 16:50 | LPR    | 修改codeCompared文件，将diff文件接入，图形化垂直展示（具体见页面，太多了） |
| 7.23 1:01   | WDL    | 增加了history每一条比对历史的详细界面（写了初步的html和css），**发现本地logout若提示‘logout at static’则无法登出, 原因不清楚** |
| 7.23 2:47   | czx    | 增加分组查询，并进行简单测试                                 |
| 7.23 13:37  | LPR    | 让czx帮新的页面跳转过去的push czx：弄好了，我就不写log了     |
| 7.23 17:21  | LPR    | 把分组查重大部分写完了，剩下下载功能                         |
| 7.24 18:52  | czx    | 增加ast_check，新增查重需要传入'check_option'，默认为 'normal'，即普通查重，传入其它的则为ast语法树查重；分组查重可以选择传入'threshold'参数，即阈值，默认为0.8 |
| 7.24 20:41  | LPR    | 支持了分组查重的下载功能，优化了两个界面，支持当无重复度时的0-1恒定显示 |
| 7.24 23:42  | UUQ    | **login页面样式**（配色未调），TODO：把之前的正则放进去、登录注册结果反馈<br> history小改动，未写完 |
| 7.25 14:25  | LPR    | 增加ast和字符串匹配选项，让group比对的边可以呈现出similarity（这个貌似是字符串匹配的结果） |
| 7.25 16:36  | LPR    | 重构codeCompares.html，修改codeCompare逻辑                   |
| 7.25 16:58  | czx    | 改了下一对多查重的后端接口，适应前端                         |
| 7.25 19:21  | LPR    | 对接后端接口、支持手动修改阈值、支持前端显示std、修改下载bug |
| 7.25 20:33  | WDL    | model增加diff_content_html字段，方便历史记录中显示，**可能需要migrate** |
| 7.25 21:20  | UUQ    | 重写了login的登录逻辑，弃用了默认的表单submit（无法回调），未完成。 对users.views的login函数进行了修改（对请求的接受和处理） |
| 7.25 21:43  | czx    | 数据库表里新增了 'group_name' 和 'check_type' 两列，分别表示每次查询的组的名字和查询的类型（只能是'normal'或'ast'），在历史记录那里可以给予展示，历史记录新增 api/history_new/ 新接口，会以一组一组的列表形式返回一个json，详见api文档 |
| 7.26 0:00   | UUQ    | 修改了login接口逻辑（POST 接口，GET视图），迁移了logout路由到users；实现了login提示功能（**待完善**），实现了sidebar检测登录状态（依赖browser本地存储和users/check_login/接口） |
| 7.26 11:37  | UUQ    | 更新了login & register的失败/成功提示，增加了判空。**TODO：迁移旧页面的正则** |
| 7.26 15:27  | LPR    | 增加代码上传不全提示弹窗，调整页面样式、颜色                 |
| 7.26 15:45  | WDL    | 增加了修改密码、修改邮箱、修改头像、修改用户名功能，找了一个随机生成gitlab风格头像的加进去了，看后续有没有需求，需要**migrate， 另外修改头像功能还需要测试** |
| 7.26 16:02  | WDL    | 有点bug，删掉了信号部分，头像功能未完善                      |
| 7.27 1:02   | UUQ    | history 迁移到group接口，以文件名展示了submission名称，增加了时间显示。现在页面有点丑陋，白天调整。 |
| 7.27 1:08   | LPR    | 支持codesCompare传入类别名，**没看到给这个页面返回的以往历史列表** 、 |
| 7.27 11:52  | WDL    | 头像功能现在可以正常上传和显示                               |
| 7.28 16:12  | LPR    | 修改点击阴影无法关闭的bug，diff支持高亮                      |
| 7.28 16:27  | UUQ    | history展示样式（稍微漂亮一点的折叠，标题旁的提示），sidebar微调，profile和menu（主页）还在写 |
| 7.28 18:47  | UUQ    | 提示登录弹窗 & 头像返回和显示功能                            |
| 7.28 21:06  | UUQ    | history: 增加无记录时的显示，避免页面突兀<br>menu (index) 初步写入布局 |
| 7.28 22:30  | WDL    | 更美观的详细历史记录页面                                     |
| 7.30 12:43  | LPR    | 增加run.py文件，pycharm环境一键运行，需要配置好环境，修改sideBar图标 |
| 7.30 13:27  | czx    | 在查询时返回的列表里，新增每一条记录的 'id'，新增接口：api/mark_plagiarism，POST一个'id'和一个'mark'（'true' or 'false'）；修了一下history的时区问题 |
| 7.30 14:24  | LPR    | 接上上面了                                                   |
| 7.30 17:04  | UUQ    | history支持显示人工标注结果 &  sidebar logo图片响应 & 新index style（未登录时） |