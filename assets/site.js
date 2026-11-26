(function(){
'use strict';
var d=document,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.remove('no-js');d.documentElement.classList.add('js');

/* header + progress rule: scroll work runs at most once per frame, reads first, then writes */
var head=$('.head'),bar=$('.progress'),scrolled=null,ticking=false;
var cssBar=!reduce&&window.CSS&&CSS.supports&&CSS.supports('(animation-timeline:scroll()) and (animation-range:0% 100%)');
function update(){
  ticking=false;
  var y=window.pageYOffset,h=d.documentElement.scrollHeight-window.innerHeight,s=y>8;
  var gr=words.length&&!reduce?gap.getBoundingClientRect():null,vh=window.innerHeight;
  if(head&&s!==scrolled){head.classList.toggle('scrolled',s);scrolled=s}
  if(bar&&!cssBar)bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
  lightWords(gr,vh);
}
function onScroll(){if(!ticking){ticking=true;requestAnimationFrame(update)}}
window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll);

/* hero + page-hero intro */
var intro=$('.hero')||$('.phero');
if(intro){requestAnimationFrame(function(){requestAnimationFrame(function(){intro.classList.add('go')})})}

/* hero spotlight on the ruled paper: moved with transform only, paused when the hero is off screen */
var hero=$('.hero'),lit=$('.hero__lit'),litIn=lit&&lit.firstElementChild;
if(hero&&litIn){
  var R=280,P=52,W=0,H=0,mx=0,my=0,over=false,vis=true,raf=0,t0=null;
  /* P = line spacing (--rl); the inner layer is 560px + P tall, so P is read back from its height */
  var size=function(){W=hero.clientWidth;H=hero.clientHeight;P=parseFloat(getComputedStyle(litIn).height)-2*R||52};
  var place=function(x,y){var bx=Math.round(x-R),by=Math.round(y-R),ph=((by%P)+P)%P;
    lit.style.transform='translate3d('+bx+'px,'+by+'px,0)';litIn.style.transform='translate3d(0,'+(-ph).toFixed(2)+'px,0)'};
  var frame=function(t){raf=0;if(!t0)t0=t;
    if(!over){mx=W*(.62+.18*Math.sin((t-t0)/2600));my=H*(.42+.2*Math.cos((t-t0)/3300))}
    place(mx,my);if(vis&&!over)raf=requestAnimationFrame(frame)};
  var kick=function(){if(!raf&&vis&&!reduce)raf=requestAnimationFrame(frame)};
  size();place(W*.7,H*.35);
  window.addEventListener('resize',function(){size();if(reduce)place(W*.7,H*.35)});
  if(!reduce){
    hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top;over=true;
      if(!raf)raf=requestAnimationFrame(function(){raf=0;place(mx,my)})});
    hero.addEventListener('pointerleave',function(){over=false;kick()});
    if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting;kick()}).observe(hero);
    kick();
  }
}

/* reveal on scroll */
var io='IntersectionObserver' in window&&!reduce?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'}):null;
$$('[data-r],.steps__grid').forEach(function(el){io?io.observe(el):el.classList.add('in')});

/* words light up as the paragraph passes through the viewport */
var gap=$('.gap__t'),words=[];
if(gap){
  var txt=gap.textContent.trim().split(/\s+/);gap.setAttribute('aria-label',gap.textContent.trim());
  gap.innerHTML=txt.map(function(w){return '<span class="w" aria-hidden="true">'+w+'</span>'}).join(' ');
  words=$$('.w',gap);
}
var litN=-1;
function lightWords(r,vh){
  if(!words.length)return;
  if(reduce){if(litN<0){words.forEach(function(w){w.classList.add('lit')});litN=words.length}return}
  var p=(vh*.92-r.top)/(r.height+vh*.22);if(r.bottom<vh*.75)p=1;p=Math.max(0,Math.min(1,p));
  var n=Math.round(p*words.length);
  if(n===litN)return;litN=n;
  words.forEach(function(w,i){w.classList.toggle('lit',i<n)});
}

/* scroll-spy on the six tasks */
var tasks=$$('.tasks li'),nowN=$('#nowN'),nowT=$('#nowT');
if(tasks.length&&'IntersectionObserver' in window){
  var spy=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
    tasks.forEach(function(t){t.classList.remove('on')});e.target.classList.add('on');
    if(nowN){nowN.firstChild.nodeValue=e.target.getAttribute('data-n')}
    if(nowT){nowT.textContent=e.target.getAttribute('data-t')}
  }})},{rootMargin:'-42% 0px -48% 0px'});
  tasks.forEach(function(t){spy.observe(t)});
}else{tasks.forEach(function(t){t.classList.add('on')})}

/* count-up for the figures */
var nums=$$('[data-count]');
function rs(x){return x.replace('₹','<span class="rs">₹</span>')}
function fmt(n){return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g,',')}
if(nums.length){
  var co='IntersectionObserver' in window&&!reduce?new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);
    var el=e.target,to=+el.getAttribute('data-count'),pre=el.getAttribute('data-pre')||'',suf=el.getAttribute('data-suf')||'',t0=null;
    function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1100),v=Math.round(to*(1-Math.pow(1-p,3)));el.innerHTML=rs(pre)+fmt(v)+suf;if(p<1)requestAnimationFrame(f)}
    requestAnimationFrame(f)})},{threshold:.6}):null;
  nums.forEach(function(el){if(co){var to=+el.getAttribute('data-count');el.innerHTML=rs(el.getAttribute('data-pre')||'')+'0'+(el.getAttribute('data-suf')||'');co.observe(el)}})
}

/* mobile menu */
var menu=$('#menu'),ob=$('#menuOpen');
function closeMenu(){if(!menu)return;menu.classList.remove('open');menu.setAttribute('aria-hidden','true');ob.setAttribute('aria-expanded','false');d.body.style.overflow=''}
if(menu&&ob){
  ob.addEventListener('click',function(){menu.classList.add('open');menu.setAttribute('aria-hidden','false');ob.setAttribute('aria-expanded','true');d.body.style.overflow='hidden';$('#menuX').focus()});
  $('#menuX').addEventListener('click',function(){closeMenu();ob.focus()});
  $$('a',menu).forEach(function(a){a.addEventListener('click',closeMenu)});
  d.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu()});
}

/* counselling dialog (preview: not connected to any lead system) */
var dlg=$('#counsel');
if(dlg&&typeof dlg.showModal==='function'){
  $$('[data-counsel]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();closeMenu();dlg.showModal()})});
  $$('[data-close]',dlg).forEach(function(b){b.addEventListener('click',function(){dlg.close()})});
  dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
  var form=$('form',dlg),err=$('.err',dlg);
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=form.elements.fullname.value.trim().length>1&&/^[+0-9 ()-]{8,16}$/.test(form.elements.mobile.value.trim())&&form.elements.who.value&&form.elements.consent.checked;
    if(!ok){err.textContent='Please fill in the marked fields and tick the consent box.';return}
    var ep=form.getAttribute('data-endpoint'),doneMsg=$('.done .s',dlg);
    if(!ep){form.hidden=true;$('.done',dlg).hidden=false;return}
    var q=new URLSearchParams(location.search),btn=$('button[type=submit]',form);
    var data={name:form.elements.fullname.value.trim(),mobile:form.elements.mobile.value.trim(),who:form.elements.who.value,language:form.elements.lang.value,consent:'yes',page:location.href,source:q.get('utm_source')||'',medium:q.get('utm_medium')||'',campaign:q.get('utm_campaign')||'',time:new Date().toISOString()};
    btn.disabled=true;err.textContent='';
    fetch(ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(function(r){return r.json()}).then(function(j){
      if(!j.ok)throw new Error('rejected');
      doneMsg.textContent=j.delivered?'A counsellor will call or WhatsApp you shortly, in English or Malayalam.':'Preview: the lead system is not connected yet, so nothing was sent.';
      form.hidden=true;$('.done',dlg).hidden=false;
    }).catch(function(){btn.disabled=false;err.textContent='Could not send. Please try again.'});
  });
  /* ad links: /book, ?book or #book open the form straight away */
  if(/^\/book\/?$/.test(location.pathname)||/(^|[?&#])book(=|&|$)/.test(location.search+location.hash)){dlg.showModal()}
}else{
  $$('[data-counsel]').forEach(function(b){b.setAttribute('href','#counsel-fallback')});
}
/* AI voice assistant (ElevenLabs): the widget script loads only after a click */
$$('[data-voice]').forEach(function(b){b.addEventListener('click',function(){
  if(dlg&&dlg.open)dlg.close();
  if(!$('elevenlabs-convai')){
    var w=d.createElement('elevenlabs-convai');w.setAttribute('agent-id',b.getAttribute('data-voice'));d.body.appendChild(w);
    var s=d.createElement('script');s.src='https://unpkg.com/@elevenlabs/convai-widget-embed';s.async=true;d.head.appendChild(s);
  }
  d.body.classList.add('voice-on');
  /* one click = one call: press the widget's own "Start a call" once it has loaded */
  var n=0,t=setInterval(function(){
    var w=$('elevenlabs-convai'),sr=w&&w.shadowRoot,go=sr&&sr.querySelector('button[aria-label="Start a call"]');
    if(go){clearInterval(t);go.click()}else if(++n>50)clearInterval(t);
  },200);
  $$('.talk [data-voice]').forEach(function(x){x.textContent='Assistant ready, bottom right of the screen'});
})});
update();
})();
