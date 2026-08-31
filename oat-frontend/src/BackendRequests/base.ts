import axios from 'axios'

const engine = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true,
})
export default engine