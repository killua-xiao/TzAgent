export declare const supportRef: (nodeOrComponent: any) => boolean;
export declare function getRefDom(domRef: React.RefObject<any>): any;
interface RefAttributes<T> extends React.Attributes {
    ref: React.Ref<T>;
}
export declare const supportNodeRef: <T = any>(node: React.ReactNode) => node is React.ReactElement & RefAttributes<T>;
/**
 * In React 19. `ref` is not a property from node.
 * But a property from `props.ref`.
 * To check if `props.ref` exist or fallback to `ref`.
 */
export declare const getNodeRef: <T = any>(node: React.ReactNode) => React.Ref<T> | null;
export {};
