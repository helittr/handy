import { server } from "@/utils/server";


export async function sys_start(path:string){
  const res = await server.post('/sys/start', path)
  if (res.status == 200) {
    return res.data.code == 0
  }
  return false
}
