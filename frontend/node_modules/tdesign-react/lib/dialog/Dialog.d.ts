import React from 'react';
import type { StyledProps } from '../common';
import type { DialogInstance, TdDialogProps } from './type';
export interface DialogProps extends TdDialogProps, StyledProps {
    isPlugin?: boolean;
}
declare const Dialog: React.ForwardRefExoticComponent<DialogProps & React.RefAttributes<DialogInstance>>;
export default Dialog;
