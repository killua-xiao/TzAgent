import './style/index.js';
export type { FormProps } from './Form';
export type { FormItemProps } from './FormItem';
export * from './type';
export * from './hooks/interface';
export declare const Form: import("react").FunctionComponent<import("./Form").FormProps & import("react").RefAttributes<any>> & {
    useForm: typeof import("./hooks/useForm").default;
    useWatch: typeof import("./hooks/useWatch").default;
    FormItem: import("react").ForwardRefExoticComponent<import("./FormItem").FormItemProps & import("react").RefAttributes<import("./FormItem").FormItemInstance>>;
    FormList: import("react").FC<import("./type").TdFormListProps>;
};
export default Form;
