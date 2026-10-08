let token=sessionStorage.getItem('agri-token')||'';
export function setToken(value:string){token=value;if(value)sessionStorage.setItem('agri-token',value);else sessionStorage.removeItem('agri-token');}
export function hasToken(){return !!token;}
export class ApiError extends Error {
 constructor(message:string, public status:number){super(message);this.name='ApiError';}
}
export async function api<T=any>(path:string, options:RequestInit={}):Promise<T>{
 const headers:Record<string,string>={};
 if(token)headers.Authorization=`Token ${token}`;
 if(options.body && !(options.body instanceof FormData))headers['Content-Type']='application/json';
 const response=await fetch(`/api/${path}`,{...options,headers:{...headers,...options.headers}});
 const body=await response.json().catch(()=>({}));
 if(!response.ok)throw new ApiError(typeof body.error==='string'?body.error:JSON.stringify(body.error||body)||`HTTP ${response.status}`,response.status);
 return body.data;
}
export const post=<T=any>(path:string,data:unknown)=>api<T>(path,{method:'POST',body:JSON.stringify(data)});
