(function(){
'use strict';
var d=document,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.remove('no-js');d.documentElement.classList.add('js');

/* header + progress rule */
var head=$('.head'),bar=$('.progress');
function onScroll(){
  var y=window.pageYOffset,h=d.documentElement.scrollHeight-window.innerHeight;
  if(head)head.classList.toggle('scrolled',y>8);
  if(bar)bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
  lightWords();
}
window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll);

/* hero + page-hero intro */
var intro=$('.hero')||$('.phero');
if(intro){requestAnimationFrame(function(){requestAnimationFrame(function(){intro.classList.add('go')})})}

/* hero spotlight on the ruled paper */
var hero=$('.hero');
if(hero&&!reduce){
  hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--mx',(e.clientX-r.left)+'px');hero.style.setProperty('--my',(e.clientY-r.top)+'px')});
  var t0=null;function drift(t){if(!t0)t0=t;if(!hero.matches(':hover')){var r=hero.getBoundingClientRect();hero.style.setProperty('--mx',(r.width*(.62+.18*Math.sin((t-t0)/2600)))+'px');hero.style.setProperty('--my',(r.height*(.42+.2*Math.cos((t-t0)/3300)))+'px')}requestAnimationFrame(drift)}
  requestAnimationFrame(drift);
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
function lightWords(){
  if(!words.length)return;
  if(reduce){words.forEach(function(w){w.classList.add('lit')});return}
  var r=gap.getBoundingClientRect(),vh=window.innerHeight;
  var p=(vh*.92-r.top)/(r.height+vh*.22);if(r.bottom<vh*.75)p=1;p=Math.max(0,Math.min(1,p));
  var n=Math.round(p*words.length);
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
    form.hidden=true;$('.done',dlg).hidden=false;
  });
}else{
  $$('[data-counsel]').forEach(function(b){b.setAttribute('href','#counsel-fallback')});
}
onScroll();
})();
