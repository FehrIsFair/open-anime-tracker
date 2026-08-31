import Button, { ButtonProps as MuiButtonProps } from "@mui/material/Button";

interface ButtonProps extends Omit<MuiButtonProps, "variant"> {
  variant?: MuiButtonProps["variant"];
  onSubmit?: () => void;
}

const SubmitBtn = (props: ButtonProps): JSX.Element => {
  const { variant = "contained", children = "Submit", onSubmit, ...rest } = props;

  return (
    <Button
      variant={variant}
      onClick={onSubmit}
      {...rest}
    >
      {children}
    </Button>
  );
};
export default SubmitBtn;
