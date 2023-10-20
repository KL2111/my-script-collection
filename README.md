# My-scrit-colletion

欢迎来到我的脚本集合！这里是我常用的各种实用脚本。脚本大多是由程序员 GPT 编写，而我作为一个 debug 测试员。

以下是各个脚本的详细介绍：

------

## 1. [md-yaml-front-matter-modify]((https://github.com/KL2111/my-script-collection/blob/main/md-yaml-front-matter-modify/md-yaml-front-matter-modify.py))

**作用**：

此脚本用于自动检查并更新 Markdown 文件的 YAML Front Matter。确保每一个文件中的 Front Matter 包含了预定义的关键字段，若某些字段缺失，该脚本将自动补全它们。

**使用方式**：

1. 运行脚本。复制到编辑器
2. 根据提示，输入文件或目录的路径。
3. 设置默认的 Front Matter 值或删除某些 Front Matter。
4. 选择是否需要对 `date` 和 `title` 进行特定的修改策略。
5. 根据每个文件的内容，决定是否应用修改。

**工具依赖**
1. Python版本
Python 3.x 
3. 依赖库
以下是运行此脚本所需的Python库，您可以使用pip进行安装：

os （Python内置库，用于操作系统相关操作）
re （Python内置库，用于正则表达式）
```
pip install [库名]
```
