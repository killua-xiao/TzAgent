import './style/index.js';
export type { CheckboxProps } from './Checkbox';
export type { CheckboxGroupProps } from './CheckboxGroup';
export * from './type';
export declare const Checkbox: import("react").FunctionComponent<import("./Checkbox").CheckboxProps & import("react").RefAttributes<HTMLLabelElement>> & {
    Group: {
        <T extends import("./type").CheckboxGroupValue = import("./type").CheckboxGroupValue>(props: import("./CheckboxGroup").CheckboxGroupProps<T>): import("react").JSX.Element;
        displayName: string;
    };
};
export default Checkbox;
