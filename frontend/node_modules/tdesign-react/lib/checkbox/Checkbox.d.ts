import React from 'react';
import { CheckProps } from '../common/Check';
export type CheckboxProps = Omit<CheckProps, 'type'>;
declare const Checkbox: React.FunctionComponent<CheckboxProps & React.RefAttributes<HTMLLabelElement>> & {
    Group: {
        <T extends import("./type").CheckboxGroupValue = import("./type").CheckboxGroupValue>(props: import("./CheckboxGroup").CheckboxGroupProps<T>): React.JSX.Element;
        displayName: string;
    };
};
export default Checkbox;
