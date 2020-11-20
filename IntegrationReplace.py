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
    # 源文件中变量和值的分隔符
    srcchar = '='
    # 规则文件中替换变量的分隔符
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
                            # 如果还有替换的情况，可以在此扩展
                            pass

if __name__ == "__main__":
    ir = IntegrationReplace()
    ir.dowork()
