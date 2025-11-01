import axios from 'axios'

const server = axios.create({
  baseURL: 'http://localhost:8001/',
  timeout: 5000,
})

export {server}
