(function(){const el=document.getElementById('reader');if(!el)return;
const txt=JSON.parse(document.getElementById('bk').textContent),key=el.dataset.k,pages=[];
txt.split(/\n(?=# )/).forEach(ch=>{const m=ch.match(/^# (.*)\n?/),title=m?m[1]:'',body=m?ch.slice(m[0].length):ch;
 const ps=body.split(/\n\s*\n/).map(p=>p.trim()).filter(Boolean);let buf=[],len=0,first=true;
 const flush=()=>{pages.push({t:first?title:'',p:buf});buf=[];len=0;first=false};
 ps.forEach(p=>{if(len+p.length>1100&&buf.length)flush();buf.push(p);len+=p.length});if(buf.length||first)flush()});
let i=Math.min(+localStorage.getItem(key)||0,pages.length-1),fs=+localStorage.getItem('fs')||18;
const pg=document.getElementById('page');
function show(){pg.style.fontSize=fs+'px';pg.innerHTML='';const d=pages[i];
 if(d.t){const h=document.createElement('h2');h.textContent=d.t;pg.appendChild(h)}
 d.p.forEach(t=>{const p=document.createElement('p');p.textContent=t;pg.appendChild(p)});
 pg.classList.remove('flip');void pg.offsetWidth;pg.classList.add('flip');
 document.getElementById('pg').textContent='Page '+(i+1)+' / '+pages.length;
 document.getElementById('prog').style.width=((i+1)/pages.length*100)+'%';localStorage.setItem(key,i)}
const go=n=>{i=Math.max(0,Math.min(pages.length-1,i+n));show()};
document.getElementById('prev').onclick=()=>go(-1);document.getElementById('next').onclick=()=>go(1);
document.getElementById('fp').onclick=()=>{fs=Math.min(30,fs+2);localStorage.setItem('fs',fs);show()};
document.getElementById('fm').onclick=()=>{fs=Math.max(13,fs-2);localStorage.setItem('fs',fs);show()};
document.getElementById('rt').onclick=()=>el.classList.toggle('sepia');
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1)});show()})();