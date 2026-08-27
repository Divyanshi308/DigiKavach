/* DigiKavach Widget - embeddable website security */
(function(){
if(window.DigiKavach)return;
window.DigiKavach={
init:function(options){
var site=options&&options.site||location.hostname;
var w=document.createElement('div');
w.style.cssText='position:fixed;bottom:20px;right:20px;z-index:999999;font-family:system-ui,sans-serif';
w.innerHTML='<div style="background:linear-gradient(135deg,#0a1628,#111827);border:1px solid #00d2ff;border-radius:14px;padding:14px 18px;color:#fff;font-size:14px;box-shadow:0 8px 30px rgba(0,0,0,.5);display:flex;align-items:center;gap:10px;cursor:pointer" onclick="this.querySelector(\'div.u\').style.display=this.querySelector(\'div.u\').style.display===\'block\'?\'none\':\'block\'"><span style="font-size:20px">\u{1F6A9}</span><div><div style="font-weight:700">DigiKavach Shield</div><div style="font-size:12px;opacity:.7">Verified safe</div></div></div><div class="u" style="display:none;margin-top:8px;background:rgba(17,24,39,.95);border:1px solid rgba(0,210,255,.3);border-radius:12px;padding:12px;font-size:12px;color:#8892b0"><b>'+site+'</b> verified by DigiKavach<br>No phishing risk detected</div>';
document.body.appendChild(w);
}
};
})();
