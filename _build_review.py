# Builds _theme_review.html: a review gallery of all card themes over their
# background art + palette, for sign-off. Render in a browser; auto-falls back
# to each theme's felt gradient when bg/<id>.jpg is missing.
src = open('index.html').read()
review = '''<div id="reviewWrap">
<style>
#reviewWrap{position:relative;z-index:99;background:#181d14;padding:26px 18px 44px;color:#eef3e6;font-family:-apple-system,system-ui,sans-serif}
.review h1{font-size:24px;text-align:center;margin:0 0 4px;font-family:Georgia,serif}
.review .sub{text-align:center;opacity:.65;margin-bottom:20px;font-size:13px}
.rrow{display:flex;align-items:center;gap:12px;margin-bottom:18px;padding:16px 14px;border-radius:14px;position:relative;overflow:hidden;
  background-size:cover;background-position:center;min-height:150px;background-color:#233022}
.rrow::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.30),rgba(0,0,0,.48));pointer-events:none}
.rrow>*{position:relative;z-index:1}
.rlabel{width:132px;flex:none;font-size:14px;font-weight:800;padding:6px 8px;border-radius:8px;background:rgba(0,0,0,.5)}
.rlabel small{display:block;font-weight:500;opacity:.75;font-size:11px;margin-top:2px}
.rcards{display:flex;gap:6px;flex-wrap:wrap}
.rcards .card{width:88px}
</style>
<div class="review"><h1>Theme Review</h1><div class="sub">All 13 ranks per theme, rendered over each theme's background art (felt gradient fallback)</div><div id="reviewRows"></div></div>
<script>
(function(){
  var t=window.__game.themes;
  var lk=window.__game.look||{};
  var ids=Object.keys(t);
  var suits=['S','H','C','D'];
  var ranks=['A','K','Q','J','10','9','8','7','6','5','4','3','2'];
  var html='';
  ids.forEach(function(id){
    if(!t[id])return;
    var L=lk[id]||{};
    var bg=L.bg||'';
    var felt=L.felt||['#2f9a6a','#0a3521'];
    html+='<div class="rrow" style="background-image:url('+bg+'),linear-gradient(180deg,'+felt[0]+','+felt[3]+')">';
    html+='<div class="rlabel" style="border-left:3px solid '+(L.accent||'#ffd24d')+'">'+t[id].name+'<small>'+t[id].sub+'</small></div><div class="rcards">';
    html+='<div class="card backcard" style="margin-right:8px">'+t[id].back()+'</div>';
    ranks.forEach(function(r,i){
      html+='<div class="card red">'+t[id].svg({r:r,s:suits[i%4]}).replace('alt=""','alt="" loading="lazy"')+'</div>';
    });
    html+='</div></div>';
  });
  document.getElementById('reviewRows').innerHTML=html;
  var app=document.querySelector('.app'); if(app) app.style.display='none';
  var c=document.getElementById('confetti'); if(c) c.style.display='none';
  var bgL=document.getElementById('bgLayer'); if(bgL) bgL.style.display='none';
  window.scrollTo(0,0);
})();
</script>
</div>'''
src = src.replace('</body>', review + '\n</body>')
open('_theme_review.html', 'w').write(src)
print('review page written')
