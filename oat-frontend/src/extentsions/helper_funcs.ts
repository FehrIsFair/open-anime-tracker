interface AnyNumber {
    [rating: number]: any
}
interface IsNumber {
    (number: number): number
}
export type MaybeNumber = AnyNumber | IsNumber;