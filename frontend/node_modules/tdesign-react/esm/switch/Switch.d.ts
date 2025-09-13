import React from 'react';
import { StyledProps } from '../common';
import { SwitchValue, TdSwitchProps } from './type';
export type SwitchChangeEventHandler = (value: boolean, event: React.MouseEvent<HTMLButtonElement>) => void;
export type SwitchClickEventHandler = SwitchChangeEventHandler;
export interface SwitchProps<T extends SwitchValue = SwitchValue> extends TdSwitchProps<T>, StyledProps {
}
declare const _default: <T extends SwitchValue = SwitchValue>(props: SwitchProps<T> & React.RefAttributes<HTMLButtonElement>) => React.ReactElement;
export default _default;
