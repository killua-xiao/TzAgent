import React from 'react';
import { CheckboxGroupValue, TdCheckboxGroupProps } from './type';
import { StyledProps } from '../common';
export interface CheckboxGroupProps<T extends CheckboxGroupValue = CheckboxGroupValue> extends TdCheckboxGroupProps<T>, StyledProps {
    children?: React.ReactNode;
}
/**
 * 多选选项组，里面可以嵌套 <Checkbox />
 */
declare const CheckboxGroup: {
    <T extends CheckboxGroupValue = CheckboxGroupValue>(props: CheckboxGroupProps<T>): React.JSX.Element;
    displayName: string;
};
export default CheckboxGroup;
