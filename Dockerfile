# 第一阶段：构建阶段
FROM python:3.10-slim AS builder

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器中的 /app 目录
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段：运行阶段
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 从构建阶段复制必要的文件
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# 设置环境变量（如果需要）
# ENV LLM_API_URL=https://api.rebang.today/v1/items
# ENV LLM_API_KEY=your_api_key

# 运行 main.py 的无限循环
CMD ["python3", "main.py"]