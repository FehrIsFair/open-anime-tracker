import _ from 'lodash'


interface User {
  username: string | null
  email: string | null
  password: string | null
}


export const to_json = (object: any): any => {
  return _(object).toJSON()
}

export interface Login {
  email: string
  password: string
}

export default User