import type * as React from 'react';
import type { Root } from 'react-dom/client';
type CreateRoot = (container: ContainerType) => Root;
declare const MARK = "__td_react_root__";
type ContainerType = (Element | DocumentFragment) & {
    [MARK]?: Root;
};
export declare function render(node: React.ReactElement, container: ContainerType): void;
export declare function unmount(container: ContainerType): Promise<void>;
/**
 * @deprecated Set React render function for compatible usage.
 * This is internal usage only compatible with React 19.
 * And will be removed in next major version.
 */
export declare function renderAdapter(render?: CreateRoot): void;
export {};
