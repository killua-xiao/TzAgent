import React from 'react';
export interface InputGroupProps extends React.HTMLAttributes<HTMLDivElement> {
    /**
     * 是否拆分
     * @default false
     */
    separate?: boolean;
}
declare const InputGroup: React.ForwardRefExoticComponent<InputGroupProps & React.RefAttributes<HTMLDivElement>>;
export default InputGroup;
