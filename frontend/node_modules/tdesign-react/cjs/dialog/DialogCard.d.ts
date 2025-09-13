import React from 'react';
import { TdDialogCardProps } from './type';
import { StyledProps } from '../common';
export interface DialogCardProps extends TdDialogCardProps, StyledProps, React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
}
declare const DialogCard: React.ForwardRefExoticComponent<DialogCardProps & React.RefAttributes<HTMLDivElement>>;
export default DialogCard;
