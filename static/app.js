(function(){var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;})();
const MONTHS=['Meskerem','Tikimt','Hidar','Tahsas','Tir','Yekatit','Megabit','Miazia','Ginbot','Sene','Hamle','Nehase','Pagume'];
function ethDate(d){const jdn=Math.floor(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/864e5)+2440588,e=1723856,r=(jdn-e)%1461,n=r%365+365*Math.floor(r/1460);
 return{y:4*Math.floor((jdn-e)/1461)+Math.floor(r/365)-Math.floor(r/1460),m:Math.floor(n/30),d:n%30+1}}
document.addEventListener('DOMContentLoaded',()=>{
 const $=s=>document.querySelector(s),$$=s=>document.querySelectorAll(s);
 $('#theme').onclick=()=>{const d=document.documentElement,n=d.dataset.theme==='dark'?'light':'dark';d.dataset.theme=n;localStorage.setItem('theme',n)};
 $('#burger').onclick=()=>$('#links').classList.toggle('open');
 const e=ethDate(new Date()),txt=MONTHS[e.m]+' '+e.d+', '+e.y+' E.C.';
 if($('#ethdate'))$('#ethdate').textContent=txt;$('#ethnow').textContent='Ethiopian date: '+txt;
 const q=$('#q'),dl=$('#sug');let tm;
 q.addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(async()=>{try{const r=await(await fetch('/api/suggest?q='+encodeURIComponent(q.value))).json();dl.innerHTML=r.map(x=>'<option value="'+x.replace(/"/g,'&quot;')+'">').join('')}catch(e){}},200)});
 const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.12});
 $$('.rv').forEach(x=>io.observe(x));
 $$('[data-n]').forEach(el=>{const t=+el.dataset.n;let c=0;const s=Math.max(1,Math.ceil(t/40));const iv=setInterval(()=>{c=Math.min(t,c+s);el.textContent=c;if(c>=t)clearInterval(iv)},30)});
 const f=$('#facts');if(f){const a=JSON.parse(f.dataset.f);let i=0;const show=()=>{f.style.opacity=0;setTimeout(()=>{f.textContent='💡 '+a[i++%a.length];f.style.opacity=1},400)};show();setInterval(show,4500)}
 const rf=$('#rf');if(rf)rf.oninput=()=>$$('#rgrid .card').forEach(c=>c.style.display=c.dataset.s.includes(rf.value.toLowerCase())?'':'none');
 $$('[data-tabs]').forEach(w=>w.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{w.querySelectorAll('.tabs button,.pane').forEach(x=>x.classList.remove('on'));b.classList.add('on');w.querySelector('[data-p="'+b.dataset.t+'"]').classList.add('on')}));
 const up=$('#up');onscroll=()=>up.classList.toggle('show',scrollY>500);up.onclick=()=>scrollTo({top:0,behavior:'smooth'});
 $$('.wiki').forEach(async el=>{if(document.documentElement.dataset.lite){el.remove();return}try{const s=await(await fetch('https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&format=json&origin=*&srsearch='+encodeURIComponent(el.dataset.q))).json();
  const d=await(await fetch('https://en.wikipedia.org/api/rest_v1/page/summary/'+encodeURIComponent(s.query.search[0].title))).json();
  const esc=x=>String(x).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  el.innerHTML=(d.thumbnail?'<img src="'+d.thumbnail.source+'" alt="">':'')+'<div><h3>🌐 '+esc(d.title)+' <small>live from Wikipedia (CC BY-SA)</small></h3><p>'+esc(d.extract)+'</p><a class="btn small" target="_blank" rel="noopener" href="'+d.content_urls.desktop.page+'">Read more</a></div>'}catch(e){el.innerHTML='<p class="empty">Online info unavailable (check internet connection).</p>'}});
});
document.addEventListener('DOMContentLoaded',()=>{const g=document.getElementById('gd');if(g)g.onchange=()=>{const d=new Date(g.value+'T00:00:00'),e=ethDate(d);document.getElementById('ge').textContent=MONTHS[e.m]+' '+e.d+', '+e.y+' E.C.'}});

document.addEventListener('DOMContentLoaded',()=>{
 if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
 const sp=document.createElement('div');sp.id='sp';document.body.appendChild(sp);addEventListener('scroll',()=>{sp.style.width=(scrollY/Math.max(1,document.body.scrollHeight-innerHeight)*100)+'%'});
 const get=()=>JSON.parse(localStorage.getItem('favs')||'[]');
 document.querySelectorAll('.fav').forEach(b=>{const id=+b.dataset.id,sync=()=>{const on=get().includes(id);b.textContent=on?'♥':'♡';b.classList.toggle('on',on)};sync();
  b.onclick=e=>{e.preventDefault();e.stopPropagation();let a=get();a=a.includes(id)?a.filter(x=>x!=id):[...a,id];localStorage.setItem('favs',JSON.stringify(a));sync()}});
 const pal=document.getElementById('palette'),pi=document.getElementById('pi'),pr=document.getElementById('pr');let pt;
 const link=(t,u,k)=>{const a=document.createElement('a');a.href=u;a.textContent=t;const s=document.createElement('small');s.textContent=k;a.appendChild(s);return a};
 const quick=()=>{pr.innerHTML='';[['Library','/library','Page'],['Know Ethiopia','/know','Page'],['Festivals','/events','Page'],['Trip planner','/planner','Page'],['Quiz','/quiz','Page']].forEach(x=>pr.appendChild(link(...x)))};
 const open=()=>{pal.hidden=false;pi.value='';quick();pi.focus()},close=()=>{pal.hidden=true};
 document.getElementById('pal').onclick=open;pal.onclick=e=>{if(e.target===pal)close()};
 addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();open()}if(e.key==='Escape')close();if(e.key==='Enter'&&!pal.hidden){const a=pr.querySelector('a');if(a)location.href=a.href}});
 pi.oninput=()=>{clearTimeout(pt);pt=setTimeout(async()=>{if(pi.value.length<2){quick();return}try{const r=await(await fetch('/api/search?q='+encodeURIComponent(pi.value))).json();pr.innerHTML='';if(!r.length)pr.innerHTML='<p class="empty" style="padding:10px">No matches</p>';r.forEach(x=>pr.appendChild(link(x.t,x.u,x.k)))}catch(e){}},180)};
});(function(){try{const a=JSON.parse(localStorage.getItem('a11y')||'{}'),h=document.documentElement;if(a.fs)h.style.fontSize=a.fs+'%';if(a.hc)h.dataset.contrast='high';if(a.lite)h.dataset.lite='1'}catch(e){}})();
document.addEventListener('DOMContentLoaded',()=>{
 const tok=document.querySelector('meta[name=csrf]').content;
 document.querySelectorAll('form').forEach(f=>{if(f.method.toLowerCase()==='post'){const i=document.createElement('input');i.type='hidden';i.name='_csrf';i.value=tok;f.appendChild(i)}});
 const h=document.documentElement,P=document.getElementById('a11yp'),get=()=>JSON.parse(localStorage.getItem('a11y')||'{}'),put=a=>localStorage.setItem('a11y',JSON.stringify(a));
 document.getElementById('a11y').onclick=()=>P.hidden=!P.hidden;
 const fs=d=>{const a=get();a.fs=Math.max(80,Math.min(150,(a.fs||100)+d));put(a);h.style.fontSize=a.fs+'%'};
 document.getElementById('tp').onclick=()=>fs(10);document.getElementById('tm').onclick=()=>fs(-10);
 document.getElementById('hc').onclick=()=>{const a=get();a.hc=!a.hc;put(a);a.hc?h.dataset.contrast='high':delete h.dataset.contrast};
 document.getElementById('lt').onclick=()=>{const a=get();a.lite=!a.lite;put(a);location.reload()};
 const mic=document.getElementById('mic'),SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR)mic.style.display='none';else mic.onclick=()=>{const r=new SR();r.lang=h.lang==='am'?'am-ET':'en-US';r.onresult=e=>{const pi=document.getElementById('pi');pi.value=e.results[0][0].transcript;pi.dispatchEvent(new Event('input'))};r.start()};
 const W={0:'Clear',1:'Mostly clear',2:'Partly cloudy',3:'Cloudy',45:'Fog',48:'Fog',51:'Drizzle',53:'Drizzle',55:'Drizzle',61:'Rain',63:'Rain',65:'Heavy rain',80:'Showers',81:'Showers',82:'Heavy showers',95:'Thunderstorm',96:'Thunderstorm',99:'Thunderstorm'};
 document.querySelectorAll('.weather').forEach(async el=>{if(h.dataset.lite){el.remove();return}try{const r=await(await fetch('https://api.open-meteo.com/v1/forecast?current_weather=true&latitude='+el.dataset.lat+'&longitude='+el.dataset.lng)).json(),c=r.current_weather;
  el.textContent='🌦 Now: '+Math.round(c.temperature)+'°C · '+(W[c.weathercode]||'—')+' · wind '+Math.round(c.windspeed)+' km/h  (Open-Meteo)'}catch(e){el.textContent='Weather unavailable (needs internet).'}});
});
