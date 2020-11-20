# 智能集成软件

大家在做集成测试的时候，可能会遇到需要修改大量的输入文件的问题，今天我们就来解决这个比较棘手的问题，让我们使用python来解决这个难题

下面是一个基本算例文件，比如说input_a的取值范围为（0，2），我们需要测试input_a的边界值是否能够通过测试，我们修改一下input_a所对应的值，需要有两个case文件，在第一个文件中 将input_a的值修改为0，在第二个文件中将input_a的值修改为2，这个时候我么就可以开始进行测试啦。

```python
input_a  = 1
input_b  = 2
input_c  = 3
input_d  = 4,5,6,7
```

##### case001.data这是第一个算例文件，下面是对应的内容

```python
input_a  = 0
input_b  = 2
input_c  = 3
input_d  = 4,5,6,7
```

##### case001.data这是第二个算例文件，下面是对应的内容

```
input_a  = 2
input_b  = 2
input_c  = 3
input_d  = 4,5,6,7
```

可以看到，上述两个文件只需要修改一个变量的值就行了，如果遇到变量的变量比较的多，用传统手工方式来做，明显是不合适的，这个时候，我们就需要使用我们不败顽童大神来编写一个小程序解决这个问题啦。

在讲述代码之前，我们需要搞定两个文件，一个称为source.txt文件，这个就是基本算例文件，另一个就是替换的文件啦，我们称之为rule.txt文件，比如说上面的栗子中，input_a的取值范围为（0，2），我们只需要在第二行写一个WE，input_a，0；2就行啦，我们在运行程序的时候，就会生成上面case001.data和case002.data文件，是不是非常的方便呢。

```python
type,variant,data,detail
WE,input_a,0;2
WE,input_b,13;14
WE,input_c,15;16
WE2,input_d,17;18;19;20
```

接下来，我们的主角开始正式登场——智能集成软件

```python
# 智能集成测试软件 
# Version 1.1
# @author: 不败顽童
# 版权所有，翻录必究

class IntegrationReplace:
    sourcefile = "source/source.txt"
    rulefile = "source/rule.txt"
    newfilename = ""
    srclines = ""
    rulelines = ""
    # 源文件中变量和值的分隔符，可以根据需求修改
    srcchar = '='
    # 规则文件中替换变量的分隔符，可以根据需求修改
    rulechar = ';'
    # 源文件和规则文件通用的分隔符
    char = ','
    count = 1

    # 初始化源文件位置、规则文件位置
    def __init__(self, sourcefile, rulefile, srcchar, rulechar):
        self.sourcefile = sourcefile
        self.rulefile = rulefile
        self.srcchar = srcchar
        self.rulefile = rulechar

    # 默认初始化
    def __init__(self):
        pass

    # 读取源文件和规则文件中的到srclines和rulelines
    def readFiles(self):
        with open(self.sourcefile, 'r', encoding="utf-8") as sf:
            self.srclines = sf.readlines()
        with open(self.rulefile, 'r', encoding="utf-8") as rf:
            self.rulelines = rf.readlines()

    # 开始替换并生成新文件（case文件）
    def writeNewFile(self, newsrcline, srcline):
        self.newfilename = "case/case" + str(self.count).zfill(3) + ".txt"
        # 读取源文件里面的数据
        with open(self.sourcefile, 'r', encoding='utf-8') as sf:
            newsrclines = sf.readlines()
        srcindex = newsrclines.index(srcline)
        newsrclines[srcindex] = newsrcline.replace('\n', '') + "\n"
        with open(self.newfilename, 'w', encoding='utf-8') as nf:
            nf.writelines(newsrclines)
        self.count += 1
        print(self.newfilename + "is created successful!")
        print(newsrcline)

    # 主函数
    def dowork(self):
        # 遍历规则文件的每一行
        self.readFiles()
        for ruleline in self.rulelines:
            datas = ruleline.split(self.char)
            datas = datas[2].split(self.rulechar)
            # 遍历每个规则文件的每一行中的每个替换数据
            for data in datas:
                self.newfilename = "case/case" + str(self.count).zfill(3) + ".txt"
                # 遍历源文件中的每一行
                for srcline in self.srclines:
                    newline = srcline.split(self.srcchar)
                    newruleline = ruleline.split(self.char)
                    # 如果源文件中的变量名和规则文件的变量名一样，则开始替换
                    if (newline[0].replace(' ', '') == newruleline[1].replace(' ', '')):
                        # 单个数据替换
                        if (newruleline[0] == "WE" or newruleline[0] == "we"):
                            newsrcline = srcline.replace(newline[1], data)
                            # 进行替换，并生成case文件
                            self.writeNewFile(newsrcline, srcline)
                        # 多个数据替换
                        elif newruleline[0] == "WE2" or newruleline[0] == "we2":
                            dList = newline[1].split(self.char)
                            for d in dList:
                                newsrcline = srcline.replace(d, data)
                                # 进行替换，并生成case文件
                                self.writeNewFile(newsrcline, srcline)
                        else:
                            # 如果还有其它替换的情况，可以在此扩展
                            pass

if __name__ == "__main__":
    ir = IntegrationReplace()
    ir.dowork()
```

我们可以看一下程序之后的结果：

```python
case/case001.txtis created successful!
input_a  =11
case/case002.txtis created successful!
input_a  =12

case/case003.txtis created successful!
input_b  =13
case/case004.txtis created successful!
input_b  =14

case/case005.txtis created successful!
input_c  =15
case/case006.txtis created successful!
input_c  =16

case/case007.txtis created successful!
input_d  =17,5,6,7
case/case008.txtis created successful!
input_d  = 4,17,6,7
case/case009.txtis created successful!
input_d  = 4,5,17,7
case/case010.txtis created successful!
input_d  = 4,5,6,17
case/case011.txtis created successful!
input_d  =18,5,6,7
case/case012.txtis created successful!
input_d  = 4,18,6,7
case/case013.txtis created successful!
input_d  = 4,5,18,7
case/case014.txtis created successful!
input_d  = 4,5,6,18
case/case015.txtis created successful!
input_d  =19,5,6,7
case/case016.txtis created successful!
input_d  = 4,19,6,7
case/case017.txtis created successful!
input_d  = 4,5,19,7
case/case018.txtis created successful!
input_d  = 4,5,6,19
case/case019.txtis created successful!
input_d  =20,5,6,7
case/case020.txtis created successful!
input_d  = 4,20,6,7
case/case021.txtis created successful!
input_d  = 4,5,20,7
case/case022.txtis created successful!
input_d  = 4,5,6,20
```

![img](result.png)



下面是所有的资料文件，已经写好咯，欢迎各位网友评论关注哟，感觉博主写的好的话记得给博主一键三连哟



链接：https://pan.baidu.com/s/1BXzKPP5g5kZjq4XVYxrxeQ 
提取码：67zr 