(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
    document.addEventListener('click',function(e){if(!n.contains(e.target)&&!t.contains(e.target)&&n.classList.contains('open')){n.classList.remove('open');t.setAttribute('aria-expanded','false');}});}
  document.querySelectorAll('.compare').forEach(function(c){
    var r=c.querySelector('.cmp-range'), active=false;
    function setPct(p){p=Math.max(0,Math.min(100,p));c.style.setProperty('--pos',p+'%');if(r)r.value=Math.round(p);}
    function pct(e){var b=c.getBoundingClientRect();return (e.clientX-b.left)/b.width*100;}
    c.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&e.button!==0)return;active=true;c.classList.add('dragging');try{c.setPointerCapture(e.pointerId);}catch(x){}setPct(pct(e));e.preventDefault();});
    c.addEventListener('pointermove',function(e){if(!active)return;setPct(pct(e));e.preventDefault();});
    function end(){active=false;c.classList.remove('dragging');}
    c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);c.addEventListener('lostpointercapture',end);
    if(r){r.addEventListener('input',function(){setPct(+r.value);});}
    setPct(50);
  });
  var f=document.getElementById('booking');
  if(!f)return;
  var WA='33647271062', MAIL='nadifa.proprete@gmail.com';
  function v(id){var el=document.getElementById(id);return el?el.value.trim():'';}
  function build(){
    var d=v('f-date'), dd='';
    if(d){var p=d.split('-');dd=p.length===3?(p[2]+'/'+p[1]+'/'+p[0]):d;}
    return 'Bonjour Nadifa Propreté, je souhaite réserver une intervention.\n'
      +'• Nom : '+v('f-name')+'\n'
      +'• Téléphone : '+v('f-phone')+'\n'
      +'• Prestation : '+v('f-service')+'\n'
      +(v('f-city')?'• Lieu : '+v('f-city')+'\n':'')
      +(dd?'• Date souhaitée : '+dd+'\n':'')
      +(v('f-msg')?'• Précisions : '+v('f-msg')+'\n':'')
      +'Merci de me confirmer le tarif et un créneau.';
  }
  var m=document.getElementById('mail-fallback');
  function syncMail(){ if(m){m.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Demande de nettoyage – '+(v('f-service')||'devis'))+'&body='+encodeURIComponent(build());} }
  f.addEventListener('input',syncMail); syncMail();
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=true, err=document.getElementById('form-error');
    ['f-name','f-phone','f-service'].forEach(function(id){var el=document.getElementById(id);var bad=!el.value.trim();el.setAttribute('aria-invalid',bad?'true':'false');if(bad)ok=false;});
    if(!ok){err.hidden=false;return;}
    err.hidden=true;
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(build()),'_blank','noopener');
  });
})();
