import { FormControl, TextField } from "@mui/material";

interface InputProps {
  id: string;
  label: string;
  value: string;
  set_field: any;
}

const EmailComponent = (props: InputProps): JSX.Element => {
  const onChange = (event: any) => {
    props.set_field(event.target.value as string);
  };

  return (
    <>
      <FormControl>
        <TextField
          id={props.id}
          label={props.label}
          variant="outlined"
          value={props.value}
          onChange={onChange}
          type="email"
        />
      </FormControl>
    </>
  );
};
export default EmailComponent;