# 项目名称 / Project Name

## 简介 / Introduction

本项目属于东北财经大学金融科技实验室，是为了标注文本数据而开发。  
This project belongs to the Financial Technology Laboratory of Dongbei University of Finance and Economics and is developed for annotating text data.

## 功能 / Features

- 使用 FastAPI 提供后端 API 接口  
  Provides backend API interfaces using FastAPI
- 使用 Gradio 创建前端界面  
  Creates a frontend interface using Gradio
- 支持文本数据的获取和更新  
  Supports fetching and updating text data

## 安装 / Installation

1. 克隆本仓库 / Clone this repository:
    ```bash
    git clone <repository_url>
    ```

2. 安装依赖 / Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 使用 / Usage

1. 启动后端服务 / Start the backend service:
    ```bash
    uvicorn app:app --reload
    ```

2. 启动前端界面 / Start the frontend interface:
    ```bash
    python gradio_app.py
    ```

## 贡献 / Contributing

欢迎提交问题和拉取请求。  
Feel free to submit issues and pull requests.

## 许可证 / License

本项目使用 Apache 2.0 许可证。  
This project is licensed under the Apache 2.0 License.