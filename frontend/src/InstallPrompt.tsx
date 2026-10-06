import {useEffect,useState} from 'react';
import {Download,X} from 'lucide-react';
interface InstallEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{outcome:'accepted'|'dismissed'}>;
}
/** Installation remains a user action; never prompt automatically. */
export default function InstallPrompt(){
 const [event,setEvent]=useState<InstallEvent|null>(null);
 const [dismissed,setDismissed]=useState(false);
 const [error,setError]=useState('');
 useEffect(()=>{
  const available=(e:Event)=>{e.preventDefault();setEvent(e as InstallEvent)};
  const installed=()=>setEvent(null);
  window.addEventListener('beforeinstallprompt',available);
  window.addEventListener('appinstalled',installed);
  return()=>{window.removeEventListener('beforeinstallprompt',available);window.removeEventListener('appinstalled',installed)};
 },[]);
 async function install(){
  if(!event)return;
  try{await event.prompt();await event.userChoice;setEvent(null)}
  catch{setError('Chrome मेनू से “Install app” चुनें।')}
 }
 if(!event||dismissed)return null;
 return <aside className="install-prompt" aria-label="Install application"><div><strong>शिवम एग्री AI अपने फोन में रखें</strong><p>होम स्क्रीन से सीधे खोलें। APK की जरूरत नहीं।</p>{error&&<p role="alert">{error}</p>}</div><button className="primary" onClick={install}><Download size={18}/> ऐप इंस्टॉल करें</button><button onClick={()=>setDismissed(true)} aria-label="Dismiss install suggestion"><X size={18}/></button></aside>;
}
