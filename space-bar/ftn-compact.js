/* Find the Note, compact run screen (CJ, Nov 22 2026): hint box first, then ONE row with the small buttons and Show answer */
{ const st=document.createElement('style'); st.textContent=`
.w-play .fb{min-height:0;padding:7px 14px;font-size:16px;margin-top:10px;gap:10px;border-radius:12px}
.w-play .fb .ic{width:28px;height:28px;font-size:15px}.w-play .fb .tx small{font-size:14px}
.ftn-row{display:block}
.w-play .ftn-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-top:10px}
.w-play .ftn-row .controls{margin:0!important;flex:0 1 auto}
.w-play .ftn-row .controls .btn{padding:8px 13px;font-size:15px}
.w-play .ftn-row .bigrow{margin:0;flex:1 1 180px}
.w-play .ftn-row .bigrow #nextBtn{padding:9px 14px;font-size:16px;border-radius:10px}
.w-play .stage{padding-bottom:10px}
@media (max-width:560px){.w-play .ftn-row{gap:6px}.w-play .ftn-row .controls,.w-play .ftn-row .controls .toolbar{gap:6px!important}.w-play .ftn-row .controls .btn{padding:7px 10px;font-size:13px}.w-play .ftn-row .controls .icon-btn svg{width:14px;height:14px}.w-play .ftn-row .bigrow{flex-basis:100%}}`; root.appendChild(st);
  const ctl=root.querySelector('.controls'), big=$('bigrow'), fb=$('fb'), row=document.createElement('div'); row.className='ftn-row';
  ctl.before(fb); fb.after(row); row.append(ctl,big); }
