import Button from "@mui/material/Button"


interface ButtonProps {
  variant: number
  submit_func: any
}


const SubmitBtn = (props: ButtonProps) => {

  const getVariant = (choice: number) => {
    switch (choice) {
      case 1:
        return 'text'
      case 2:
        return 'contained'
      case 3:
        return 'outlined'
      default:
        return 'contained'
    }
  }

  return (
    <>
      <Button
        variant={getVariant(props.variant)}
        onClick={() => props.submit_func()}
      >
          Submit
      </Button>
    </>
  )
}
export default SubmitBtn