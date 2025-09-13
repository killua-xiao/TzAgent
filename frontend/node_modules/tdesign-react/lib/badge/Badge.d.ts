import React from 'react';
import { StyledProps } from '../common';
import { TdBadgeProps } from './type';
export interface BadgeProps extends TdBadgeProps, StyledProps {
}
declare const Badge: React.ForwardRefExoticComponent<BadgeProps & React.RefAttributes<HTMLSpanElement>>;
export default Badge;
