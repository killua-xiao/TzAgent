import { FormItemProps } from '../FormItem';
export declare const ctrlKeyMap: Map<any, any>;
export declare const initialDataMap: Map<any, any>;
export default function useFormItemInitialData(name: FormItemProps['name']): {
    getDefaultInitialData: ({ children, initialData, }: {
        children: FormItemProps["children"];
        initialData: FormItemProps["initialData"];
    }) => any;
};
