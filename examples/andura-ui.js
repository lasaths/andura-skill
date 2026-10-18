/* ANDURA example UI behaviour, shared by every examples/*.html. Load right after <body>.
   ?state= sets body[data-state]; ?scale= sets --s (OS text size); [data-for] gets aria-current; .trunc gets a title (peek);
   .hold = 1500 ms hold-to-acknowledge; confirmAck() opens the #ack confirm dialog (focus on CANCEL).
   States where the 09:54 alarms are still active get body[data-alarms]; [data-stale-in~=<state>] gets .stale (greyed + data age). */
const q=new URLSearchParams(location.search);if(q.get('state'))document.body.dataset.state=q.get('state');
if(q.get('mode'))document.documentElement.dataset.anduraMode=q.get('mode'); /* ?mode=sunlit: high-contrast light mode (colour.md §9) */
{const st=document.body.dataset.state;if(['alarm','detail','stale','comms','offline','flood'].includes(st))document.body.dataset.alarms='';}
if(q.get('scale')){document.documentElement.style.setProperty('--s',q.get('scale'));if(+q.get('scale')>=1.25)document.documentElement.dataset.big='';} /* html[data-big]: text at 125 % or more, fixed multi-column layouts fall back to reflow */
addEventListener('DOMContentLoaded',()=>{
 document.querySelectorAll('.trunc:not([title])').forEach(e=>e.title=e.textContent.trim()); /* peek = full label */
 const st=document.body.dataset.state; /* active nav slot = aria-current (persist_check masks it) */
 document.querySelectorAll('[data-stale-in]').forEach(e=>{if(e.dataset.staleIn.split(' ').includes(st))e.classList.add('stale')});
 document.querySelectorAll('[data-for]').forEach(e=>{if(e.dataset.for.split(' ').includes(st))e.setAttribute('aria-current','page')});
 /* constant on-screen width for scaled 3D outlines: --k = user units per CSS px */
 document.querySelectorAll('.viewport>svg').forEach(v=>{const vb=v.viewBox.baseVal,fit=()=>{const b=v.getBoundingClientRect();if(b.width)v.style.setProperty('--k',Math.max(vb.width/b.width,vb.height/b.height))};
  fit();new ResizeObserver(fit).observe(v)});
 /* hold-to-acknowledge: 1500 ms (motion.duration.hold); release cancels */
 document.querySelectorAll('.hold').forEach(h=>{const on=()=>h.classList.add('holding'),off=()=>h.classList.remove('holding');
  h.addEventListener('pointerdown',on);['pointerup','pointerleave','pointercancel','blur'].forEach(x=>h.addEventListener(x,off));
  h.addEventListener('keydown',e=>{if(e.key==' '||e.key=='Enter'){e.preventDefault();on()}});h.addEventListener('keyup',off);
  h.addEventListener('transitionend',e=>{if(h.classList.contains('holding')&&e.propertyName=='opacity'){off();acked()}})});
});
function confirmAck(){document.getElementById('ack').showModal()} /* desktop/tablet: confirm step, focus on CANCEL */
function acked(){document.body.classList.add('acked');document.querySelectorAll('.ack-state').forEach(e=>e.textContent='09:54:12 · ACKED')}
