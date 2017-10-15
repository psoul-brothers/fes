$(document).ready(function(){
  /* メニューのサブメニュー
  http://techmemo.biz/javascript/acordionmenu/ */
  $(".submenu").css("display","none");
  $(".trigger").click(function(){
    $(".submenu").slideUp("normal"); //一度消す
    
    if($("+.submenu",this).css("display")=="none"){
      $(this).addClass("active-submenu");
      $(this).removeClass("none-submenu");
      $("+.submenu",this).slideDown("normal");
    }else{
      $(this).removeClass("active-submenu");
      $(this).addClass("none-submenu");
      $("+.submenu",this).slideUp("normal");
    }
  });

  /* ヘッダーがスクロールで出たり消えたり
  http://weboook.blog22.fc2.com/blog-entry-412.html */
  var menuHeight = $("#menu-wrap").height();
  var startPos = 0;
  $("header").css("padding-bottom", + menuHeight + "px");
  $(window).scroll(function(){
    var currentPos = $(this).scrollTop();
    if (currentPos > startPos) {
      if($(window).scrollTop() >= 200) {
        $("#menu-wrap").css("top", "-" + menuHeight + "px");
      }
    } else {
      $("#menu-wrap").css("top", 0 + "px");
    }
    startPos = currentPos;
  });
});
