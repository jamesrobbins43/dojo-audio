/* Remember the audio input the member used last, shared by every tool (CJ Nov 22 2026: "Always remember the input previously used").
   localStorage 'dgu-mic' = {id,label}. Device ids can change between visits (Safari, private windows), so we also match by label.
   Usage (self-defining, works wherever it's pasted):  window.dguMic.pick(currentId, strict?) -> Promise<deviceId>,  window.dguMic.save(track), window.dguMic.id() */
(window.dguMic||(window.dguMic={
  read(){ try{ const v=localStorage.getItem('dgu-mic'); if(!v) return null; if(v[0]==='{') return JSON.parse(v); return {id:v,label:''}; }catch(e){ return null; } },
  id(){ const s=this.read(); return s&&s.id||''; },
  save(t){ try{ if(!t) return; const set=t.getSettings?t.getSettings():{}; const id=set.deviceId||''; if(!id) return; localStorage.setItem('dgu-mic',JSON.stringify({id,label:t.label||''})); }catch(e){} },
  async pick(cur,strict){ const sv=this.read(); const want=cur||(!strict&&sv&&sv.id)||''; if(!want) return '';
    let ds=[]; try{ ds=(await navigator.mediaDevices.enumerateDevices()).filter(d=>d.kind==='audioinput'); }catch(e){ return want; }
    if(ds.some(d=>d.deviceId===want)) return want;
    if(sv&&sv.label&&((!cur&&!strict)||cur===sv.id)){ const m=ds.find(d=>d.label===sv.label); if(m) return m.deviceId; }
    return want; }
}))
