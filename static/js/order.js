
function pagechange(num) {
  var user = document.getElementById('user').innerHTML;
  var lastIndex = user.indexOf(")");
  var startIndex = user.indexOf("(") + 1;
  var userid = user.substring(startIndex, lastIndex);
  var username = user.substring(0, startIndex-1);
  switch (num) {
    case 0:
      window.location.href = "?page=demandpool.html&username="+username+"&userid="+userid;
      break;
    case 1:
      window.location.href = "?page=request.html&username="+username+"&userid="+userid;
      break;
    case 2:
      window.location.href = "?page=service.html&username="+username+"&userid="+userid;
      break;
    case 3:
      window.location.href = "?page=release.html&username="+username+"&userid="+userid;
      break;
  }
}

var xmlhttp=null;

// 提交表单，登录
function recieveOrder(obj) {
  var user = document.getElementById('user').innerHTML;
  var lastIndex = user.indexOf(")");
  var startIndex = user.indexOf("(") + 1;
  var userid = user.substring(startIndex, lastIndex);
  var index = obj.id.substring(3);
  var orderid = document.getElementById('orderid'+index).innerHTML;
  
  //1、创建XMLHttpRequest对象
  //2、需要针对IE和其它浏览器建立这个对象的不同方式写不同的代码
  if(window.XMLHttpRequest){
      //针对FF,Mozilar,Opera,Safari,IE7,IE8
      xmlhttp=new XMLHttpRequest();
      //修正某些浏览器bug
      if(xmlhttp.overrideMimeType){
          xmlhttp.overrideMimeType("text/xml");
      }
  }else if(window.ActiveXObject){
      //针对IE6以下的浏览器
      var activexName=["MSXML2.XMLHTTP","Microsoft.XMLHTTP",""];
      for( var i=0;i<activexName.length;i++){
          try{
              //取出一个控件名称创建,如果创建成功则停止,反之抛出异常
              xmlhttp=new ActiveXObject(activexName[i]);
              break;                
          }catch(e){    }
      }
  }

  //设置连接信息
  //第一个参数表示http请求方式,支持所有http的请求方式,主要使用get和post
  //第二个参数表示请求的url地址,get方式请求的参数也在urlKh
  //第三介参数表示采用异步还是同步方式交互,true表示异步
  
  //异步方式下,send这句话立即完成执行
  //POST方式请求的代码
  xmlhttp.open("POST","http://everypay.sinaapp.com/", true);
  //POST方式需要自己设置http的请求头
  xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  //POST方式发送数据

  xmlhttp.send("action=rco&userid=" + userid + "&orderid=" + orderid);
    
  //注册回调函数。注意注册回调函数是不能加括号,加了会把函数的值返回给onreadystatechange
  xmlhttp.onreadystatechange=callback;

}

//回调函数
function callback() {
    //判断对象的状态是交互完成
    if (xmlhttp.readyState == 4) {
        //判断http的交互是否成功
        if (xmlhttp.status == 200) {
            //获取服务器端返回的数据
            //获取服务器端输出的纯文本数据
            var responseText = xmlhttp.responseText;
            var lastIndex = responseText.indexOf("\n");
            var jsonstr = responseText.substring(0, lastIndex);
            var obj = eval("("+jsonstr+")");
            if (obj['status'] == 'success') {
              pagechange(0);
            }
        }
    }
}

$(function () {
  var i = 0;
  $(".item dl dt b").each(function () {
      $(this).attr('id','orderid'+i);
      i++;
  });
});

$(function () {
  var i = 0;
  $(".item dl dt button").each(function () {  
      $(this).attr('id','rco'+i);
      i++;
  });
}); 


