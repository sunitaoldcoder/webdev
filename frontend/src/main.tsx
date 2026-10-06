import React from 'react';
import {createRoot} from 'react-dom/client';
import App from './App';
import InstallPrompt from './InstallPrompt';
import './styles.css';
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/><InstallPrompt/></React.StrictMode>);
if(import.meta.env.PROD && 'serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
