# apiRemoteLLM
## 一个可以穿透连接远端大模型的接口

### 使用方法：
    1、先在远程的服务器中部署好ollama（或者vllm、sglang等平台）
    2、pip install -r requirement.txt
    3、设置ssh免密登陆：
        ```
        ssh-keygen -t rsa -b 4096
        ssh-copy-id -i ~/.ssh/id_rsa.pub -p port user@remote_server
        ```
    4、在config中添加对应的配置

### 功能：
    1、zotero划词翻译
        1、安装zotero插件：Translate for Zotero
        2、翻译服务选择customGPT，密钥随便填，接口填http://localhost:5001/zotero_translate, 其中5001为config文件中的 '''MAIN_PORT'''
    
    2、immersive translate网页翻译
        1、安装浏览器插件immersive translate，
        2、自定义API地址：http://localhost:5001/immersive_translate，密钥随便填
    
    3、libre translate翻译
        加载只需要的语言包：libretranslate --load-only en,zh
        1、打开http://localhost:5002，其中5001为config文件中的 '''LIBRE_TRANSLATION_PORT'''
        2、可以在translate_web/templates/app.js.template中修改默认prompt、model及temprature的值，字段分别为promptText、modelText、temperatureText

    4、cherry studio、chatbox
        1、路由地址为http://localhost:5001/cherry_studio


