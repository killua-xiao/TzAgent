import React from 'react';
import type { TdFormProps } from './type';
import useForm from './hooks/useForm';
import useWatch from './hooks/useWatch';
import { StyledProps } from '../common';
export interface FormProps extends TdFormProps, StyledProps {
    children?: React.ReactNode;
}
declare const Form: React.FunctionComponent<FormProps & React.RefAttributes<any>> & {
    useForm: typeof useForm;
    useWatch: typeof useWatch;
    FormItem: React.ForwardRefExoticComponent<import("./FormItem").FormItemProps & React.RefAttributes<import("./FormItem").FormItemInstance>>;
    FormList: React.FC<import("./type").TdFormListProps>;
};
export default Form;
