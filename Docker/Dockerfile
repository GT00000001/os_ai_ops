# 1. 选择基础镜像
FROM python:3.12-slim

# 2. 设置工作目录（容器内部路径）
WORKDIR /app

# 3. 复制依赖清单，并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu126 -r requirements.txt


# 4. 复制项目代码
COPY . .

# 5. 容器启动时执行的命令
CMD ["python", "response_generator.py"]
