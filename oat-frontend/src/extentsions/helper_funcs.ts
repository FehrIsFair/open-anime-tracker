import Cookies from 'universal-cookie'

interface AnyNumber {
    [rating: number]: any
}
interface IsNumber {
    (number: number): number
}

export const cookie_handler = new Cookies()

export type MaybeNumber = AnyNumber | IsNumber;