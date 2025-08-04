# apiRemoteLLM
## 一个可以穿透连接远端大模型的接口

### 使用方法：
    1、先在远程的服务器中部署好ollama（或者vllm、sglang等平台）
    2、pip install -r requirement.txt
    3、设置ssh与公网IP免密登陆：
    linux 和 macos：
        ```
        ssh-keygen -t rsa -b 4096
        ssh-copy-id -i ~/.ssh/id_rsa.pub -p [公网ssh端口] [user]@[公网ip]
        ```
    windows:
        ```
        ssh-keygen -t rsa -b 4096

        type $env:USERPROFILE\.ssh\id_rsa.pub | ssh [公网端口] [user]@[公网ip] -p [公网ssh端口] "mkdir -p `$HOME/.ssh && chmod 700 `$HOME/.ssh && cat >> `$HOME/.ssh/authorized_keys && chmod 600 `$HOME/.ssh/authorized_keys"
        ```
    4、设置公网与计算节点免密登录
        ```
        ssh-keygen -t rsa -b 4096
        ssh-copy-id -i ~/.ssh/id_rsa.pub -p [计算节点端口] [user]@[计算节点ip]
        ```

    5、在config中添加对应的配置
        ```
        PUBLIC_IP = '公网ip'
        PRIVATE_PORT = 公网ssh端口
        USER_NAME = '账号'
        REMOTE_PORT = 计算节点11434映射到公网服务器的端口
        HOST = '127.0.0.1'
        LOCAL_PORT = 10001
        MAIN_PORT = 5001
        LIBRE_TRANSLATION_PORT = 5002
        SSH_KEEP_ALIVE = 3600
        ```

### 功能：
    1、zotero划词翻译
        1、安装zotero插件：Translate for Zotero
        2、翻译服务选择customGPT，密钥随便填，接口填http://localhost:5001/zotero_translate, 其中5001为config文件中的 '''MAIN_PORT'''
    
    2、immersive translate网页翻译
        1、安装浏览器插件immersive translate，
        2、自定义API地址：http://localhost:5001/immersive_translate，密钥随便填
    
    3、libre translate翻译
        1、打开http://localhost:5002，其中5001为config文件中的 '''LIBRE_TRANSLATION_PORT'''
        2、可以在translate_web/templates/app.js.template中修改默认prompt、model及temprature的值，字段分别为promptText、modelText、temperatureText

    4、cherry studio、chatbox
        1、路由地址为http://localhost:5001/cherry_studio#


