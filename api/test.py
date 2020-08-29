import js2py

code = 'function gay(){ fetch("http://127.0.0.1:8000/download/12/").then(response => response.blob()).then(function(myBlob) {const objectURL = URL.createObjectURL(myBlob); console.log(objectURL);});}'
y=js2py.eval_js6(code)

y()