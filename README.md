# NewWordSpider项目使用文档

## 1. 项目概述
   本项目旨在通过爬取特定网站的内容，提取新词，并将其转换为**小鹤双拼**格式
   最终保存到Rime用户词库中。
   项目支持使用 jieba 分词和 DeepSeek API 进行分词，并提供异步处理功能以提高效率。

### **效果演示**

程序默认会在指定的rime用户词库(默认名称为rime_user_dict.txt)后面附加新词
并且打上时间日期注视，重复的词将不会被重复添加。
同时内置的sqlite数据库会备份老词库，加入新词，防止数据丢失

<img src="./misc/rime20240923-123653.png" width="600" height="300" />

其中windows的rime用户词库位于用户home目录下的特定位置
"C:\Users\用户名\AppData\Roaming\Rime"

## 2. 项目结构

```bash
project_root
├── main.py
├── tokenizer.py
├── crawler.py
├── RimeUserDict.py
├── PinyinTools.py
├── logger_config.py
├── config.json
└── README.md
```

##   3. 主要文件说明
main.py
主程序入口，负责读取配置文件、爬取新句子、分词、转换拼音、保存词库等操作。

tokenizer.py
分词模块，支持 jieba 分词和 DeepSeek API 分词。提供异步分词功能。

crawler.py
爬虫模块，负责从指定网站爬取新句子。支持不同的解析器策略。

RimeUserDict.py
Rime用户词库管理模块，负责读取、写入、追加和保存Rime用户词库文件和SQLite数据库。

PinyinTools.py
拼音工具模块，负责将汉字转换为拼音，并将全拼转换为小鹤双拼。

logger_config.py
日志配置模块，负责配置日志系统，并提供自定义日志记录器。

config.json
配置文件，包含API URL、API Key、分词模式等配置项。

README.md
项目说明文档，包含项目概述、安装说明、使用说明等。

app.log
运行时自动生成的日志文件，记录程序运行时的日志信息。


## 4. 安装与配置
### 4.1 安装依赖
在项目根目录下运行以下命令安装所需的依赖包：


```bash
pip install -r requirements.txt
```
建议使用conda等环境进行依赖管理。

### 4.2 配置文件
在 config.json 文件中配置以下参数：

```json
{
"API_URL": "https://api.deepseek.com/chat/completions",
"API_KEY": "<DeepSeek API Key>",
"SPLIT_WORDS_MODE": "deepseek",
"USER_DICT_PATH": "./flypy_user.txt",
"USER_DICT_DB_PATH": "./flypy_user.db"
}
```
API_URL : DeepSeek API 的 URL。,当然你也可以用其他LLM的api

API_KEY : DeepSeek API Key。

SPLIT_WORDS_MODE : 分词模式，可选值为 deepseek 或 jieba。

USER_DICT_PATH : Rime 用户词库文件路径。

USER_DICT_DB_PATH : SQLite 数据库文件路径。

### 4.3 运行项目
在项目根目录下运行以下命令启动项目：

```bash
python main.py
```
### 4.4 日志记录
项目会将运行时的日志信息记录到 app.log 文件中，并在控制台输出。日志信息包括函数名和模块名，方便调试和排查问题。

### 4.5 分词模式
项目支持两种分词模式：

deepseek : 使用 DeepSeek API 进行分词。
jieba : 使用 jieba 进行分词。
分词模式在 config.json 文件中配置。

### 4.6 数据库操作
项目会将新词条保存到 SQLite 数据库中，并在初次运行时备份老用户词典的数据。数据库文件路径在 config.json 文件中配置。

### 4.7 词库文件操作
项目会将新词条追加到 Rime 用户词库文件中，并在每次追加时添加日期注释。词库文件路径在 config.json 文件中配置。

