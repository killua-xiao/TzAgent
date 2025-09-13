import React from 'react';
import { StyledProps } from '../common';
import { TdCheckboxProps } from '../checkbox/type';
export interface CheckProps extends TdCheckboxProps, StyledProps {
    type: 'radio' | 'radio-button' | 'checkbox';
    allowUncheck?: boolean;
    title?: string;
    children?: React.ReactNode;
    stopLabelTrigger?: Boolean;
}
/**
 * Check 组件支持使用 CheckContext 进行状态托管
 */
export declare const CheckContext: React.Context<CheckContextValue>;
/**
 * 托管 Check 组件的状态，请提供 inject() 方法注入托管好的 props
 */
export interface CheckContextValue {
    inject: (props: CheckProps) => CheckProps;
}
declare const Check: React.ForwardRefExoticComponent<CheckProps & React.RefAttributes<HTMLLabelElement>>;
export default Check;
