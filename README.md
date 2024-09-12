## 发票检测技术文档

### Version 2.0--PyQt + MySQL Database

#### Racheus Zhao，JAKA Intern

2024 Summer

---

### 1.前言

在1.0版本后，经过他人的建议和不断地修改，在原有的基础上做出了2.0版本。2.0版本基于Qt进行开发，拥有更加美观的前端界面。同时引入流行的数据库MySQL进行数据的存储。同时加强了对数据的添加、修改、读取等功能。

![UI window](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\ui.png)

新一代的界面保留了上一代的一些功能，重新整理了按键的位置和布局。

### 2.技术细节

#### 2.1 接入MySQL

MySQL在过去由于性能高、成本低、可靠性好，已经成为最流行的开源数据库，因此被广泛地应用在Internet上的中小型网站中，在个人端的pc上部署MySQL8.0或9.0，具体教程可参考网络教程。

在命令行中初始化，并建立数据库。当然，你也可以在一些图形化操作界面中手动添加。

```mysql
> mysql -u root -p
> password : #在此输入你的密码
```

然后我们建立一个数据库，当然你可以取你自己想要的名字，不过需要修改一些代码的设计。

建议在命令行中按照以下方式建立：

```mysql
CREATE TABLE tb_invoice (
id INT(8) NOT NULL AUTO_INCREMENT,
invoice_code varchar(50) NOT NULL,
date varchar(50) ,
buyer_code varchar(50),
buyer_name varchar(50),
seller_code varchar(50),
seller_name varchar(50),
invoice_amount_SMALL varchar(50),
note varchar(255),
PRIMARY KEY (id)
)
```

当然，还提供了一种方法，可以直接运行`db_setup.py`文件,通过为您写好的python脚本搭建数据库。

```python
python db_setup.py
```

#### 2.2 从文件夹批量读入发票文件

最重要最核心的应用就是从文件夹导入。我们的想法是客户会每天、每周、甚至每月会有一个积累发票的文件夹。最好以pdf的形式储存，这个程序会自动读取pdf格式的文件夹。步骤如下图所示：

![tutor1](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\folderchoose.png)

测试系统会自动运行整理发票。整理完成后会弹出弹窗提示在这轮检测的过程中没有被检测到的发票。如果全部检测完成，系统会弹出成功的提示样例。

![Error List](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\errorlist.png)

*未来2.1版本考虑将未检测成功的发票的文字信息附在一个新的页面中，用户可以通过手动的复制粘贴进行未检测成功发票信息的录入操作，以及相关界面的设计。预计为左右排版，右侧文本框提供纯文字信息。*

#### 2.3 发票的搜索操作

在数据库中，区分发票信息的唯一关键字为**“发票号码”**，即每张发票应该拥有唯一的发票号码。因此搜索的过程应该采用这一唯一关键字。

如果搜索成功，主界面会变成以下样式：

![search_ok](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\search_YES.png)

如果不成功，会变成以下样式：

![Search failed.](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\search_NO.png)

####  2.4 发票的修改操作

修改操作是基于搜索操作的，一个很简单的道理，修改需要告诉程序：你要修改哪条信息？因此在设计的过程中，modify的运行必须基于已有的搜索，否则会出错误。

![modify](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\modify.png)

在一个新的界面中，可以进行预填信息的编辑，预填信息是从数据库中搜索出的信息，二者保持一致。

下面是一个例子，在命令行中对数据库进行搜索：

```mysql
select * from tb_invoice;
```

这是修改前的某张发票的信息：

![Before](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\origindata.png)

这是执行修改后的程序信息：

![Modified](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\modified.png)

#### 2.5 发票的删除操作

和修改发票信息相似，修改操作是基于搜索操作的，点击删除按钮后会出现以下界面对用户进行提示：

![delete](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\del.png)

确定删除后将从数据库中删除这条信息，**需要注意的是**，删除后不可恢复。

#### 2.6 添加新的发票

如果用户不希望通过文件等方法添加，可以手动添加相关的发票信息。

![add](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\add.png)

确定添加后点击“OK”即可，可以看到数据库中的变化：

![数据库中添加项](C:\Users\dell\Desktop\InvoiceDetector2.0\Image\dbadd.png)

以上是2.0版本的基础使用细节。

*笔者将在近期继续优化界面以及功能逻辑，预计9月中旬前发布2.1版本，敬请期待。*

---

Racheus Zhao 

JAKA Intern 

2024/8/9


