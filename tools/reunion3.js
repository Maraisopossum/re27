(function(){
  var chips=document.querySelectorAll('.chip[data-f]');
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.classList.remove('on')});c.classList.add('on');
    var f=c.getAttribute('data-f');
    document.querySelectorAll('.day').forEach(function(d){d.hidden=!(f==='all'||d.getAttribute('data-p')===f)});
  })});
  var opened=false,btn=document.getElementById('openall');
  btn.addEventListener('click',function(){opened=!opened;
    document.querySelectorAll('.day').forEach(function(d){d.open=opened});
    btn.textContent=opened?'Tout replier':'Tout déplier';
  });
  var omap=document.getElementById('omap'),dcs=document.querySelectorAll('.dc'),cur=null;
  function hl(n){
    cur=(cur===n)?null:n;
    omap.classList.toggle('hl',cur!==null);
    omap.querySelectorAll('.rg').forEach(function(g){g.classList.toggle('on',cur!==null&&g.getAttribute('data-d')===String(cur))});
    dcs.forEach(function(b){b.classList.toggle('on',cur!==null&&b.getAttribute('data-d')===String(cur))});
  }
  dcs.forEach(function(b){b.addEventListener('click',function(){hl(b.getAttribute('data-d'))})});
  omap.querySelectorAll('.rg').forEach(function(g){g.addEventListener('click',function(){
    var n=g.getAttribute('data-d');hl(n);var t=document.getElementById('j'+n);if(t){t.open=true}
  })});
  var pick=document.getElementById('farepick');
  function fmt(v){return Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g,' ')+' €'}
  function upd(){var f=parseFloat(pick.value);document.getElementById('farev').textContent=fmt(f);document.getElementById('total').textContent=fmt(f+BASE)}
  pick.value=pick.options[1].value;pick.addEventListener('change',upd);upd();
  if(location.hash){try{var t=document.querySelector(location.hash);if(t&&t.tagName==='DETAILS')t.open=true}catch(e){}}
})();
