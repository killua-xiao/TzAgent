import React from 'react';
import { StyledProps } from '../common';
import type { FormInstanceFunctions, NamePath, TdFormItemProps } from './type';
export interface FormItemProps extends TdFormItemProps, StyledProps {
    children?: React.ReactNode | React.ReactNode[] | ((form: FormInstanceFunctions) => React.ReactElement);
}
export interface FormItemInstance {
    name?: NamePath;
    isUpdated?: boolean;
    value?: any;
    getValue?: Function;
    setValue?: Function;
    setField?: Function;
    validate?: Function;
    resetField?: Function;
    setValidateMessage?: Function;
    getValidateMessage?: Function;
    resetValidate?: Function;
    validateOnly?: Function;
    isFormList?: boolean;
}
declare const FormItem: React.ForwardRefExoticComponent<FormItemProps & React.RefAttributes<FormItemInstance>>;
export default FormItem;
