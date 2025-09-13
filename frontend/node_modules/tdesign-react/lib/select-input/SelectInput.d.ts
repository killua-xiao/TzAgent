import React from 'react';
import { PopupRef } from '../popup';
import { TdSelectInputProps } from './type';
import { StyledProps } from '../common';
import { InputRef } from '../input';
export interface SelectInputProps extends TdSelectInputProps, StyledProps {
    updateScrollTop?: (content: HTMLDivElement) => void;
    options?: any[];
}
declare const SelectInput: React.ForwardRefExoticComponent<SelectInputProps & React.RefAttributes<Partial<PopupRef & InputRef>>>;
export default SelectInput;
