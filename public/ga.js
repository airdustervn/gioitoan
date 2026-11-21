/* Google Analytics 4 cho gioitoan.com.vn.
   Dán Mã đo lường (dạng G-XXXXXXXXXX) vào GA_ID bên dưới là chạy, không cần sửa chỗ khác.
   Chỉ chạy trên tên miền thật, không chạy khi xem thử trong Claude hay trên máy. */
(function(){
  var GA_ID = "";
  window.gt = function(){};
  if(!GA_ID || !/(^|\.)gioitoan\.com\.vn$/.test(location.hostname)) return;
  var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+GA_ID;document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};
  gtag("js",new Date());gtag("config",GA_ID,{anonymize_ip:true});
  window.gt=function(ev,p){try{gtag("event",ev,p||{});}catch(e){}};
  /* Trang chủ là 1 trang, đổi mục bằng #: gửi lượt xem trang cho từng mục */
  var last=location.hash;
  addEventListener("hashchange",function(){if(location.hash===last)return;last=location.hash;
    gtag("event","page_view",{page_location:location.href,page_path:location.pathname+location.hash,page_title:document.title});});
})();
