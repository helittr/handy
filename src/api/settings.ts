import { server } from "@/utils/server";


export interface scriptManager {
  scriptPath:string
  logPath:string
  scriptPackages:[string]
}

export interface settings {
  theme:string
  collapsed:boolean
  lastUpdate:number
  scriptManager:scriptManager
}

export async function get_settings():Promise<settings>{
  const res = await server.get('/settings')
  return res.data.data as settings
}

export async function update_settings(settings:settings){
  return server.post('/settings', settings)
}
