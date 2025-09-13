import React from 'react';
import { AttachNode, AttachNodeReturnValue } from '../common';
export interface PortalProps {
    /**
     * 指定挂载的 HTML 节点, false 为挂载在 body
     */
    attach?: React.ReactElement | AttachNode | boolean;
    /**
     * 触发元素
     */
    triggerNode?: HTMLElement;
    children: React.ReactNode;
}
export declare function getAttach(attach: PortalProps['attach'], triggerNode?: HTMLElement): AttachNodeReturnValue;
declare const Portal: React.ForwardRefExoticComponent<PortalProps & React.RefAttributes<unknown>>;
export default Portal;
