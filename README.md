# file-remark
Add a remark for the file in the OS.

## 项目地址

github: <https://github.com/icexmoon/file-remark>

gitee: <https://gitee.com/icexmoon/file-remark>

pypi: <https://pypi.org/project/file-remark-icexmoon/>

## 用途

这是一个可以给系统中的文件或路径添加备注的小工具。

特点有：

- 使用绝对路径来匹配文件。
- 独立数据存储，不依赖于文件的meta信息。

缺点有：

- 文件如果移动后，就无法关联到备注信息（后续可以考虑添加md5匹配的机制）。

## 目的

之所以我会开发这么个小工具，是因为有时候会遇到需要给安装程序备注一个激活码，或者给压缩包备注一个解压密码的情况，此时多数情况是不得不添加一个额外的txt文件来说明，不仅麻烦，还显得很多余。

当然我也有在网上搜索类似的工具，但没有找到，只找到一个可以在文件的meta信息中写入备注的工具，但这个工具有个缺点，如果文件被修改了，meta信息就会被重写，导致添加的备注丢失。

## 使用说明

### 安装

```shell
pip install file-remark-icexmoon
```

### 更新

```shell
pip install file-remark-icexmoon --upgrade
```

### 显示当前目录下的文件和目录

```shell
pyfr
```

该命令可以同时显示已添加的文件备注和未添加备注的目录和文件。

比如：

```shell
❯ pyfr
- LICENSE [this is a license for open source]
- pyproject.toml [this is a test comment]
d src [this is a source directory]
- .git
- .vscode
d dist
- README.md
- setup.cfg
- setup.py
d tests
```

其中`[xxx]`是添加的备注信息。默认先显示有备注的文件，再显示其他的，但也可以使用其它参数修改显示结果。

开头的`d`或`-`是用来区分目录还是文件，这里使用的是Linux中的风格。

### 修改显示结果

可以使用多种参数修改显示结果：

- `-o`或`--only_remark`：仅显示添加了备注的文件或目录。
- `-l`或`--remark_last`：将由备注信息的条目显示在最后。

### 添加备注

```shell
pyfr --add --file .\LICENSE --remark 'this is a license for open source'
```

或

```shell
pyfr -af .\LICENSE -r 'this is a license for open source'
```

`-f`参数后是需要添加备注的文件路径，可以使用相对路径或绝对路径。`-r`参数后是备注的内容，如果包含空白符需要使用引号包裹。

执行完毕后会自动打印当前目录下的条目以便查看添加结果。

> 目前只能添加备注，之后会增加修改备注和删除备注的功能。

### 显示系统版本

```shell
pyfr -v
```

或

```shell
pyfr --version
```

### 初始化程序

```shell
pyfr --init_process
```

如果数据库损坏或遇到其它问题，可以使用此功能尝试重新初始化程序，但该操作将丢失已添加的所有数据。

## 更新日志

- 0.0.1 基础版本。
- 0.0.2 修改数据库表结构，添加显示版本功能。
- 0.0.3 修复程序初始化会出错的bug。
- 0.0.4 升级数据库到v3，输出信息中添加标识区分文件和目录