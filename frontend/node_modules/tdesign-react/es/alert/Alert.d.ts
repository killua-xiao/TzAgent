import React from 'react';
import { TdAlertProps } from './type';
import { StyledProps } from '../common';
export interface AlertProps extends TdAlertProps, StyledProps {
}
declare const Alert: React.ForwardRefExoticComponent<AlertProps & React.RefAttributes<HTMLDivElement>>;
export default Alert;
