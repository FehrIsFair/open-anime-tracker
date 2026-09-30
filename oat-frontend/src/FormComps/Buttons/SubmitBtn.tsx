import Button, { ButtonProps as MuiButtonProps } from "@mui/material/Button";

interface ButtonProps extends Omit<MuiButtonProps, "variant"> {
  variant?: MuiButtonProps["variant"];
  onSubmit?: () => void;
  testId?: string;
}

const SubmitBtn = (props: ButtonProps): JSX.Element => {
  const { variant = "contained", children = "Submit", onSubmit, testId = "qa-submit_btn-submit", ...rest } = props;

  return (
    <Button
      data-testid={testId}
      variant={variant}
      onClick={onSubmit}
      {...rest}
    >
      {children}
    </Button>
  );
};
export default SubmitBtn;
