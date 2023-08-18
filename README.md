# ChatMultiPDFs-Streamlit
A simple local ChatPDF program that supports uploading multiple PDFS. Techniques used: LangChain, Streamlit. You can replace any LLM interface or Embedding interface you prefer
<hr>

:sunglasses:一个简单的本地ChatPDF程序，支持上传多个pdf文件。使用的技术:LangChain, Streamlit。您可以替换您喜欢的任何LLM接口或嵌入接口

:snake: Python==3.9.0

<hr>

## Install
```
pip install -r requirements.txt
```

## Run
To modify your own.env file, you can modify the.env_example file and delete the suffix.

You need to add OPENAI_API_KEY and HUGGINGFACEHUB_API_TOKEN to the.env file

修改自己的.env文件， 可以修改.env_example文件然后删掉后缀。
你需要在.env文件中添加OPENAI_API_KEY和HUGGINGFACEHUB_API_TOKEN
.env:
```
OPENAI_API_KEY=...
HUGGINGFACEHUB_API_TOKEN=...

HTTPS_PROXY= socks5://127.0.0.1:7890   #国内用的化需要代理 clash默认端口7890 无需更改
```

Terminal：
```
streamlit run .\main.py
```


<hr>
## Reference
:point_right: Referenced this youtuber's video [Alejandro AO - Software & Ai](https://www.youtube.com/@alejandro_ao)
