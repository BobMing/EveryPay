//判断输入值是否为空
function check() {
  if($('#content').val()==''){
    document.getElementById("content").style.borderColor = "#FF0000";
    return false;
  }

  document.getElementById("content").style.borderColor = "#BBB";

  price = $('#quote').val();
  if(price ==''){
    document.getElementById("quote").style.borderColor = "#FF0000";
    return false;
  } else {
    var partten = /^[1-9]d*.*d*|0.d*[1-9]d*|0?.0+|0$/;
    if(!partten.test(price)){
      document.getElementById("quote").style.borderColor = "#FF0000";
      alert('请输入正确的价格');
      return false;
    }
  }
  document.getElementById("quote").style.borderColor = "#BBB";

  if($('#place').val()==''){
    document.getElementById("place").style.borderColor = "#FF0000";
    return false;
  }
  document.getElementById("place").style.borderColor = "#BBB";
  return true;
}

var xmlhttp=null;
var userid = null;
var username = null;

//取消发布
function cancel() {
  userid=document.getElementById("userid").innerHTML;
  username=document.getElementById("username").innerHTML;
  window.location.href = "?page=request.html&userid="+userid+"&username="+username;
}

//发布成功
//跳转到发布成功页
function success() {
  if (!check()) {
    return;
  }

  var content=document.getElementById("content").value;
  var quote=document.getElementById("quote").value;
  var place=document.getElementById("place").value;
  userid=document.getElementById("userid").innerHTML;
  username=document.getElementById("username").innerHTML;

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
  xmlhttp.open("POST","http://everypay.sinaapp.com/",true);
  //POST方式需要自己设置http的请求头
  xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  //POST方式发送数据
  xmlhttp.send("userid="+userid+"&demand="+content+"&quote="+quote+"&destination="+place+"&action=rel");

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
              window.location.href = "?page=request.html&userid="+userid+"&username="+username;
            }
        }
    }
}

// vertical align box   
(function(elem){ 
  elem.css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( elem.height() / 2 ) ) );
}($(".informNeed-wrap")));

$(window).resize(function(){
  $(".informNeed-wrap").css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( $(".informNeed-wrap").height() / 2 ) ) );
  
});