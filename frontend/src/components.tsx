import {useState,type ReactNode} from 'react';
import {Mic,Volume2,LoaderCircle,ShieldCheck,MapPin} from 'lucide-react';
import {districts,districtHi,disclaimer,type Language} from './i18n';
export function Notice({children}:{children:ReactNode}){return <div className="notice"><ShieldCheck size={18}/><span>{children}</span></div>}
export function Safety(){return <div className="safety">{disclaimer}<br/><small>AI-based advisory. Verify important crop-treatment decisions with a qualified agriculture expert/KVK.</small></div>}
export function Busy(){return <div className="busy"><LoaderCircle className="spin"/> कृपया प्रतीक्षा करें…</div>}
export function DistrictSelect({value,onChange,lang}:{value:string;onChange:(s:string)=>void;lang:Language}){return <label className="district-picker"><MapPin size={16}/><select aria-label="District" value={value} onChange={e=>onChange(e.target.value)}>{districts.map(d=><option key={d} value={d}>{lang==='hi'?districtHi[d]:d}</option>)}</select></label>}
export function VoiceButton({onText,lang}:{onText:(text:string)=>void;lang:Language}){
 const [listening,setListening]=useState(false);const [error,setError]=useState('');
 function start(){
  const speech=(window as any).SpeechRecognition||(window as any).webkitSpeechRecognition;
  if(!speech){setError('इस ब्राउज़र में आवाज़ सुविधा उपलब्ध नहीं है। कृपया लिखकर पूछें।');return;}
  const recognition=new speech();recognition.lang=lang==='hi'?'hi-IN':'en-IN';recognition.interimResults=false;
  recognition.onresult=(e:any)=>onText(e.results[0][0].transcript);recognition.onend=()=>setListening(false);
  recognition.onerror=()=>{setListening(false);setError('माइक्रोफ़ोन अनुमति और इंटरनेट जाँचें।');};
  try{recognition.start();setListening(true);setError('');}catch{setError('माइक्रोफ़ोन शुरू नहीं हो सका।');}
 }
 return <><button type="button" className={listening?'voice listening':'voice'} onClick={start} disabled={listening}><Mic size={20}/>{listening?'सुन रहे हैं…':lang==='hi'?'बोलकर पूछें':'Ask by voice'}</button>{error&&<p role="alert" className="error">{error}</p>}</>
}
export function Speak({text,lang}:{text:string;lang:Language}){return <button className="text-button" onClick={()=>{if('speechSynthesis' in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=lang==='hi'?'hi-IN':'en-IN';speechSynthesis.speak(u);}}}><Volume2 size={17}/> {lang==='hi'?'सुनें':'Listen'}</button>}
export function Field({label,children}:{label:string;children:ReactNode}){return <label className="field"><span>{label}</span>{children}</label>}
