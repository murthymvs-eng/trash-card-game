# Builds _theme_review.html: a review gallery of all card themes, for sign-off.
src = open('index.html').read()
review = '''<div id="reviewWrap">
<style>
#reviewWrap{position:relative;z-index:99;background:#20281f;padding:26px 18px 44px;color:#eef3e6;font-family:-apple-system,system-ui,sans-serif}
.review h1{font-size:24px;text-align:center;margin:0 0 4px;font-family:Georgia,serif}
.review .sub{text-align:center;opacity:.65;margin-bottom:20px;font-size:13px}
.rrow{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.rlabel{width:132px;flex:none;font-size:14px;font-weight:800}
.rlabel small{display:block;font-weight:500;opacity:.6;font-size:11px;margin-top:2px}
.rcards{display:flex;gap:6px;flex-wrap:wrap}
.rcards .card{width:108px}
</style>
<div class="review"><h1>Card Theme Review</h1><div class="sub">All 13 ranks in each theme - suits rotate spade/heart/club/diamond</div><div id="reviewRows"></div></div>
<script>
(function(){
  var t=window.__game.themes;
  var ids=Object.keys(t);
  var suits=['S','H','C','D'];
  var ranks=['A','K','Q','J','10','9','8','7','6','5','4','3','2'];
  var html='';
  ids.forEach(function(id){
    if(!t[id])return;
    html+='<div class="rrow"><div class="rlabel">'+t[id].name+'<small>'+t[id].sub+'</small></div><div class="rcards">';
    html+='<div class="card backcard" style="margin-right:8px">'+t[id].back()+'</div>';
    ranks.forEach(function(r,i){
      html+='<div class="card red">'+t[id].svg({r:r,s:suits[i%4]}).replace('alt=""','alt="" loading="lazy"')+'</div>';
    });
    html+='</div></div>';
  });
  document.getElementById('reviewRows').innerHTML=html;
  var app=document.querySelector('.app'); if(app) app.style.display='none';
  var c=document.getElementById('confetti'); if(c) c.style.display='none';
  window.scrollTo(0,0);
})();
</script>
</div>'''
src = src.replace('</body>', review + '\n</body>')
open('_theme_review.html', 'w').write(src)
print('review page written')