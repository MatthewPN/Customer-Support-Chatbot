function do_ajax() {
    var req = new XMLHttpRequest();
    var result = document.getElementById('result');
    req.onreadystatechange = function()
    {
      if(this.readyState == 4 && this.status == 200) {
        result.innerHTML = this.responseText;
      } else {
        result.innerHTML = "処理中...";
      }
    }
    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("name=" + document.getElementById('name').value);
  }
