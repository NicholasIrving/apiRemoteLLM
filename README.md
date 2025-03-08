# apiRemoteLLM

## 一个可以穿透连接 OLLAMA 的接口

### 使用方法

1. **在远程服务器部署**  
   先在远程的服务器中部署好 OLLAMA。

2. **安装依赖**  
   执行以下命令安装所需的 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. **设置 SSH 免密登录**  
   运行以下命令生成 SSH 密钥并将其复制到远程服务器：
   ```bash
   ssh-keygen -t rsa -b 4096
   ssh-copy-id -i ~/.ssh/id_rsa.pub -p <port> <user>@<remote_server>
   ```

4. **添加配置**  
   在 `config` 文件中添加相应的配置信息。

---

### 功能

#### 1. Zotero 划词翻译  
   - **安装 Zotero 插件**：`Translate for Zotero`。  
   - **配置翻译服务**：
     - 选择 **customGPT** 作为翻译服务。
     - **密钥**：任意填写。
     - **接口地址**：
       ```
       http://localhost:5001/zotero_translate
       ```
     - 其中 `5001` 由 `config` 文件中的 `MAIN_PORT` 决定。

#### 2. Immersive Translate 网页翻译  
   - **安装浏览器插件**：`Immersive Translate`。  
   - **自定义 API 地址**：
     ```
     http://localhost:5001/immersive_translate
     ```
   - **密钥**：可随意填写。

#### 3. Libre Translate 翻译  
   - **访问地址**：
     ```
     http://localhost:5002
     ```
     其中 `5002` 对应 `config` 文件中的 `LIBRE_TRANSLATION_PORT`。  
   - **自定义翻译参数**：  
     可在 `translate_web/templates/app.js.template` 文件中修改默认的 `prompt`、`model` 和 `temperature`：
     - `promptText`
     - `modelText`
     - `temperatureText`

#### 4. Cherry Studio / Chatbox  
   - 访问地址：
     ```
     http://localhost:5001/cherry_studio
     ```
