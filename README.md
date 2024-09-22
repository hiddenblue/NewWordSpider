# NewWordSpider项目使用文档

## 1. 项目概述
   本项目旨在通过爬取特定网站的内容，提取新词，并将其转换为**小鹤双拼**格式
   最终保存到Rime用户词库中。
   项目支持使用 jieba 分词和 DeepSeek API 进行分词，并提供异步处理功能以提高效率。

## 2. 项目结构

```bash
   project_root/
   │
   ├── main.py
   ├── tokenizer.py
   ├── crawler.py
   ├── RimeUser.py
   ├── PinyinAdder.py
   ├── QuanPintoXiaohe.py
   ├── logger_config.py
   ├── config.json
   ├── README.md
```

##   2.1 主要文件说明
   main.py : 项目的主入口文件，负责调用其他模块进行分词、转换和保存操作。 
   
tokenizer.py : 包含分词相关的函数，支持 jieba 分词和 DeepSeek API 分词。

crawler.py : 包含爬取网站内容的函数。

RimeUser.py : 包含与Rime用户词库相关的操作，如读取、写入和追加词条。

PinyinAdder.py : 包含将汉字转换为拼音的函数。

QuanPintoXiaohe.py : 包含将全拼转换为小鹤双拼的函数。

logger_config.py : 包含日志配置相关的函数。

config.json : 配置文件，包含API URL、API Key、分词模式等配置项。

README.md : 项目说明文档。
   
app.log : 日志文件，记录程序运行时的日志信息。

## 3. 安装与配置
   ### 3.1 安装依赖
   在项目根目录下运行以下命令安装所需的依赖包：

```bash
pip install -r requirements.txt
```
### 3.2 配置文件
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
API_URL : DeepSeek API 的 URL。

API_KEY : DeepSeek API Key。

SPLIT_WORDS_MODE : 分词模式，可选值为 deepseek 或 jieba。

USER_DICT_PATH : Rime 用户词库文件路径。

USER_DICT_DB_PATH : SQLite 数据库文件路径。

## 4. 使用说明
   ### 4.1 运行项目
   在项目根目录下运行以下命令启动项目：

```bash
python main.py
```
### 4.2 日志记录
项目会将运行时的日志信息记录到 app.log 文件中，并在控制台输出。日志信息包括函数名和模块名，方便调试和排查问题。

### 4.3 分词模式
项目支持两种分词模式：

deepseek : 使用 DeepSeek API 进行分词。
jieba : 使用 jieba 进行分词。
分词模式在 config.json 文件中配置。

### 4.4 数据库操作
项目会将新词条保存到 SQLite 数据库中，并在初次运行时备份老用户词典的数据。数据库文件路径在 config.json 文件中配置。

### 4.5 词库文件操作
项目会将新词条追加到 Rime 用户词库文件中，并在每次追加时添加日期注释。词库文件路径在 config.json 文件中配置。

