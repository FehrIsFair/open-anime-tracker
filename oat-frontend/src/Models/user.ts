import _ from 'lodash'


export interface User {
  username: string
  email: string
  password: string
}


export const to_json = (object: User): any => {
  return _(object).toJSON()
}

export default User