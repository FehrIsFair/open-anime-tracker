import axios from 'axios'

const engine = axios.create({
  baseURL: 'http://localhost:5000'
})
export default engine