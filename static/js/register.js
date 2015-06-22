// Login/Register form
// Author: Lingfeng Xu
//------------------------------------

function check() {
  if($('#username').val()==''){
    document.getElementById("username").style.borderColor = "#FF0000";
    return false;
  }
  document.getElementById("username").style.borderColor = "#BBB";

  if($('#password').val()==''){
    document.getElementById("password").style.borderColor = "#FF0000";
    return false;
  }
  document.getElementById("password").style.borderColor = "#BBB";

  if($('#repassword').val()==''){
    document.getElementById("repassword").style.borderColor = "#FF0000";
    return false;
  } else {
    if($('#password').val()!=$('#repassword').val()) {
      document.getElementById("repassword").style.borderColor = "#FF0000";
      alert('密码确认不一致');
      return false;
    }
  }
  document.getElementById("repassword").style.borderColor = "#BBB";

  var tel = $('#telephone').val()

  if(tel ==''){
    document.getElementById("telephone").style.borderColor = "#FF0000";
    return false;
  } else {
    var partten =/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
    if(!partten.test(tel)){
      document.getElementById("telephone").style.borderColor = "#FF0000";
      alert('请输入合法手机号码');
      return false;
    }
  }
  document.getElementById("telephone").style.borderColor = "#BBB";
  return true;
}

var xmlhttp=null;

// 判断用户名是否重复
function checkuser() {
  var userName=document.getElementById("username").value;

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

  //注册回调函数。注意注册回调函数是不能加括号,加了会把函数的值返回给onreadystatechange
  xmlhttp.onreadystatechange=callback;

  //设置连接信息
  //第一个参数表示http请求方式,支持所有http的请求方式,主要使用get和post
  //第二个参数表示请求的url地址,get方式请求的参数也在urlKh
  //第三介参数表示采用异步还是同步方式交互,true表示异步
  
  //异步方式下,send这句话立即完成执行
  //POST方式请求的代码
  xmlhttp.open("POST","http://everypay.sinaapp.com",true);
  //POST方式需要自己设置http的请求头
  xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  //POST方式发送数据
  xmlhttp.send("username="+userName+"&action=usr");

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
            if (obj['status'] == 'failure') {
              document.getElementById ("ximg").style.display = "inline";
            } else {
              document.getElementById ("ximg").style.display = "none";
            }
        }
    }
}

// vertical align box   
(function(elem){ 
  elem.css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( elem.height() / 2 ) ) );
}($(".register-wrap")));

$(window).resize(function(){
  $(".register-wrap").css("margin-top", Math.floor( ( $(window).height() / 2 ) - ( $(".register-wrap").height() / 2 ) ) );
  
});

