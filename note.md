# 开发笔记
采用采用http://50fedf6c.tunnel.qydev.com/sanchi完全正常

bokeh serve  sanchi --host 50fedf6c.tunnel.qydev.com --port 5100

而nginx 浏览器端则会出现bokeh.min.js:6 Uncaught SyntaxError: Invalid or unexpected token,猜测是静态文件处理问题


### 部署
https://github.com/bokeh/demo.bokehplots.com

### 静态文件位置
bokeh info --static

/home/wwj/sanchi/env/local/lib/python2.7/site-packages/bokeh/server/static

#### 复制静态文件给nginx用
cp -r `bokeh info --static` /home/wwj/sanchi/static


location /apps/static {
	        alias /home/wwj/sanchi/static;
}


# 改title
~/sanchi/env/lib/python2.7/site-packages/bokeh/embed.py

# WebSocket connection closed
WebSocket connection closed: code=1002, reason=u'Invalid UTF-8 in text frame'

http://blog.fgribreau.com/2012/05/how-to-fix-could-not-decode-text-frame.html

后端往前端扔了无效字符串

# 什么问题
Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

http://stackoverflow.com/questions/18193305/python-unicode-equal-comparison-failed